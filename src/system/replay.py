"""
Operational replay: run the integrated system every 5 days through each kharif season as if live,
with realistic data delays, and compare with the official drought declarations.

    python src/system/replay.py [--years 2023 2024 2025 2026]

On each issue date d (1 Jun - 30 Nov, every 5 days):
  weather  : AgERA5 is published ~WEATHER_DELAY_DAYS late -> SPEI-30/90 of day d - delay, and the
             weather module's +15-day forecast issued on that day (lead from d = 15 - delay days)
  satellite: Sentinel-2 images up to d - SAT_DELAY_DAYS (median SVI of the rainfed sampled fields,
             images at most 30 days old, at least MIN_SAT_FIELDS fields)
  status   : same rules as run_system.py (alarm / confirmed / continuing / insufficient data)
No crop model is used, so every year 2023-2026 is out-of-sample for the system (the weather model
is trained on 1979-2011; SVI normals exclude the scored year).

Per site and season: first alarm date, first confirmation date, and the official declaration
(data/official/drought_declarations.csv; AP G.O. dates). A declared mandal should be alarmed and
confirmed, ideally BEFORE the G.O.; a non-declared one should not be confirmed.
Outputs: results/replay/{replay_daily.csv, replay_seasons.csv, REPLAY_REPORT.md}
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "replay"
WEATHER_DELAY_DAYS = 7      # AgERA5 publication delay (about one week)
SAT_DELAY_DAYS = 2          # Sentinel-2 L2A availability
MIN_SAT_FIELDS = 5
H = 15
GO_DATES = {2023: "2023-10-31", 2024: "2024-10-29", 2025: "2025-10-31", 2026: "2026-10-01"}


def level(status: str) -> int:
    """Declared level: 0 none, 1 moderate, 2 severe; NaN unknown / ambiguous."""
    s = str(status).lower()
    if "unknown" in s or "/" in s:
        return np.nan
    return 2 if s.startswith("severe") else 1 if s.startswith("moderate") else 0 if "not declared" in s else np.nan


def season_end(y: int, w: pd.DataFrame, f: pd.DataFrame) -> pd.Timestamp:
    """Last issue date of a season: 30 Nov, or earlier when the data end (weather is published
    WEATHER_DELAY_DAYS late, satellite SAT_DELAY_DAYS late)."""
    last_w = w["date"].max() + pd.Timedelta(days=WEATHER_DELAY_DAYS)
    last_s = f.loc[f.SVI_c.notna(), "date"].max() + pd.Timedelta(days=SAT_DELAY_DAYS)
    return min(pd.Timestamp(f"{y}-11-30"), last_w, last_s)


def daily(years, stress_z: float = C.STRESS_Z) -> pd.DataFrame:
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    w = pd.read_csv(C.CLEAN_DIR / "weather_5day.csv", parse_dates=["date"])
    fc = pd.read_csv(C.CLEAN_DIR / "weather_forecasts.csv", parse_dates=["date"])
    fc = fc[fc.h == H]
    rain = f[(f.irrigated == 0) & f.SVI_c.notna() & (f.age_c <= C.MAX_INPUT_AGE)]
    rows = []
    for y in years:
        end = season_end(y, w, f)
        for d in pd.date_range(f"{y}-06-01", end, freq="5D"):
            dw, ds = d - pd.Timedelta(days=WEATHER_DELAY_DAYS), d - pd.Timedelta(days=SAT_DELAY_DAYS)
            for code in C.SITE_ORDER:
                wx = C.SITES[code]["weather"]
                ww = w[(w.weather == wx) & (w.date <= dw)].tail(1)
                ff = fc[(fc.weather == wx) & (fc.date <= dw) & (fc.date > dw - pd.Timedelta(days=5))].tail(1)
                last = rain[(rain.site_code == code) & (rain.date <= ds)]
                last = last[last.date == last.date.max()] if len(last) else last
                last = last[(ds - last.date).dt.days <= C.STEP_DAYS]
                if not len(ww) or (dw - ww.date.iloc[0]).days > C.STEP_DAYS:      # no stale weather
                    continue
                spei30, spei90 = float(ww.SPEI30.iloc[0]), float(ww.SPEI90.iloc[0])
                severe_fc = bool(len(ff) and ff[["p_healthy", "p_moderate", "p_severe"]].to_numpy()[0].argmax() == 2)
                alarm = spei30 < C.ALARM_SPEI or severe_fc
                ok = len(last) >= MIN_SAT_FIELDS
                med = float(last.SVI_c.median()) if len(last) else np.nan
                conf = ok and med < stress_z
                status = ("insufficient satellite data" if not ok else
                          "drought" if alarm and conf else
                          "drought continuing" if conf and spei90 < C.ALARM_SPEI else
                          "watch" if alarm else "crop stress, no alarm" if conf else "normal")
                rows.append(dict(year=y, issue_date=d.date(), site=code, SPEI30=round(spei30, 2),
                                 SPEI90=round(spei90, 2), severe_forecast=severe_fc, alarm=alarm,
                                 rainfed_fields=len(last), median_SVI=round(med, 2) if ok else np.nan,
                                 confirmed=conf, status=status))
    return pd.DataFrame(rows)


def seasons(dd: pd.DataFrame) -> pd.DataFrame:
    gov = pd.read_csv(C.ROOT / "data" / "official" / "drought_declarations.csv")
    sites = pd.read_csv(C.SITES_TABLE).set_index("site_code")
    out = []
    for (y, s), g in dd.groupby(["year", "site"]):
        g = g.sort_values("issue_date")
        a = g[g.alarm].issue_date
        c = g[g.status.isin(["drought", "drought continuing"])].issue_date
        dec = gov[(gov.site_code == s) & (gov.year == y)]
        od = dec.order_date.iloc[0] if len(dec) and "order_date" in dec and isinstance(dec.order_date.iloc[0], str) else ""
        go = pd.Timestamp(od if od else GO_DATES[y]).date()          # Karnataka (Sira) has its own order dates
        st = dec.status.iloc[0] if len(dec) else "unknown"
        last = max(g.issue_date)
        out.append(dict(year=y, site=s, mandal=sites.loc[s, "mandal"], weather_cell=sites.loc[s, "agera5_cell"],
                        design=("retrospective" if y <= max(C.TRAIN_YEARS) else "prospective"),
                        season_end=last, partial_season=last < pd.Timestamp(f"{y}-11-26").date(),
                        official=st, official_level=level(st), GO_date=go,
                        first_alarm=a.min() if len(a) else None, first_confirmed=c.min() if len(c) else None,
                        confirmed_dates=int(len(c)), dates_with_satellite=int((g.status != "insufficient satellite data").sum()),
                        confirmed_before_GO=bool(len(c) and c.min() <= go),
                        lead_days_before_GO=int((go - c.min()).days) if len(c) and c.min() <= go else np.nan))
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs="+", type=int, default=[2023, 2024, 2025, 2026])
    ap.add_argument("--sensitivity", nargs="*", type=float, default=[-0.75, -1.25],
                    help="extra confirmation thresholds to report (robustness only; -1 is the rule)")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    dd = daily(a.years)
    dd.to_csv(OUT / "replay_daily.csv", index=False)
    ss = seasons(dd)
    ss.to_csv(OUT / "replay_seasons.csv", index=False)
    known = ss[ss.official_level.notna()]

    def counts(k: pd.DataFrame) -> dict:
        """Eventual detection and advance warning, separately, per declared level."""
        out = {}
        for lev, name in ((2, "severe"), (1, "moderate")):
            g = k[k.official_level == lev]
            out[f"{name}: confirmed (eventually)"] = f"{int((g.confirmed_dates > 0).sum())}/{len(g)}"
            out[f"{name}: confirmed before order"] = f"{int(g.confirmed_before_GO.sum())}/{len(g)}"
        g = k[k.official_level == 0]
        out["not declared: confirmed (false alarm)"] = f"{int((g.confirmed_dates > 0).sum())}/{len(g)}"
        return out

    by_design = pd.DataFrame([{"site-seasons": n, **counts(k)} for n, k in
                              (("2023 (retrospective)", known[known.design == "retrospective"]),
                               ("2024-2026 (prospective)", known[known.design == "prospective"]),
                               ("all", known))])
    # mandal x season: each official decision counted once (sites in one mandal pooled; ambiguous excluded)
    mrows = []
    for (y, m), g in known.groupby(["year", "mandal"]):
        if g.official_level.nunique() != 1:
            continue
        conf = g[g.confirmed_dates > 0]
        first = min(conf.first_confirmed) if len(conf) else None
        go = g.GO_date.iloc[0]
        mrows.append(dict(year=y, mandal=m, sites=", ".join(g.site), weather_cells=g.weather_cell.nunique(),
                          official=g.official.iloc[0], official_level=g.official_level.iloc[0], order_date=go,
                          system_first_confirmed=first, confirmed=first is not None,
                          before_order=bool(first is not None and first <= go),
                          partial_season=bool(g.partial_season.any())))
    md = pd.DataFrame(mrows)
    md.to_csv(OUT / "replay_mandal_seasons.csv", index=False)
    md_sum = pd.DataFrame([{"mandal-seasons": "all", **{
        k.replace("site", "mandal"): v for k, v in counts(md.rename(columns={
            "before_order": "confirmed_before_GO"}).assign(confirmed_dates=md.confirmed.astype(int))).items()}}]) \
        if len(md) else pd.DataFrame()
    partial = ss[ss.partial_season].groupby("year").season_end.max()
    decl = known[known.official_level > 0]
    lines = ["# Operational replay of the integrated system, kharif 2023-2026", "",
             f"Every 5 days from 1 Jun to 30 Nov, or to the end of the data, with weather {WEATHER_DELAY_DAYS} days "
             f"late (AgERA5) and satellite {SAT_DELAY_DAYS} days late; weather older than {C.STEP_DAYS} days is "
             f"not used. Alarm = SPEI-30 < {C.ALARM_SPEI} or a Severe +{H}-day forecast; confirmed = median "
             f"rainfed SVI < {C.STRESS_Z:g} from >= {MIN_SAT_FIELDS} fields. No crop model is used.", "",
             "**Data ends.** " + ("; ".join(f"{y}: partial season, last issue date {d}" for y, d in partial.items())
                                  if len(partial) else "all seasons complete") + ".", "",
             "**Retrospective vs prospective.** The farmland mask, field segments and irrigation flag were derived "
             "from 2019-2023 imagery, so 2023 is RETROSPECTIVE (field selection saw that season; the SVI normal "
             "excludes 2023). 2024-2026 are PROSPECTIVE with respect to every fitted or selected component.", "",
             "**Thresholds fixed in advance.** SPEI < -1 (moderate drought, McKee et al. 1993 / WMO convention), "
             "SVI < -1 (one standard deviation below the field's normal), >= 5 fields and the data delays were "
             "set in run_system.py before this replay was written; they were not tuned on it.", "",
             "## Agreement with official declarations, site-seasons", "", to_md(by_design, index=False), "",
             f"Median lead before the order, declared site-seasons confirmed in advance: "
             f"{decl.lead_days_before_GO.median():.0f} days.", "",
             "## Each official decision counted once (mandal x season)", "",
             "Lepakshi and Cholasamudram lie in Lepakshi mandal and share one weather cell; Balaji Villas and "
             "Pullaiah lie in Kurnool Urban and share one weather cell. Here each mandal-season is one event "
             "(confirmed if any of its sites is confirmed; the Adoni / Peddakadubur border site is excluded).", "",
             to_md(md_sum, index=False) if len(md_sum) else "", "",
             to_md(md.drop(columns=["official_level"]), index=False) if len(md) else "", "",
             "## Season summary per site", "", to_md(ss, index=False), "",
             "Small sample (one area per mandal, 4 seasons): read as case evidence, not a statistical test.", ""]
    tab = by_design
    sens = []
    for z in [C.STRESS_Z] + list(a.sensitivity):
        k = seasons(dd if z == C.STRESS_Z else daily(a.years, z))
        k = k[k.official_level.notna()]
        d_ = k[k.official_level > 0]
        sens.append({"confirmation threshold (SVI <)": z,
                     "severe confirmed": f"{int((k[k.official_level == 2].confirmed_dates > 0).sum())}/{int((k.official_level == 2).sum())}",
                     "moderate confirmed": f"{int((k[k.official_level == 1].confirmed_dates > 0).sum())}/{int((k.official_level == 1).sum())}",
                     "not declared but confirmed": f"{int((k[k.official_level == 0].confirmed_dates > 0).sum())}/{int((k.official_level == 0).sum())}",
                     "declared, confirmed before order": f"{int(d_.confirmed_before_GO.sum())}/{len(d_)}"})
    lines += ["## Sensitivity to the confirmation threshold (robustness check; the rule stays SVI < -1)", "",
              to_md(pd.DataFrame(sens), index=False), ""]
    (OUT / "REPLAY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(by_design.to_string(index=False))
    print(md_sum.to_string(index=False) if len(md_sum) else "")
    print(md[["year", "mandal", "sites", "official", "system_first_confirmed", "before_order", "partial_season"]].to_string(index=False))


if __name__ == "__main__":
    main()
