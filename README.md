# Satellite Module — Crop Stress Confirmation from Sentinel-2 (v2)

Stage 2 of the integrated drought assessment system:
**weather (predict) → satellite (confirm) → UAV (quantify)**.
The weather module forecasts *meteorological* drought (SPEI). This module measures whether
crops actually became stressed (*agricultural* drought), how long after the weather signal,
and whether weather information improves crop-stress forecasts.

> **v1 is withdrawn.** v1 used simulated Sentinel-2 values and rule-based labels for 40
> hand-picked random fields; its results are not valid and are not in this repository.

---

## Quick start

```bat
git clone --recursive https://github.com/ARYAN3012-G/Sentinel2-Drought-Confirmation.git
cd Sentinel2-Drought-Confirmation
run_all.bat          :: Windows   (bash run_all.sh on Linux / macOS / Git Bash)
```

The weather module ([weather_time_series](https://github.com/ARYAN3012-G/weather_time_series))
comes along as a git submodule in `external/weather_time_series`; step 0 fetches it if the
clone was made without `--recursive` and prepares its data (seconds). No PyTorch is needed.

| # | Command | What it does |
|---|---|---|
| 0 | `python src/dataprep/ensure_weather.py` | fetch + prepare the weather module (submodule) |
| 1 | `python src/dataprep/build_dataset.py` | clean Sentinel-2 series, 5-day grid, VCI labels, QC report |
| 2 | `python src/dataprep/weather_link.py` | SPEI-30/60/90 and weather on the same 5-day grid |
| 3 | `python src/dataprep/weather_forecasts.py` | weather-module forecasts (t+7/15/30) for every satellite date |
| 4 | `python -m pytest tests -q` | 12 integrity / leakage tests |
| 5 | `python src/analysis/lag_analysis.py` | weather drought → crop stress: lags, alarm confirmation, seasonal SVI |
| 6 | `python src/experiments/run_forecast.py` | 15/30-day crop-condition forecasts: 4 versions, baselines, onsets, CIs |

---

## 1. Where the fields come from (no hand-picking)

No surveyed field boundaries exist, so farmland is found automatically in Google Earth Engine
(`src/gee/script_A_cropland_fields.js`):

1. 3 km circle around each of the 8 study areas; overlapping circles split by nearest centre.
2. Cropland in ESA WorldCover 2020 or 2021 (Zanaga et al.).
3. Removed if Dynamic World (Brown et al. 2022) calls it built-up in any year 2019-2025,
   trees in > 3 years or water in > 1 year.
4. Kept only if Sentinel-2 NDVI shows a crop cycle in at least 2 of 7 years (deliberately not
   "most years", so fields that failed in drought years are not removed).
5. Edge pixels removed; pixels green in summer (Mar-May) in ≥ 3 years marked *likely irrigated*.
6. Farmland split into field-sized segments with SNIC (Achanta & Süsstrunk 2017), 0.3-10 ha.
7. Random sample with a fixed seed: 20 rainfed + 10 irrigated segments per site = **240 fields**.

| Site | Farmland | Rainfed | Irrigated | Segments |
|---|---|---|---|---|
| Somandepalle | 1,164 ha | 917 | 248 | 1,733 |
| Lepakshi | 1,628 ha | 1,059 | 570 | 2,400 |
| Cholasamudram | 1,756 ha | 1,221 | 535 | 2,620 |
| Sira | 1,568 ha | 1,256 | 312 | 2,323 |
| Peddakadubur | 1,850 ha | 1,504 | 346 | 2,782 |
| Kurnool Dinnedevarapadu | 284 ha | 218 | 66 | 418 |
| Kurnool Balaji Villas | 218 ha | 171 | 48 | 326 |
| Kurnool Pullaiah | 1,000 ha | 477 | 522 | 1,476 |

## 2. Satellite data

`src/gee/script_B_timeseries.js`: Sentinel-2 SR Harmonized, 2019 – Oct 2026, cloud/shadow
masked with Cloud Score+ (≥ 0.6) and the SCL layer. Exports per field and date: mean B2-B12
reflectance, NDVI, NDMI, EVI, clear-pixel count; plus NDVI/NDMI of the whole farmland area of
each site (rainfed and irrigated separately).

Cleaning (`src/dataprep/`): observation kept if ≥ 60 % of the field's pixels are clear;
same-day tile duplicates merged; isolated NDVI spikes removed; regular 5-day grid.
Two versions of every series:
- **interp** (linear, gaps ≤ 30 days) — used only for labels;
- **causal** (last observation carried forward, ≤ 30 days old) — the only version used as model input.

## 3. Labels: Standardized Vegetation Index (SVI)

SVI = (NDVI − reference mean) / reference spread (Peters et al. 2002), per field and day of year
(mean ±15 days, spread ±30 days). The reference comes **only from training years 2019-2023**
and **never from the year being labelled** — the satellite equivalent of the weather module's
frozen SPEI calibration. Classes use the **same thresholds as SPEI** in the weather module:
Healthy ≥ 0 · Moderate −1.5 to 0 · Severe < −1.5. Dates with no normal crop signal
(reference max NDVI < 0.35 or range < 0.10) are unlabelled.

Why not VCI (Kogan 1995)? Its min/max envelope needs a long record; with 4-5 reference years
about 20 % of all dates fall below every reference year by chance and get VCI ≈ 0 ("severe").
VCI is still computed and used as an input.

## 4. Link to the weather module

Each site uses its weather series (Lepakshi → Cholasamudram's ERA5-Land cell). SPEI-30/60/90
are recomputed with the weather module's calibrator (log-logistic, 1979-2011, frozen).
- **Lag analysis**: correlation of VCI(t) with SPEI-k(t − lag), lag 0-90 days.
- **Alarm confirmation**: after SPEI-30 falls below −1, how often does rainfed farmland reach
  SVI < −1 within 60 days, compared with the base rate for any date?
- **Weather-module forecasts as input**: the weather module's best model (weather_spei_doy,
  XGBoost, trained 1979-2011) forecasts the SPEI class at t+7/15/30 for every date from 2019;
  these reproduce its published test scores (macro-F1 0.765 / 0.632 / 0.436).
- **Forecasting**: SVI class 15 / 30 days ahead, four versions on identical samples:
  1 satellite history · 2 + past weather · 3 + weather-module forecast (the integrated system) ·
  4 + actual future weather (upper bound = perfect weather forecast) · reference weather only.
  RF and XGBoost, 5 seeds, persistence / climatology / majority baselines, purged chronological
  split (TRAIN 2019-23 / VAL 2024 / TEST 2025-26), leave-one-cluster-out (Kurnool vs south),
  block-bootstrap 95 % CIs, and **onset** scores (fields healthy at t that drop below normal by
  t+h), which persistence cannot predict by definition.

Note: weather data end in June 2026, so samples needing later weather are not used.

## Outputs

| Path | Content |
|---|---|
| `results/qc/QC_REPORT.md` | observations kept per site, label shares by period / year / site |
| `results/lag/LAG_REPORT.md` | lag correlations, alarm confirmation, seasonal SVI per year |
| `results/forecast/REPORT_temporal.md`, `REPORT_loco.md` | forecast results with CIs |

## Structure

```
external/weather_time_series/  weather module (git submodule)
src/gee/                   Earth Engine scripts A (farmland + segments) and B (time series)
src/gee/upload/            sampled_fields.zip (240 fields, uploaded as an Earth Engine asset)
data/gee_exports/          files exported from Earth Engine (raw data of this module)
data/polygons/             study-area centres, drone photo positions
src/config.py              all settings
src/dataprep/              cleaning, SVI/VCI labels, weather link, weather-module forecasts
src/analysis/              lag analysis
src/experiments/           forecasting
tools/drone_gps_to_kml.py  drone photo GPS -> Google Earth (for the UAV stage)
tests/                     leakage / integrity tests
```

## References

- Peters et al. (2002). Drought monitoring with NDVI-based Standardized Vegetation Index. *PE&RS* 68(1), 71-75.
- Kogan (1995). Application of vegetation index and brightness temperature for drought detection. *Adv. Space Res.* 15(11), 91-100.
- Brown et al. (2022). Dynamic World, near real-time global 10 m land use land cover mapping. *Scientific Data* 9, 251.
- Zanaga et al. (2021, 2022). ESA WorldCover 10 m v100 / v200.
- Achanta & Süsstrunk (2017). Superpixels and polygons using simple non-iterative clustering. *CVPR*.
- Pasquarella et al. (2023). Cloud Score+: comprehensive cloud and cloud-shadow masking for Sentinel-2. *CVPR Workshops*.
- Vicente-Serrano et al. (2010). SPEI. *J. Climate* 23, 1696-1718.
