"""
Download extra AgERA5 cells that some satellite sites lie in but the weather module does not
have (config.WEATHER_EXTRA), and store them in the weather module's PREPARED format.

    python tools/download_weather_cell.py [--end 2026-11-02]

Same CDS dataset, variables and column names as the weather module (its tools/update_agera5.py),
same SPEI rule: 30-day water balance P - ET0, log-logistic calibration on 1979-2011, frozen.
These cells are only used as INPUT for the satellite sites (and the weather module's model
forecasts for them); the weather model is never trained on them.
Needs a CDS account, the dataset licence accepted and ~/.cdsapirc. Output: data/weather_extra/<name>.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import config as C  # noqa: E402

U = C.weather_module("../tools/update_agera5.py")
spei = C.weather_module("dataprep/spei.py")


def prepared_frame(d: pd.DataFrame, name: str, lat: float, lon: float) -> pd.DataFrame:
    d = d.rename(columns=U.VARS).sort_values("valid_time").reset_index(drop=True)
    days = pd.date_range(d.valid_time.min(), d.valid_time.max())
    if len(days) != len(d) or d[U.CORE].isna().any().any():
        sys.exit(f"[{name}] download has gaps or missing values - not written")
    d["field"], d["latitude"], d["longitude"] = name, lat, lon
    d["cluster"] = "extra"
    d["Water_Balance"] = spei.water_balance(d)
    d["WB30"] = spei.accumulate(d["Water_Balance"], 30)
    cal = spei.SPEICalibrator(30, *C.SPEI_CALIB, 4.0).fit(d["valid_time"], d["WB30"])
    d["SPEI"] = cal.transform(d["valid_time"], d["WB30"]).to_numpy()
    s = d["SPEI"].to_numpy()
    d["label"] = np.where(s < -1.5, 2, np.where(s < 0.0, 1, 0))
    d.loc[d["SPEI"].isna(), "label"] = -1
    d["period"] = np.where(d.valid_time.dt.year <= 2011, "train",
                           np.where(d.valid_time.dt.year <= 2018, "val", "test"))
    return d[d["SPEI"].notna()].reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="1979-01-01")
    ap.add_argument("--end", default="2026-11-02")
    a = ap.parse_args()
    C.WEATHER_EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    cache = C.ROOT / "data" / "downloads"
    cache.mkdir(parents=True, exist_ok=True)
    for name, (lat, lon) in C.WEATHER_EXTRA.items():
        target = cache / f"{name}_{a.start}_{a.end}.download"
        d = U.read_download(target) if target.exists() else U.download(lat, lon, a.start, a.end, target)
        out = prepared_frame(d, name, lat, lon)
        out["valid_time"] = out["valid_time"].dt.strftime("%Y-%m-%d")
        out.to_csv(C.WEATHER_EXTRA_DIR / f"{name}.csv", index=False)
        jo = out[pd.to_datetime(out.valid_time).dt.month.between(6, 10)].assign(
            y=pd.to_datetime(out.valid_time).dt.year).groupby("y")["Precipitation_Flux"].sum()
        print(f"{name}: {out.valid_time.iloc[0]} -> {out.valid_time.iloc[-1]}, {len(out)} days; "
              f"Jun-Oct 2026 rain {jo.get(2026, np.nan):.0f} mm vs 1979-2011 mean {jo.loc[1979:2011].mean():.0f} mm")


if __name__ == "__main__":
    main()
