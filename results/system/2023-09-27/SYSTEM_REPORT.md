# Drought system report - 2023-09-27

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | ALARM | median_SVI | fields_below_normal | CONFIRMED | status |
|---|---|---|---|---|---|---|---|
| Som | -1.0600 | -0.0700 | True | -2.1500 | 100% | True | DROUGHT: alarm confirmed by crops |
| Lep | -1.0200 | 0.0800 | True | -2.5500 | 100% | True | DROUGHT: alarm confirmed by crops |
| Cho | -1.0200 | 0.0800 | True | -1.8600 | 100% | True | DROUGHT: alarm confirmed by crops |
| Sira | -0.7600 | 0.3100 | False | -0.7000 | 38% | False | normal |
| Ped | -0.0200 | 1.2500 | False | -0.3200 | 41% | False | normal |
| Din | 0.2700 | 1.2600 | False | -0.7000 | 41% | False | normal |
| Bal | 0.6000 | 1.1700 | False | -0.6700 | 38% | False | normal |
| Pul | 0.3300 | 0.9400 | False | -0.5200 | 33% | False | normal |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | ALARM |
|---|---|---|---|---|---|---|---|
| Som | 2023-09-27 | -1.0600 | -0.0700 | Moderate (87%) | Moderate (73%) | Moderate (54%) | True |
| Lep | 2023-09-27 | -1.0200 | 0.0800 | Moderate (86%) | Moderate (76%) | Moderate (58%) | True |
| Cho | 2023-09-27 | -1.0200 | 0.0800 | Moderate (86%) | Moderate (76%) | Moderate (58%) | True |
| Sira | 2023-09-27 | -0.7600 | 0.3100 | Moderate (97%) | Moderate (70%) | Moderate (56%) | False |
| Ped | 2023-09-27 | -0.0200 | 1.2500 | Moderate (86%) | Moderate (70%) | Moderate (54%) | False |
| Din | 2023-09-27 | 0.2700 | 1.2600 | Moderate (66%) | Moderate (61%) | Moderate (40%) | False |
| Bal | 2023-09-27 | 0.6000 | 1.1700 | Healthy (84%) | Healthy (67%) | Moderate (48%) | False |
| Pul | 2023-09-27 | 0.3300 | 0.9400 | Healthy (61%) | Healthy (60%) | Moderate (51%) | False |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_SVI | fields_below_normal | fields_severe | CONFIRMED |
|---|---|---|---|---|---|
| Som | 2 | -2.1500 | 100% | 100% | True |
| Lep | 2 | -2.5500 | 100% | 50% | True |
| Cho | 2 | -1.8600 | 100% | 50% | True |
| Sira | 16 | -0.7000 | 38% | 25% | False |
| Ped | 17 | -0.3200 | 41% | 24% | False |
| Din | 17 | -0.7000 | 41% | 29% | False |
| Bal | 16 | -0.6700 | 38% | 25% | False |
| Pul | 12 | -0.5200 | 33% | 25% | False |

CONFIRMED = median rainfed SVI < -1.

## Stage 3: fields to fly

Up to 5 fields per site and list. Map: `fields_to_fly.kml` (open in Google Earth; red = damaged now, orange = at risk). Table: `fields_to_fly.csv`.

