"""
Step 3: how does weather drought (SPEI) show up in crops (SVI)?

    python src/analysis/lag_analysis.py

A. Lag correlation: SVI(t) vs SPEI-k(t - lag), k in {30, 60, 90} days, lag 0-90 days,
   crop-season steps only, per site and rainfed / irrigated (pooled over sampled fields).
B. Confirmation: weather alarm = SPEI-30 falls below -1 (after >= 30 days above, crop season).
   Confirmed if the site's rainfed farmland reaches SVI < -1 within 60 days.
   Compared with the base rate for any crop-season date (does an alarm add information?).
C. Seasonal SVI per site and year (Aug-Nov, rainfed) for comparison with declared droughts.
Outputs: results/lag/{lag_correlation.csv, best_lag.csv, confirmation.csv, seasonal_vci.csv, LAG_REPORT.md}
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "lag"


def load():
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    w = pd.read_csv(C.CLEAN_DIR / "weather_5day.csv", parse_dates=["date"])
    z = None
    if (C.CLEAN_DIR / "zones_5day.csv").exists():
        z = pd.read_csv(C.CLEAN_DIR / "zones_5day.csv", parse_dates=["date"])
    return f, w, z


def add_lagged_spei(df: pd.DataFrame, w: pd.DataFrame) -> pd.DataFrame:
    """SPEI-k at date t - lag for every lag (weather is on the same 5-day grid)."""
    w = w.sort_values(["weather", "date"])
    cols = {}
    for lag in C.LAGS_DAYS:
        sh = w[["weather", "date"]].copy()
        sh["date"] = sh["date"] + pd.Timedelta(days=lag)          # value of day t-lag shown at t
        for k in C.SPEI_SCALES:
            sh[f"SPEI{k}_lag{lag}"] = w[f"SPEI{k}"].to_numpy()
        cols[lag] = sh
    out = df
    for lag in C.LAGS_DAYS:
        out = out.merge(cols[lag], on=["weather", "date"], how="left")
    return out


def lag_correlation(f: pd.DataFrame, w: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    d = f[f["date"].dt.month.isin(C.CROP_SEASON_MONTHS) & f["SVI"].notna()]
    d = add_lagged_spei(d[["field_id", "site_code", "irrigated", "weather", "date", "SVI"]], w)
    rows = []
    for (site, irr), g in d.groupby(["site_code", "irrigated"]):
        for k in C.SPEI_SCALES:
            for lag in C.LAGS_DAYS:
                x = g[f"SPEI{k}_lag{lag}"]
                ok = x.notna()
                r = g.loc[ok, "SVI"].corr(x[ok], method="spearman") if ok.sum() > 30 else np.nan
                rows.append(dict(site=site, irrigated=irr, spei_scale=k, lag_days=lag, rho=r, n=int(ok.sum())))
    corr = pd.DataFrame(rows)
    best = corr.loc[corr.groupby(["site", "irrigated"])["rho"].idxmax()].reset_index(drop=True)
    return corr, best


def site_rainfed_vci(f: pd.DataFrame, z: pd.DataFrame | None) -> dict[str, pd.DataFrame]:
    """Rainfed SVI per site from two sources, reported side by side:
    - median of the 20 sampled rainfed fields (each field is small, so it is often cloud-free);
    - whole-area rainfed farmland (zone). A whole 3 km area is rarely cloud-free in the monsoon,
      so in some sites the zone has too few reference points for SVI in Jul-Oct (no label)."""
    out = {"median of sampled fields": f[f["irrigated"] == 0].groupby(["site_code", "date"])["SVI"]
           .median().reset_index()}
    if z is not None:
        out["whole-area farmland"] = z[z["irrigated"] == 0][["site_code", "date", "SVI"]]
    return out


def confirmation(svci: pd.DataFrame, w: pd.DataFrame) -> pd.DataFrame:
    steps_reset = C.ALARM_RESET_DAYS // C.STEP_DAYS
    steps_win = C.CONFIRM_WINDOW_DAYS // C.STEP_DAYS
    rows = []
    for site, g in svci.groupby("site_code"):
        wx = w[w["weather"] == C.SITES[site]["weather"]].set_index("date")["SPEI30"]
        g = g.set_index("date").sort_index()
        dates = g.index
        spei30 = wx.reindex(dates).to_numpy()
        stress = (g["SVI"] < C.STRESS_Z).to_numpy()
        labelled = g["SVI"].notna().to_numpy()
        season = np.isin(dates.month, C.CROP_SEASON_MONTHS)

        def followed(i):
            j = slice(i + 1, i + 1 + steps_win)
            if not labelled[j].any():
                return None, None
            hit = np.where(stress[j] & labelled[j])[0]
            return (True, (hit[0] + 1) * C.STEP_DAYS) if len(hit) else (False, None)

        alarms, base = [], []
        for i in range(steps_reset, len(dates) - 1):
            if not season[i] or not np.isfinite(spei30[i]):
                continue
            hit, delay = followed(i)
            if hit is None:
                continue
            base.append(hit)
            prev = spei30[i - steps_reset:i]
            if spei30[i] < C.ALARM_SPEI and np.all(np.nan_to_num(prev, nan=0) >= C.ALARM_SPEI):
                already = bool(labelled[i] and stress[i])                 # stressed when the alarm fired
                censored = i + steps_win >= len(dates)                    # follow-up window incomplete
                alarms.append((dates[i].date(), hit, delay, already, censored))
        n = len(alarms)
        hits = sum(a[1] for a in alarms)
        delays = [a[2] for a in alarms if a[1]]
        new = [a for a in alarms if not a[3]]
        rows.append(dict(site=site, alarms=n, confirmed=hits,
                         already_stressed_at_alarm=sum(a[3] for a in alarms),
                         new_onset_confirmed=f"{sum(a[1] for a in new)}/{len(new)}",
                         follow_up_incomplete=sum(a[4] for a in alarms),
                         confirmation_rate=round(hits / n, 3) if n else np.nan,
                         base_rate_any_date=round(float(np.mean(base)), 3) if base else np.nan,
                         median_delay_days=float(np.median(delays)) if delays else np.nan,
                         alarm_dates=", ".join(str(a[0]) for a in alarms)))
    return pd.DataFrame(rows)


def seasonal(svci: pd.DataFrame) -> pd.DataFrame:
    s = svci[svci["date"].dt.month.isin([8, 9, 10, 11])].copy()
    s["year"] = s["date"].dt.year
    return s.pivot_table(index="site_code", columns="year", values="SVI", aggfunc="mean").round(2)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f, w, z = load()
    corr, best = lag_correlation(f, w)
    corr.to_csv(OUT / "lag_correlation.csv", index=False)
    best.to_csv(OUT / "best_lag.csv", index=False)
    pooled = (corr.groupby(["irrigated", "spei_scale", "lag_days"])["rho"].median()
              .unstack("lag_days").round(2))
    sources = site_rainfed_vci(f, z)
    conf = {k: confirmation(v, w) for k, v in sources.items()}
    pd.concat([c.assign(source=k) for k, c in conf.items()]).to_csv(OUT / "confirmation.csv", index=False)
    seas = {k: seasonal(v) for k, v in sources.items()}
    pd.concat([s.assign(source=k) for k, s in seas.items()]).to_csv(OUT / "seasonal_vci.csv")
    labelled = {k: v[v["date"].dt.month.isin([7, 8, 9, 10]) & v["date"].dt.year.eq(2026)]
                .groupby("site_code")["SVI"].apply(lambda x: f"{x.notna().mean():.0%}") for k, v in sources.items()}

    lines = ["# Weather drought -> crop stress", "",
             "## A. Lag correlation (Spearman rho between SVI on day t and SPEI-k on day t-lag)", "",
             "Descriptive association over all available years, best of 3 scales x 19 lags (not a causal lag; "
             "SPEI-90 at lag 0 already summarises the previous 90 days of weather).", "",
             "Crop-season steps (Jul-Nov) with a label. Positive rho = wetter weather, healthier crops.", "",
             "### Median over sites (rows: irrigated 0/1, SPEI scale; columns: lag in days)", "",
             to_md(pooled), "",
             "### Strongest link per site", "", to_md(best.round(3), index=False), "",
             "## B. Does a weather alarm predict satellite-confirmed stress?", "",
             f"Alarm: SPEI-30 < {C.ALARM_SPEI} after >= {C.ALARM_RESET_DAYS} days above, in Jul-Nov. "
             f"Confirmed: rainfed farmland SVI < {C.STRESS_Z:g} within {C.CONFIRM_WINDOW_DAYS} days. "
             "Base rate = same check for every crop-season date. An alarm is informative only if "
             "its confirmation rate is clearly above the base rate. Descriptive: alarms come from OBSERVED "
             "SPEI-30 (not from the weather module's forecasts), sites sharing a weather cell (Lepakshi, "
             "Cholasamudram) share alarm dates, and 3-7 alarms per site are too few for site-level tests. "
             "already_stressed_at_alarm = crops were below the threshold when the alarm fired (not a new onset); "
             "new_onset_confirmed counts only the others.", "",
             "Two sources of site SVI (same label rules): median of the sampled rainfed fields, "
             "and the whole-area rainfed farmland. Share of Jul-Oct 2026 dates with an SVI value:", "",
             to_md(pd.DataFrame(labelled)), ""]
    for k, c in conf.items():
        lines += [f"### Source: {k}", "", to_md(c.drop(columns=["alarm_dates"]), index=False), ""]
    lines += ["## C. Mean Aug-Nov SVI of rainfed farmland per year (negative = worse than normal)", "",
              "Compare with official drought declarations (data/official/drought_declarations.csv).", ""]
    for k, sd in seas.items():
        lines += [f"### Source: {k}", "", to_md(sd), ""]
    (OUT / "LAG_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT / 'LAG_REPORT.md'}")


if __name__ == "__main__":
    main()
