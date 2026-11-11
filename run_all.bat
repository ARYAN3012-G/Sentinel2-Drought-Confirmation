@echo off
REM ==========================================================================
REM  Satellite module (stage 2) - full pipeline (Windows). Run from this folder.
REM  Clone with:  git clone --recursive https://github.com/ARYAN3012-G/Sentinel2-Drought-Confirmation.git
REM  (the weather module comes along as a git submodule)
REM ==========================================================================
setlocal
cd /d %~dp0
set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

echo [setup] Installing requirements
python -m pip install -r requirements.txt || goto :error
echo [0/7] Weather module (git submodule) and its prepared data
python src\dataprep\ensure_weather.py || goto :error
echo [1/7] Clean Sentinel-2 series + SVI labels
python src\dataprep\build_dataset.py || goto :error
echo [2/7] Weather link (SPEI-30/60/90 on the 5-day grid)
python src\dataprep\weather_link.py || goto :error
echo [3/7] Weather-module forecasts for every satellite date (XGBoost, a few minutes)
python src\dataprep\weather_forecasts.py || goto :error
echo [4/7] Integrity / leakage tests
python -m pytest tests -q || goto :error
echo [5/7] Lag analysis: weather drought -^> crop stress
python src\analysis\lag_analysis.py || goto :error
echo [5/7] Drought events 2023/2025/2026, irrigation label check, lag robustness
python src\analysis\drought_events.py || goto :error
echo [6/7] Forecast: temporal split
python src\experiments\run_forecast.py --split temporal || goto :error
echo [7/7] Forecast: leave-one-cluster-out
python src\experiments\run_forecast.py --split loco || goto :error
echo [8/8] Integrated system: train crop model, reports for 2023-10-27, 2026-09-01, 2026-10-01 and the latest date
python src\system\run_system.py --train --date 2023-10-27 2026-09-01 2026-10-01 || goto :error
python src\system\run_system.py || goto :error
echo.
echo DONE. See results\qc\QC_REPORT.md, results\lag\LAG_REPORT.md,
echo results\forecast\REPORT_temporal.md and REPORT_loco.md
goto :eof
:error
echo FAILED at the step above.
exit /b 1
