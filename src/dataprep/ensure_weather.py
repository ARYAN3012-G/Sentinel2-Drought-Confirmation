"""
Step 0: make sure the weather module is available and prepared.

    python src/dataprep/ensure_weather.py

The weather module (github.com/ARYAN3012-G/weather_time_series) is included as a git
submodule in external/weather_time_series. This script
  1. fetches it if the folder is empty (git submodule update --init), unless another copy is
     found (parent folder, sibling folder or WEATHER_MODULE_DIR — see src/config.py);
  2. runs the weather module's prepare_data.py if its data/prepared/ folder is missing or older
     than the raw weather files (site audit, duplicate removal, SPEI calibrated on 1979-2011;
     takes seconds).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SUBMODULE = ROOT / "external" / "weather_time_series"


def candidates():
    env = os.environ.get("WEATHER_MODULE_DIR")
    return [Path(env)] if env else [] + [ROOT.parent, ROOT.parent / "weather_time_series",
                                          ROOT.parent / "weather_module", SUBMODULE]


def find():
    for c in candidates():
        if (c / "src" / "dataprep" / "spei.py").exists():
            return c
    return None


def main():
    wdir = find()
    if wdir is None:
        print("Weather module not found - fetching the git submodule external/weather_time_series")
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=ROOT, check=True)
        wdir = find()
        if wdir is None:
            sys.exit("Could not get the weather module. Clone it with:\n"
                     "  git clone https://github.com/ARYAN3012-G/weather_time_series.git "
                     f"{SUBMODULE}")
    print(f"Weather module: {wdir}")
    prepared = wdir / "data" / "prepared"
    raw = list((wdir / "data" / "processed" / "weather").glob("*_with_spei.csv"))
    prep = list(prepared.glob("*.csv"))
    stale = bool(prep) and max(p.stat().st_mtime for p in raw) > min(p.stat().st_mtime for p in prep)
    if not prep or stale:
        print("Preparing weather data (weather module's prepare_data.py)"
              + (" - raw weather files are newer than the prepared ones" if stale else "") + " ...")
        subprocess.run([sys.executable, "src/dataprep/prepare_data.py"], cwd=wdir, check=True)
    n = len(list(prepared.glob("*.csv")))
    print(f"Weather data ready: {n} sites in {prepared}")


if __name__ == "__main__":
    main()
