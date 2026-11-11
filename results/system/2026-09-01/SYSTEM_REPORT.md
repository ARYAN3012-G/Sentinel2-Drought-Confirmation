# Drought system report - 2026-09-01

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -1.3700 | -1.8800 | True | True | 5 | -1.1200 | 60% | True | True | DROUGHT: alarm confirmed by crops |
| Lep | -1.1400 | -1.7000 | True | True | 1 | 0.0100 | 0% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Cho | -1.1400 | -1.7000 | True | True | 3 | -0.7300 | 33% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Sira | -1.0900 | -1.3900 | True | True | 1 | -1.8600 | 100% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Ped | -1.4000 | -1.6700 | True | True | 4 | 0.4300 | 25% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Din | -1.1200 | -1.3500 | True | True | 1 | 0.3300 | 0% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Bal | -1.0600 | -1.3300 | True | True | 0 |  |  | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Pul | -1.0600 | -1.3300 | True | True | 4 | -0.5700 | 50% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2026-09-01 | -1.3700 | -1.8800 | Severe (50%), issued 2026-09-01 | Moderate (66%), issued 2026-09-01 | Moderate (52%), issued 2026-09-01 | True | True |
| Lep | 2026-09-01 | -1.1400 | -1.7000 | Severe (53%), issued 2026-09-01 | Moderate (78%), issued 2026-09-01 | Moderate (61%), issued 2026-09-01 | True | True |
| Cho | 2026-09-01 | -1.1400 | -1.7000 | Severe (53%), issued 2026-09-01 | Moderate (78%), issued 2026-09-01 | Moderate (61%), issued 2026-09-01 | True | True |
| Sira | 2026-09-01 | -1.0900 | -1.3900 | Moderate (79%), issued 2026-09-01 | Moderate (89%), issued 2026-09-01 | Moderate (60%), issued 2026-09-01 | True | True |
| Ped | 2026-09-01 | -1.4000 | -1.6700 | Severe (77%), issued 2026-09-01 | Moderate (66%), issued 2026-09-01 | Moderate (56%), issued 2026-09-01 | True | True |
| Din | 2026-09-01 | -1.1200 | -1.3500 | Severe (64%), issued 2026-09-01 | Moderate (70%), issued 2026-09-01 | Moderate (46%), issued 2026-09-01 | True | True |
| Bal | 2026-09-01 | -1.0600 | -1.3300 | Moderate (50%), issued 2026-09-01 | Moderate (67%), issued 2026-09-01 | Moderate (46%), issued 2026-09-01 | True | True |
| Pul | 2026-09-01 | -1.0600 | -1.3300 | Moderate (50%), issued 2026-09-01 | Moderate (67%), issued 2026-09-01 | Moderate (46%), issued 2026-09-01 | True | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 5 | 22.0000 | -1.1200 | 60% | 40% | True | True |
| Lep | 1 | 22.0000 | 0.0100 | 0% | 0% | False | False |
| Cho | 3 | 22.0000 | -0.7300 | 33% | 0% | False | False |
| Sira | 1 | 2.0000 | -1.8600 | 100% | 100% | False | False |
| Ped | 4 | 4.0000 | 0.4300 | 25% | 25% | False | False |
| Din | 1 | 12.0000 | 0.3300 | 0% | 0% | False | False |
| Bal | 0 |  |  |  |  | False | False |
| Pul | 4 | 12.0000 | -0.5700 | 50% | 25% | False | False |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Som | stressed now (satellite candidate) | 1 | Som_210526987_57 | 14.0015 | 77.6010 | 0.5700 | 0 | -1.7300 | 22.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (66%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 2 | Som_2097648969_50 | 14.0233 | 77.6040 | 0.5000 | 0 | -1.6800 | 22.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (66%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 3 | Som_1700228554_34 | 14.0118 | 77.5916 | 0.3400 | 0 | -1.1200 | 22.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (66%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | at risk (normal now) | 1 | Lep_-171177260_37 | 13.8125 | 77.6181 | 0.3700 | 0 | 0.0100 |  | 0.7400 | 2026-09-01 | 2026-09-01 | Moderate (78%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 1 | Cho_1817686041_58 | 13.8262 | 77.5735 | 0.5800 | 0 | -1.2300 | 22.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (78%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_1795621425_56 | 13.7737 | 76.9868 | 0.5600 | 0 | -1.8600 | 2.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (89%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_-430971332_39 | 15.8054 | 77.2495 | 0.3900 | 0 | -1.6900 | 4.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (66%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 1 | Ped_-1473159057_38 | 15.7563 | 77.2550 | 0.3800 | 0 | 1.3600 |  | 0.5000 | 2026-09-01 | 2026-09-01 | Moderate (66%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | at risk (normal now) | 1 | Din_-1012988290_83 | 15.7492 | 78.0592 | 0.8300 | 0 | 0.3300 |  | 0.5700 | 2026-09-01 | 2026-09-01 | Moderate (70%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_-1093009035_51 | 15.7787 | 78.0991 | 0.5100 | 0 | -2.3000 | 12.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (67%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 2 | Pul_-1723364789_65 | 15.7850 | 78.0875 | 0.6500 | 0 | -1.1700 | 12.0000 |  | 2026-09-01 | 2026-09-01 | Moderate (67%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 1 | Pul_-2111834955_52 | 15.7738 | 78.0837 | 0.5200 | 0 | 0.0300 |  | 0.8100 | 2026-09-01 | 2026-09-01 | Moderate (67%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 2 | Pul_1878893000_41 | 15.7791 | 78.0999 | 0.4100 | 0 | 0.0800 |  | 0.5100 | 2026-09-01 | 2026-09-01 | Moderate (67%), issued 2026-09-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
