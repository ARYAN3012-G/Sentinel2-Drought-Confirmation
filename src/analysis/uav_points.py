"""
Step 5c: satellite view of the UAV survey fields (independent check of stage 2).

    python src/analysis/uav_points.py

Input: data/gee_exports/B_uav_points_timeseries.csv (Sentinel-2 in a 25 m circle at each UAV
survey point, Earth Engine script B v2) and data/uav_points.csv (survey dates, UAV verdicts from
the dataset table: drought / healthy images). The same cleaning, 5-day grid and SVI reference
(2019-2023, own year excluded) as for the sampled fields are used.

Per point: NDVI, SVI and the departure from normal on the flight date, the lowest SVI in the
30 days before the flight, the mean SVI of the 2025 kharif season (Aug-Oct), and the satellite
verdict (stressed = SVI < -1 on or just before the flight date). The UAV verdict comes from the
UAV team's images and is NOT produced by this module - this is a comparison, not a model.
Output: results/uav/{uav_points_satellite.csv, UAV_POINTS_REPORT.md}
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402
from dataprep.build_dataset import INDICES, clean_observations, to_5day  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "uav"


def satellite_series() -> pd.DataFrame:
    raw = pd.read_csv(C.UAV_TS_FILE)
    raw = raw.rename(columns=lambda c: c[:-5] if c.endswith("_mean") else c)
    raw["date"] = pd.to_datetime(raw["date"])
    raw["full_px"] = raw.groupby("field_id")["NDVI_count"].transform("max")
    obs, _ = clean_observations(raw, "field_id", "NDVI_count", "full_px", C.MIN_CLEAR_FRAC_FIELD, INDICES)
    static = raw.groupby("field_id")[["site_code"]].first().reset_index()
    return to_5day(obs, "field_id", static, INDICES)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pts = pd.read_csv(C.UAV_POINTS_TABLE)
    g = satellite_series()
    rows = []
    for p in pts.itertuples():
        s = g[g.field_id == p.point_id].set_index("date").sort_index()
        rec = {"point": p.point_id, "site": p.site_code, "crop": p.crop, "uav_verdict": p.uav_verdict,
               "flight_date": p.flight_date if isinstance(p.flight_date, str) else "unknown"}
        kharif = s.loc["2025-08-01":"2025-10-31", "SVI"]
        rec["SVI_kharif_2025_mean"] = round(float(kharif.mean()), 2) if kharif.notna().any() else np.nan
        if isinstance(p.flight_date, str):
            fd = pd.Timestamp(p.flight_date)
            win = s.loc[fd - pd.Timedelta(days=30):fd]
            at = s.loc[:fd].dropna(subset=["NDVI"]).tail(1)
            if len(at):
                r = at.iloc[0]
                rec.update({"satellite_date": str(at.index[0].date()), "NDVI": round(r.NDVI, 3),
                            "NDVI_normal": round(r.ref_mean, 3) if np.isfinite(r.ref_mean) else np.nan,
                            "SVI": round(r.SVI, 2) if np.isfinite(r.SVI) else np.nan})
            rec["SVI_min_30d_before"] = round(float(win.SVI.min()), 2) if win.SVI.notna().any() else np.nan
            svi = rec.get("SVI", np.nan)
            low = rec["SVI_min_30d_before"]
            rec["satellite_verdict"] = ("no label (no normal crop signal or no clear image)" if np.isnan(svi) and np.isnan(low)
                                        else "stressed" if np.nanmin([svi, low]) < C.STRESS_Z else "not stressed")
        rows.append(rec)
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "uav_points_satellite.csv", index=False)
    lines = ["# Satellite view of the UAV survey fields", "",
             "Sentinel-2 in a 25 m circle at each UAV survey point (same cleaning and SVI reference as the "
             "sampled fields: 2019-2023, own year excluded). UAV verdict = majority of the UAV team's labelled "
             "images (dataset table; not produced here). Satellite verdict = stressed if SVI < -1 on the last "
             "clear image before the flight or at any point in the 30 days before it.", "",
             "Caution: the flights were in Nov 2025 - Jan 2026, partly after the kharif harvest. A harvested or "
             "drying maize field has low NDVI whatever the season, and SVI is unlabelled where the field has no "
             "normal crop signal at that time of year. Read disagreements with the crop stage in mind.", "",
             to_md(t, index=False), ""]
    (OUT / "UAV_POINTS_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(t[["point", "flight_date", "uav_verdict", "SVI", "SVI_min_30d_before", "satellite_verdict"]].to_string(index=False))
    print(f"Wrote {OUT / 'UAV_POINTS_REPORT.md'}")


if __name__ == "__main__":
    main()
