"""
Step 5b: drought events and label checks.

    python src/analysis/drought_events.py

A. Drought seasons side by side (2023 and 2026 = dry, 2025 = normal): per site, Jun-Oct rain vs the
   1979-2011 normal, mean SPEI-30/90 in Aug-Oct, rainfed and irrigated SVI in Aug-Nov, and the share
   of rainfed sampled fields that were below normal (SVI < -1) or severe (SVI < -1.5) in Sep-Oct.
   Compare with official drought mandal lists (G.O.) - the satellite gives the share of fields hit.
B. Irrigation label check: a truly irrigated field should stay greener than rainfed fields in a
   drought season. Per irrigated field: mean SVI in drought seasons (2023, 2026 Aug-Nov) and the
   correlation of its SVI with SPEI-90. "Doubtful" = drops as much as the site's rainfed median
   in drought seasons AND responds to SPEI-90 at least as strongly as the rainfed median.
C. Lag robustness: best SPEI scale and lag per site for rainfed fields, leaving out one year at a
   time - shows whether one year drives a site's result (e.g. Somandepalle's 85-90 day lag).
Outputs: results/events/{drought_seasons.csv, irrigation_check.csv, lag_by_left_out_year.csv, EVENTS_REPORT.md}
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "events"
SEASONS = [2023, 2025, 2026]
DROUGHT_YEARS = [2023, 2026]


def rain_vs_normal() -> pd.DataFrame:
    """Jun-Oct rainfall per weather site and year vs the 1979-2011 normal (daily weather-module data)."""
    rows = []
    for path in sorted((C.WEATHER_DIR / "data" / "prepared").glob("*.csv")):
        site = path.stem
        d = pd.read_csv(path, usecols=["valid_time", "Precipitation_Flux"], parse_dates=["valid_time"])
        d = d.assign(y=d["valid_time"].dt.year)
        jo = d[d["valid_time"].dt.month.between(6, 10)].groupby("y")["Precipitation_Flux"].sum()
        normal = jo.loc[1979:2011].mean()
        for y in SEASONS:
            if y in jo.index:
                rows.append({"weather": site, "year": y, "rain_jun_oct_mm": round(jo[y]),
                             "rain_vs_normal_pct": round(100 * (jo[y] / normal - 1))})
    return pd.DataFrame(rows)


def drought_seasons(f, w) -> pd.DataFrame:
    rain = rain_vs_normal()
    rows = []
    for (site, wx), g in f.groupby(["site_code", "weather"]):
        for y in SEASONS:
            s = g[(g.date.dt.year == y)]
            aug_nov = s[s.date.dt.month.between(8, 11)]
            sep_oct = s[s.date.dt.month.between(9, 10) & (s.irrigated == 0)]
            ww = w[(w.weather == wx) & (w.date.dt.year == y) & w.date.dt.month.between(8, 10)]
            per_field = sep_oct.groupby("field_id")["SVI"].mean()
            r = rain[(rain.weather == wx) & (rain.year == y)]
            rows.append({
                "site": site, "year": y,
                "rain_jun_oct_mm": r.rain_jun_oct_mm.iloc[0] if len(r) else np.nan,
                "rain_vs_normal_%": r.rain_vs_normal_pct.iloc[0] if len(r) else np.nan,
                "SPEI30_aug_oct": round(ww["SPEI30"].mean(), 2) if len(ww) else np.nan,
                "SPEI90_aug_oct": round(ww["SPEI90"].mean(), 2) if len(ww) else np.nan,
                "SVI_rainfed_aug_nov": round(aug_nov[aug_nov.irrigated == 0]["SVI"].mean(), 2),
                "SVI_irrigated_aug_nov": round(aug_nov[aug_nov.irrigated == 1]["SVI"].mean(), 2),
                "rainfed_fields_below_normal_%": round(100 * (per_field < -1).mean()) if len(per_field) else np.nan,
                "rainfed_fields_severe_%": round(100 * (per_field < -1.5).mean()) if len(per_field) else np.nan,
                "rainfed_fields_n": len(per_field)})
    return pd.DataFrame(rows)


def irrigation_check(f, w) -> pd.DataFrame:
    d = f[f.date.dt.month.isin(C.CROP_SEASON_MONTHS) & f.SVI.notna()].merge(
        w[["weather", "date", "SPEI90"]], on=["weather", "date"], how="left")
    dry = d[d.date.dt.year.isin(DROUGHT_YEARS) & d.date.dt.month.between(8, 11)]
    per = pd.DataFrame({
        "drought_SVI": dry.groupby("field_id")["SVI"].mean(),
        "rho_SPEI90": d.groupby("field_id").apply(lambda g: g["SVI"].corr(g["SPEI90"], method="spearman")),
    }).join(f.groupby("field_id")[["site_code", "irrigated"]].first())
    rows = []
    for site, g in per.groupby("site_code"):
        rf, ir = g[g.irrigated == 0], g[g.irrigated == 1]
        doubt = ir[(ir.drought_SVI <= rf.drought_SVI.median()) & (ir.rho_SPEI90 >= rf.rho_SPEI90.median())]
        rows.append({"site": site, "irrigated_fields": len(ir), "doubtful": len(doubt),
                     "drought_SVI_rainfed_median": round(rf.drought_SVI.median(), 2),
                     "drought_SVI_irrigated_median": round(ir.drought_SVI.median(), 2),
                     "rho_rainfed_median": round(rf.rho_SPEI90.median(), 2),
                     "rho_irrigated_median": round(ir.rho_SPEI90.median(), 2),
                     "doubtful_field_ids": " ".join(map(str, doubt.index[:10]))})
    return pd.DataFrame(rows)


def lag_robustness(f, w) -> pd.DataFrame:
    d = f[f.date.dt.month.isin(C.CROP_SEASON_MONTHS) & f.SVI.notna() & (f.irrigated == 0)]
    d = d.groupby(["site_code", "weather", "date"], as_index=False)["SVI"].median()
    ws = w.sort_values(["weather", "date"])
    rows = []
    for (site, wx), g in d.groupby(["site_code", "weather"]):
        wx_s = ws[ws.weather == wx].set_index("date")
        for left_out in [None] + sorted(g.date.dt.year.unique()):
            gg = g if left_out is None else g[g.date.dt.year != left_out]
            best = (np.nan, None, None)
            for k in C.SPEI_SCALES:
                for lag in C.LAGS_DAYS:
                    x = wx_s[f"SPEI{k}"].reindex(gg.date - pd.Timedelta(days=lag)).to_numpy()
                    ok = ~np.isnan(x)
                    if ok.sum() < 30:
                        continue
                    rho = pd.Series(gg.SVI.to_numpy()[ok]).corr(pd.Series(x[ok]), method="spearman")
                    if np.isnan(best[0]) or rho > best[0]:
                        best = (rho, k, lag)
            rows.append({"site": site, "left_out_year": "none" if left_out is None else str(left_out),
                         "best_rho": round(best[0], 2), "best_SPEI": best[1], "best_lag_days": best[2]})
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    w = pd.read_csv(C.CLEAN_DIR / "weather_5day.csv", parse_dates=["date"])
    ds, ic, lr = drought_seasons(f, w), irrigation_check(f, w), lag_robustness(f, w)
    ds.to_csv(OUT / "drought_seasons.csv", index=False)
    ic.to_csv(OUT / "irrigation_check.csv", index=False)
    lr.to_csv(OUT / "lag_by_left_out_year.csv", index=False)
    lines = ["# Drought events and label checks", "",
             "## A. Drought seasons (2023, 2026 dry; 2025 normal)", "",
             "Rain = Jun-Oct total vs 1979-2011 normal (AgERA5). SVI < 0 = greener-than-normal is lost. "
             "Field shares: rainfed sampled fields with mean Sep-Oct SVI < -1 (below normal) or < -1.5 "
             "(severe). Compare with the official drought mandal lists for each year.", "",
             to_md(ds, index=False), "",
             "## B. Irrigation label check", "",
             "Drought SVI = mean SVI in Aug-Nov of 2023 and 2026. A real irrigated field should stay "
             "above its site's rainfed median. Doubtful = as low as the rainfed median AND as "
             "weather-driven (Spearman rho with SPEI-90) as the rainfed median.", "",
             to_md(ic, index=False), "",
             "## C. Lag robustness (rainfed fields, site median SVI, one year left out at a time)", "",
             "If the best scale/lag changes when one year is left out, that year drives the result.", "",
             to_md(lr.pivot(index="left_out_year", columns="site",
                            values="best_lag_days").reset_index(), index=False), "",
             to_md(lr, index=False), ""]
    (OUT / "EVENTS_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT / 'EVENTS_REPORT.md'}")


if __name__ == "__main__":
    main()