At-risk ranking skipped: 2023 is inside the crop model's training years (2019-2024), so its predictions would be in-sample.

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | onset_risk_15d |
|---|---|---|---|---|---|---|---|---|---|
| Som | damaged now | 1 | Som_362814257_52 | 14.0324 | 77.6027 | 0.5200 | 0 | -2.7500 |  |
| Som | damaged now | 2 | Som_1700228554_34 | 14.0118 | 77.5916 | 0.3400 | 0 | -1.5500 |  |
| Lep | damaged now | 1 | Lep_-1716647714_53 | 13.8026 | 77.6180 | 0.5300 | 1 | -4.0000 |  |
| Lep | damaged now | 2 | Lep_459778305_53 | 13.8110 | 77.6425 | 0.5300 | 0 | -3.9400 |  |
| Lep | damaged now | 3 | Lep_-1567128699_67 | 13.8006 | 77.5964 | 0.6700 | 0 | -1.1600 |  |
| Cho | damaged now | 1 | Cho_-592418679_91 | 13.8373 | 77.5676 | 0.9100 | 0 | -2.4500 |  |
| Cho | damaged now | 2 | Cho_1004943644_42 | 13.8133 | 77.5427 | 0.4200 | 1 | -1.9800 |  |
| Cho | damaged now | 3 | Cho_-552009438_44 | 13.8297 | 77.5598 | 0.4400 | 1 | -1.5500 |  |
| Cho | damaged now | 4 | Cho_-1692411977_102 | 13.8256 | 77.5870 | 1.0200 | 0 | -1.2700 |  |
| Sira | damaged now | 1 | Sira_2018929124_87 | 13.7849 | 76.9682 | 0.8700 | 0 | -2.3500 |  |
| Sira | damaged now | 2 | Sira_-760834575_47 | 13.7779 | 76.9876 | 0.4700 | 0 | -2.0600 |  |
| Sira | damaged now | 3 | Sira_-33407465_52 | 13.7950 | 76.9700 | 0.5200 | 0 | -1.6000 |  |
| Sira | damaged now | 4 | Sira_157775990_72 | 13.7817 | 76.9793 | 0.7200 | 0 | -1.5300 |  |
| Sira | damaged now | 5 | Sira_-1344237192_63 | 13.8021 | 76.9669 | 0.6300 | 0 | -1.1100 |  |
| Ped | damaged now | 1 | Ped_-687601348_57 | 15.7605 | 77.2635 | 0.5700 | 0 | -2.9300 |  |
| Ped | damaged now | 2 | Ped_2054992808_58 | 15.7638 | 77.2440 | 0.5800 | 1 | -2.4900 |  |
| Ped | damaged now | 3 | Ped_-509492233_82 | 15.7890 | 77.2313 | 0.8200 | 0 | -1.7700 |  |
| Ped | damaged now | 4 | Ped_300215151_73 | 15.7616 | 77.2401 | 0.7300 | 0 | -1.7700 |  |
| Ped | damaged now | 5 | Ped_-608278541_33 | 15.7668 | 77.2429 | 0.3300 | 1 | -1.5700 |  |
| Din | damaged now | 1 | Din_929501593_81 | 15.7850 | 78.0380 | 0.8100 | 0 | -2.9600 |  |
| Din | damaged now | 2 | Din_4358011_38 | 15.7773 | 78.0356 | 0.3800 | 0 | -2.4700 |  |
| Din | damaged now | 3 | Din_1028714085_104 | 15.7771 | 78.0348 | 1.0400 | 0 | -2.3900 |  |
| Din | damaged now | 4 | Din_894904914_53 | 15.7857 | 78.0388 | 0.5300 | 0 | -1.8700 |  |
| Din | damaged now | 5 | Din_-272741483_63 | 15.7711 | 78.0475 | 0.6300 | 0 | -1.6300 |  |
| Bal | damaged now | 1 | Bal_-820752182_61 | 15.7661 | 78.0746 | 0.6100 | 1 | -4.0000 |  |
| Bal | damaged now | 2 | Bal_85063551_54 | 15.7639 | 78.0750 | 0.5400 | 1 | -2.5100 |  |
| Bal | damaged now | 3 | Bal_246590930_48 | 15.7846 | 78.0665 | 0.4800 | 0 | -1.8900 |  |
| Bal | damaged now | 4 | Bal_-915454758_79 | 15.7847 | 78.0460 | 0.7900 | 0 | -1.8300 |  |
| Bal | damaged now | 5 | Bal_1880226631_36 | 15.7869 | 78.0478 | 0.3600 | 0 | -1.6900 |  |
| Pul | damaged now | 1 | Pul_94858241_37 | 15.7765 | 78.0924 | 0.3700 | 1 | -3.1300 |  |
| Pul | damaged now | 2 | Pul_1137120678_44 | 15.8046 | 78.0862 | 0.4400 | 0 | -1.8000 |  |
| Pul | damaged now | 3 | Pul_1878893000_41 | 15.7790 | 78.0999 | 0.4100 | 0 | -1.7300 |  |
| Pul | damaged now | 4 | Pul_-684475182_101 | 15.7971 | 78.0964 | 1.0100 | 1 | -1.5900 |  |
| Pul | damaged now | 5 | Pul_693464584_75 | 15.7853 | 78.0725 | 0.7500 | 0 | -1.5700 |  |
