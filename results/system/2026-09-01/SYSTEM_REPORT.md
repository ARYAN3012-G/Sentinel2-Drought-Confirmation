# Drought system report - 2026-09-01

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -1.3700 | -1.8800 | True | True | 0 |  |  | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Lep | -1.1400 | -1.7000 | True | True | 0 |  |  | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Cho | -1.1400 | -1.7000 | True | True | 2 | -1.3300 | 50% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Sira | -1.0900 | -1.3900 | True | True | 1 | -3.3600 | 100% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Ped | -1.4000 | -1.6700 | True | True | 3 | 0.5400 | 33% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Din | -1.1200 | -1.3500 | True | True | 0 |  |  | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Bal | -1.0600 | -1.3300 | True | True | 0 |  |  | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Pul | -1.0600 | -1.3300 | True | True | 4 | -0.9000 | 25% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2026-09-01 | -1.3700 | -1.8800 | Severe (73%), issued 2026-09-01 | Moderate (62%), issued 2026-09-01 | Moderate (45%), issued 2026-09-01 | True | True |
| Lep | 2026-09-01 | -1.1400 | -1.7000 | Severe (81%), issued 2026-09-01 | Moderate (60%), issued 2026-09-01 | Moderate (45%), issued 2026-09-01 | True | True |
| Cho | 2026-09-01 | -1.1400 | -1.7000 | Severe (81%), issued 2026-09-01 | Moderate (60%), issued 2026-09-01 | Moderate (45%), issued 2026-09-01 | True | True |
| Sira | 2026-09-01 | -1.0900 | -1.3900 | Moderate (96%), issued 2026-09-01 | Moderate (92%), issued 2026-09-01 | Moderate (49%), issued 2026-09-01 | True | True |
| Ped | 2026-09-01 | -1.4000 | -1.6700 | Severe (91%), issued 2026-09-01 | Moderate (50%), issued 2026-09-01 | Moderate (52%), issued 2026-09-01 | True | True |
| Din | 2026-09-01 | -1.1200 | -1.3500 | Severe (83%), issued 2026-09-01 | Moderate (53%), issued 2026-09-01 | Moderate (43%), issued 2026-09-01 | True | True |
| Bal | 2026-09-01 | -1.0600 | -1.3300 | Severe (69%), issued 2026-09-01 | Moderate (52%), issued 2026-09-01 | Moderate (54%), issued 2026-09-01 | True | True |
| Pul | 2026-09-01 | -1.0600 | -1.3300 | Severe (69%), issued 2026-09-01 | Moderate (52%), issued 2026-09-01 | Moderate (54%), issued 2026-09-01 | True | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 0 |  |  |  |  | False | False |
| Lep | 0 |  |  |  |  | False | False |
| Cho | 2 | 22.0000 | -1.3300 | 50% | 50% | False | False |
| Sira | 1 | 2.0000 | -3.3600 | 100% | 100% | False | False |
| Ped | 3 | 4.0000 | 0.5400 | 33% | 33% | False | False |
| Din | 0 |  |  |  |  | False | False |
| Bal | 0 |  |  |  |  | False | False |
| Pul | 4 | 14.5000 | -0.9000 | 25% | 25% | False | False |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cho | stressed now (satellite candidate) | 1 | Cho_1817686041_52 | 13.8262 | 77.5737 | 0.5200 | 0 | -2.3400 | 22.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (60%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_-297557598_64 | 13.7738 | 76.9831 | 0.6400 | 0 | -3.3600 | 2.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (92%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_1870933361_43 | 15.7982 | 77.2575 | 0.4300 | 0 | -2.1000 | 4.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (50%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 1 | Ped_1353360778_72 | 15.7761 | 77.2795 | 0.7200 | 0 | 0.5400 |  | 0.6900 | 2026-09-01 | 2026-09-01 | Moderate (50%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_-831687081_86 | 15.7869 | 78.1027 | 0.8600 | 0 | -1.8000 | 17.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (52%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
