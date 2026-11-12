# Drought system report - 2026-10-01

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -2.1400 | -2.1800 | True | True | 4 | -1.8500 | 75% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Lep | -1.9900 | -2.3400 | True | True | 10 | -0.6600 | 50% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Cho | -1.9900 | -2.3400 | True | True | 9 | -2.4900 | 78% | True | True | DROUGHT: alarm confirmed by crops |
| Sira | -1.7700 | -2.0600 | True | True | 22 | -1.8100 | 77% | True | True | DROUGHT: alarm confirmed by crops |
| Ped | -1.8000 | -2.0700 | True | True | 20 | -0.4100 | 20% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Din | -1.2100 | -1.7600 | True | True | 17 | -1.8900 | 82% | True | True | DROUGHT: alarm confirmed by crops |
| Bal | -0.5800 | -1.4700 | True | False | 19 | -1.1300 | 58% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Pul | -0.5800 | -1.4700 | True | False | 19 | -0.8400 | 37% | True | False | normal (observed) |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2026-10-01 | -2.1400 | -2.1800 | Moderate (50%), issued 2026-10-01 | Moderate (76%), issued 2026-10-01 | Moderate (54%), issued 2026-10-01 | True | True |
| Lep | 2026-10-01 | -1.9900 | -2.3400 | Moderate (69%), issued 2026-10-01 | Moderate (78%), issued 2026-10-01 | Moderate (53%), issued 2026-10-01 | True | True |
| Cho | 2026-10-01 | -1.9900 | -2.3400 | Moderate (69%), issued 2026-10-01 | Moderate (78%), issued 2026-10-01 | Moderate (53%), issued 2026-10-01 | True | True |
| Sira | 2026-10-01 | -1.7700 | -2.0600 | Moderate (85%), issued 2026-10-01 | Moderate (77%), issued 2026-10-01 | Moderate (45%), issued 2026-10-01 | True | True |
| Ped | 2026-10-01 | -1.8000 | -2.0700 | Moderate (83%), issued 2026-10-01 | Moderate (70%), issued 2026-10-01 | Moderate (42%), issued 2026-10-01 | True | True |
| Din | 2026-10-01 | -1.2100 | -1.7600 | Moderate (91%), issued 2026-10-01 | Moderate (65%), issued 2026-10-01 | Moderate (51%), issued 2026-10-01 | True | True |
| Bal | 2026-10-01 | -0.5800 | -1.4700 | Moderate (81%), issued 2026-10-01 | Moderate (71%), issued 2026-10-01 | Moderate (47%), issued 2026-10-01 | True | False |
| Pul | 2026-10-01 | -0.5800 | -1.4700 | Moderate (81%), issued 2026-10-01 | Moderate (71%), issued 2026-10-01 | Moderate (47%), issued 2026-10-01 | True | False |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 4 | 9.5000 | -1.8500 | 75% | 50% | False | False |
| Lep | 10 | 2.0000 | -0.6600 | 50% | 40% | True | False |
| Cho | 9 | 2.0000 | -2.4900 | 78% | 67% | True | True |
| Sira | 22 | 4.0000 | -1.8100 | 77% | 59% | True | True |
| Ped | 20 | 4.0000 | -0.4100 | 20% | 10% | True | False |
| Din | 17 | 17.0000 | -1.8900 | 82% | 71% | True | True |
| Bal | 19 | 17.0000 | -1.1300 | 58% | 37% | True | True |
| Pul | 19 | 17.0000 | -0.8400 | 37% | 26% | True | False |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Som | stressed now (satellite candidate) | 1 | Som_-1542221172_63 | 13.9866 | 77.6259 | 0.6300 | 0 | -3.5100 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (76%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 2 | Som_480487923_115 | 13.9892 | 77.6247 | 1.1500 | 0 | -2.5800 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (76%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 3 | Som_1482689627_50 | 14.0087 | 77.6485 | 0.5000 | 0 | -1.1100 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (76%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 1 | Lep_-1245907324_61 | 13.7997 | 77.6202 | 0.6100 | 0 | -3.8400 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 2 | Lep_-875948390_67 | 13.7806 | 77.6332 | 0.6700 | 0 | -2.0600 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 3 | Lep_359137185_33 | 13.7773 | 77.6282 | 0.3300 | 0 | -2.0100 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 4 | Lep_453852489_66 | 13.8184 | 77.6227 | 0.6600 | 0 | -1.5500 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 5 | Lep_-1812797810_63 | 13.7933 | 77.6033 | 0.6300 | 0 | -1.0300 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | at risk (normal now) | 1 | Lep_1366978471_115 | 13.7921 | 77.6394 | 1.1500 | 0 | 0.0600 |  | 0.6600 | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | at risk (normal now) | 2 | Lep_575486404_51 | 13.7898 | 77.6363 | 0.5100 | 0 | 0.1000 |  | 0.6400 | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | at risk (normal now) | 3 | Lep_-393847897_93 | 13.7894 | 77.6325 | 0.9300 | 0 | 0.3600 |  | 0.5800 | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 1 | Cho_1817686041_52 | 13.8262 | 77.5737 | 0.5200 | 0 | -3.6000 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 2 | Cho_-1929682815_75 | 13.8219 | 77.5890 | 0.7500 | 0 | -3.2000 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 3 | Cho_-256237829_41 | 13.7926 | 77.5875 | 0.4100 | 0 | -2.9100 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 4 | Cho_-2044978701_39 | 13.7910 | 77.5690 | 0.3900 | 0 | -2.7800 | 22.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 5 | Cho_747050785_68 | 13.8093 | 77.5802 | 0.6800 | 0 | -2.4900 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (78%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_384305002_59 | 13.8013 | 76.9684 | 0.5900 | 0 | -3.4400 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (77%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 2 | Sira_-429783427_42 | 13.8001 | 76.9492 | 0.4200 | 0 | -3.1300 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (77%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 3 | Sira_-297557598_64 | 13.7738 | 76.9831 | 0.6400 | 0 | -2.7000 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (77%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 4 | Sira_73696548_81 | 13.7786 | 76.9926 | 0.8100 | 0 | -2.6900 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (77%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 5 | Sira_-854967134_68 | 13.8034 | 76.9954 | 0.6800 | 0 | -2.6500 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (77%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_1362413355_81 | 15.7970 | 77.2511 | 0.8100 | 0 | -3.4500 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 2 | Ped_-605429907_77 | 15.7909 | 77.2628 | 0.7700 | 0 | -1.6400 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 3 | Ped_-1766731421_34 | 15.7902 | 77.2761 | 0.3400 | 0 | -1.4800 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 4 | Ped_1870933361_43 | 15.7982 | 77.2575 | 0.4300 | 0 | -1.1700 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 1 | Ped_1438855646_93 | 15.7982 | 77.2488 | 0.9300 | 0 | 0.0200 |  | 0.8600 | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 2 | Ped_-889960087_38 | 15.7629 | 77.2693 | 0.3800 | 0 | 0.2800 |  | 0.6400 | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 3 | Ped_979873077_45 | 15.7878 | 77.2793 | 0.4500 | 0 | 0.3100 |  | 0.6100 | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 4 | Ped_1325521048_50 | 15.7716 | 77.2588 | 0.5000 | 0 | 0.7800 |  | 0.5900 | 2026-10-01 | 2026-10-01 | Moderate (70%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 1 | Din_1948219898_56 | 15.7763 | 78.0408 | 0.5600 | 0 | -2.4200 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (65%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 2 | Din_-965966673_90 | 15.7735 | 78.0335 | 0.9000 | 0 | -2.4000 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (65%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 3 | Din_948347010_42 | 15.7742 | 78.0497 | 0.4200 | 0 | -2.3900 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (65%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 4 | Din_447276050_76 | 15.7762 | 78.0378 | 0.7600 | 0 | -2.2900 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (65%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 5 | Din_886971862_71 | 15.7670 | 78.0510 | 0.7100 | 0 | -2.0300 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (65%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 1 | Bal_-552641801_47 | 15.7866 | 78.0395 | 0.4700 | 0 | -3.1600 | 22.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 2 | Bal_2097057505_52 | 15.7828 | 78.0468 | 0.5200 | 0 | -2.5900 | 22.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 3 | Bal_-1700098560_78 | 15.7848 | 78.0500 | 0.7800 | 0 | -1.9200 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 4 | Bal_-1067433852_104 | 15.7855 | 78.0679 | 1.0400 | 0 | -1.8400 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 5 | Bal_1631364936_58 | 15.7842 | 78.0484 | 0.5800 | 0 | -1.7000 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 1 | Bal_225116981_80 | 15.7874 | 78.0663 | 0.8000 | 0 | 0.1400 |  | 0.6100 | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 2 | Bal_1133162854_98 | 15.7673 | 78.0727 | 0.9800 | 0 | 0.9900 |  | 0.5000 | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 3 | Bal_-1142886139_38 | 15.7635 | 78.0738 | 0.3800 | 0 | 1.0200 |  | 0.5000 | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_-676507978_78 | 15.8158 | 78.0816 | 0.7800 | 0 | -4.0000 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 2 | Pul_1631148664_34 | 15.7997 | 78.0741 | 0.3400 | 0 | -1.7500 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 3 | Pul_-391022102_74 | 15.8129 | 78.0682 | 0.7400 | 0 | -1.6500 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 4 | Pul_391662750_74 | 15.8045 | 78.0899 | 0.7400 | 0 | -1.6000 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 5 | Pul_596494743_57 | 15.7984 | 78.0719 | 0.5700 | 0 | -1.5300 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 1 | Pul_1028490795_46 | 15.7734 | 78.0865 | 0.4600 | 0 | 0.3200 |  | 0.6000 | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 2 | Pul_1171905605_46 | 15.8054 | 78.0975 | 0.4600 | 0 | 0.9100 |  | 0.5800 | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
