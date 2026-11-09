"""
Link to the weather module: daily ERA5-Land weather -> the satellite 5-day grid.

    python src/dataprep/weather_link.py

For every weather site used by the satellite sites (Lepakshi uses Cholasamudram):
  - SPEI-30/60/90 with the weather module's log-logistic calibrator, fitted on 1979-2011
    only and frozen (same rule as the weather module);
  - 5-day values on grid date t use only days t-4 ... t (sums or means), SPEI is the value on day t.
Output: data/clean/weather_5day.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402
from dataprep.timeseries import make_grid  # noqa: E402

spei = C.weather_module("dataprep/spei.py")

RAW = {
    "P": ("Precipitation_Flux", "sum"),
    "ET0": ("ReferenceET_PenmanMonteith_FAO56", "sum"),
    "WB": ("Water_Balance", "sum"),
    "Tmax": ("Temperature_Air_2m_Max_24h", "mean"),
    "Tmin": ("Temperature_Air_2m_Min_24h", "mean"),
    "RHmax": ("Derived_Relative_Humidity_2m_Max_24h", "mean"),
    "RHmin": ("Derived_Relative_Humidity_2m_Min_24h", "mean"),
    "Solar": ("Solar_Radiation_Flux", "mean"),
    "Wind": ("Wind_Speed_10m_Mean_24h", "mean"),
}


def load_daily(weather_site: str) -> pd.DataFrame:
    path = C.WEATHER_PREPARED_DIR / f"{weather_site}.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} missing - run the weather module's "
                                "src/dataprep/prepare_data.py first.")
    d = pd.read_csv(path, parse_dates=["valid_time"]).sort_values("valid_time").reset_index(drop=True)
    d["Water_Balance"] = spei.water_balance(d)
    for k in C.SPEI_SCALES:
        acc = spei.accumulate(d["Water_Balance"], k)
        cal = spei.SPEICalibrator(k, *C.SPEI_CALIB).fit(d["valid_time"], acc)
        d[f"SPEI{k}"] = cal.transform(d["valid_time"], acc).to_numpy()
    return d


def to_5day(d: pd.DataFrame, grid: pd.DatetimeIndex) -> pd.DataFrame:
    """Aggregate days (t-STEP+1 ... t] onto grid date t. Uses no day after t."""
    s = d.set_index("valid_time")
    out = pd.DataFrame(index=grid)
    for name, (col, how) in RAW.items():
        r = s[col].rolling(f"{C.STEP_DAYS}D", min_periods=C.STEP_DAYS)
        out[name] = (r.sum() if how == "sum" else r.mean()).reindex(grid)
    for k in C.SPEI_SCALES:
        out[f"SPEI{k}"] = s[f"SPEI{k}"].reindex(grid)
    return out.rename_axis("date").reset_index()


def main():
    grid = make_grid(C.GRID_START, pd.Timestamp("2026-12-31"), C.STEP_DAYS)
    frames = []
    for w in sorted({v["weather"] for v in C.SITES.values()}):
        d = load_daily(w)
        f = to_5day(d, grid)
        f.insert(0, "weather", w)
        frames.append(f)
        last = d["valid_time"].max().date()
        print(f"{w:24s} daily data to {last}")
    out = pd.concat(frames, ignore_index=True).dropna(subset=["P"])
    C.CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(C.CLEAN_DIR / "weather_5day.csv", index=False)
    print(f"Wrote {C.CLEAN_DIR / 'weather_5day.csv'} ({len(out)} rows)")


if __name__ == "__main__":
    main()
