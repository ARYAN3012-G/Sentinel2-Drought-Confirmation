# Drought system report - 2023-10-27

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -2.2400 | -2.2300 | True | True | 12 | -1.4200 | 83% | True | True | DROUGHT: alarm confirmed by crops |
| Lep | -2.1300 | -2.5200 | True | True | 5 | -1.0900 | 60% | True | True | DROUGHT: alarm confirmed by crops |
| Cho | -2.1300 | -2.5200 | True | True | 4 | -2.8900 | 75% | False | False | WEATHER ALARM, satellite data insufficient (cannot confirm) |
| Sira | -2.1700 | -2.2600 | True | True | 20 | -2.4300 | 80% | True | True | DROUGHT: alarm confirmed by crops |
| Ped | -2.5200 | -1.9100 | True | True | 22 | -0.7000 | 36% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Din | -2.3700 | -1.8500 | True | True | 20 | -1.7100 | 85% | True | True | DROUGHT: alarm confirmed by crops |
| Bal | -2.0300 | -1.5900 | True | True | 19 | -1.1700 | 58% | True | True | DROUGHT: alarm confirmed by crops |
| Pul | -2.0300 | -1.5900 | True | True | 14 | -0.6400 | 36% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2023-10-27 | -2.2400 | -2.2300 | Severe (93%), issued 2023-10-27 | Severe (55%), issued 2023-10-27 | Healthy (52%), issued 2023-10-27 | True | True |
| Lep | 2023-10-27 | -2.1300 | -2.5200 | Severe (86%), issued 2023-10-27 | Severe (62%), issued 2023-10-27 | Healthy (50%), issued 2023-10-27 | True | True |
| Cho | 2023-10-27 | -2.1300 | -2.5200 | Severe (86%), issued 2023-10-27 | Severe (62%), issued 2023-10-27 | Healthy (50%), issued 2023-10-27 | True | True |
| Sira | 2023-10-27 | -2.1700 | -2.2600 | Severe (93%), issued 2023-10-27 | Severe (60%), issued 2023-10-27 | Healthy (38%), issued 2023-10-27 | True | True |
| Ped | 2023-10-27 | -2.5200 | -1.9100 | Severe (98%), issued 2023-10-27 | Severe (81%), issued 2023-10-27 | Moderate (52%), issued 2023-10-27 | True | True |
| Din | 2023-10-27 | -2.3700 | -1.8500 | Severe (97%), issued 2023-10-27 | Severe (86%), issued 2023-10-27 | Moderate (64%), issued 2023-10-27 | True | True |
| Bal | 2023-10-27 | -2.0300 | -1.5900 | Severe (97%), issued 2023-10-27 | Severe (84%), issued 2023-10-27 | Moderate (54%), issued 2023-10-27 | True | True |
| Pul | 2023-10-27 | -2.0300 | -1.5900 | Severe (97%), issued 2023-10-27 | Severe (84%), issued 2023-10-27 | Moderate (54%), issued 2023-10-27 | True | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 12 | 2.0000 | -1.4200 | 83% | 42% | True | True |
| Lep | 5 | 2.0000 | -1.0900 | 60% | 40% | True | True |
| Cho | 4 | 2.0000 | -2.8900 | 75% | 75% | False | False |
| Sira | 20 | 4.0000 | -2.4300 | 80% | 65% | True | True |
| Ped | 22 | 9.0000 | -0.7000 | 36% | 23% | True | False |
| Din | 20 | 2.0000 | -1.7100 | 85% | 60% | True | True |
| Bal | 19 | 2.0000 | -1.1700 | 58% | 26% | True | True |
| Pul | 14 | 2.0000 | -0.6400 | 36% | 14% | True | False |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

