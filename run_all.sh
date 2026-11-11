#!/usr/bin/env bash
# Satellite module (stage 2) - full pipeline. Run from this folder: bash run_all.sh
set -euo pipefail
cd "$(dirname "$0")"
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
echo "[setup] Requirements";       python -m pip install -r requirements.txt
echo "[0/7] Weather module";      python src/dataprep/ensure_weather.py
echo "[1/7] Clean + SVI labels";  python src/dataprep/build_dataset.py
echo "[2/7] Weather link";        python src/dataprep/weather_link.py
echo "[3/7] Weather forecasts";   python src/dataprep/weather_forecasts.py
echo "[4/7] Tests";               python -m pytest tests -q
echo "[5/7] Lag analysis";        python src/analysis/lag_analysis.py
echo "[5/7] Drought events";      python src/analysis/drought_events.py
echo "[6/7] Forecast temporal";   python src/experiments/run_forecast.py --split temporal
echo "[7/7] Forecast LOCO";       python src/experiments/run_forecast.py --split loco
echo "[8/8] Integrated system";   python src/system/run_system.py --train --date 2023-10-27 2026-09-01 2026-10-01 && python src/system/run_system.py
echo "DONE. See results/qc, results/lag, results/forecast"