At-risk ranking skipped: 2023 is inside the crop model's training years (2019-2024), so its predictions would be in-sample.

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Som | stressed now (satellite candidate) | 1 | Som_362814257_52 | 14.0324 | 77.6027 | 0.5200 | 0 | -2.9700 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (55%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 2 | Som_-1784866033_71 | 13.9855 | 77.5949 | 0.7100 | 0 | -2.5500 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (55%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 3 | Som_883794299_121 | 14.0020 | 77.5942 | 1.2100 | 0 | -2.3700 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (55%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 4 | Som_920238639_59 | 13.9967 | 77.5949 | 0.5900 | 0 | -2.2100 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (55%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 5 | Som_1087396711_50 | 14.0208 | 77.6019 | 0.5000 | 0 | -1.8600 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (55%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 1 | Lep_-850369929_83 | 13.7845 | 77.6348 | 0.8300 | 0 | -1.8200 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (62%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 2 | Lep_-1567128699_67 | 13.8005 | 77.5964 | 0.6700 | 0 | -1.7800 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (62%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 3 | Lep_1847530424_30 | 13.8248 | 77.6293 | 0.3000 | 0 | -1.0900 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (62%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 1 | Cho_-1848777060_91 | 13.7943 | 77.5832 | 0.9100 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (62%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 2 | Cho_760920043_54 | 13.8166 | 77.5869 | 0.5400 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (62%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 3 | Cho_-252629698_73 | 13.7891 | 77.5816 | 0.7300 | 0 | -1.7800 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (62%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_-557626191_38 | 13.8095 | 76.9553 | 0.3800 | 0 | -4.0000 | 4.0000 |  | 2023-10-27 | 2023-10-27 | Severe (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 2 | Sira_-477568747_46 | 13.7990 | 76.9788 | 0.4600 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 3 | Sira_-33407465_52 | 13.7950 | 76.9700 | 0.5200 | 0 | -4.0000 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 4 | Sira_-2138012297_94 | 13.7957 | 76.9561 | 0.9400 | 0 | -4.0000 | 14.0000 |  | 2023-10-27 | 2023-10-27 | Severe (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 5 | Sira_2018929124_87 | 13.7848 | 76.9683 | 0.8700 | 0 | -3.5300 | 4.0000 |  | 2023-10-27 | 2023-10-27 | Severe (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_300215151_73 | 15.7617 | 77.2401 | 0.7300 | 0 | -4.0000 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (81%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 2 | Ped_-1000886989_32 | 15.8019 | 77.2414 | 0.3200 | 0 | -3.1000 | 4.0000 |  | 2023-10-27 | 2023-10-27 | Severe (81%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 3 | Ped_1411335133_54 | 15.7921 | 77.2412 | 0.5400 | 0 | -2.1300 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (81%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 4 | Ped_-509492233_82 | 15.7890 | 77.2314 | 0.8200 | 0 | -1.9100 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (81%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 5 | Ped_56712922_61 | 15.7989 | 77.2636 | 0.6100 | 0 | -1.8400 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (81%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 1 | Din_1028714085_104 | 15.7771 | 78.0349 | 1.0400 | 0 | -3.5900 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (86%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 2 | Din_349003720_75 | 15.7814 | 78.0395 | 0.7500 | 0 | -3.4600 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (86%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 3 | Din_-272741483_63 | 15.7711 | 78.0475 | 0.6300 | 0 | -3.1300 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (86%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 4 | Din_642593467_91 | 15.7718 | 78.0482 | 0.9100 | 0 | -3.0400 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (86%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 5 | Din_2049257924_64 | 15.7728 | 78.0336 | 0.6400 | 0 | -2.7100 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (86%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 1 | Bal_-915454758_79 | 15.7848 | 78.0461 | 0.7900 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 2 | Bal_1017553099_41 | 15.7850 | 78.0506 | 0.4100 | 0 | -3.3300 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 3 | Bal_1108221314_76 | 15.7685 | 78.0780 | 0.7600 | 0 | -2.6300 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 4 | Bal_-1059541894_63 | 15.7832 | 78.0634 | 0.6300 | 0 | -2.1100 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 5 | Bal_-1597424154_74 | 15.7722 | 78.0750 | 0.7400 | 0 | -1.8700 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_228577482_69 | 15.7859 | 78.0723 | 0.6900 | 0 | -2.7900 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 2 | Pul_1137120678_44 | 15.8046 | 78.0862 | 0.4400 | 0 | -2.3100 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 3 | Pul_331786056_66 | 15.7868 | 78.0753 | 0.6600 | 0 | -1.1700 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 4 | Pul_-1864386639_99 | 15.8038 | 78.0892 | 0.9900 | 0 | -1.1100 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 5 | Pul_50838742_97 | 15.7868 | 78.0791 | 0.9700 | 0 | -1.0400 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
