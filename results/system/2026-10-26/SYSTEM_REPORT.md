# Drought system report - 2026-10-26

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -0.8500 | -1.7900 | True | False | 19 | -2.2200 | 89% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Lep | -0.1700 | -1.5600 | True | False | 17 | -0.9900 | 47% | True | False | normal (observed) |
| Cho | -0.1700 | -1.5600 | True | False | 14 | -1.3600 | 64% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Sira | 0.3100 | -1.3700 | True | False | 23 | -1.3700 | 74% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Ped | -2.4600 | -2.3600 | True | True | 20 | -0.4100 | 10% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Din | -2.2600 | -2.1200 | True | True | 19 | -1.0500 | 53% | True | True | DROUGHT: alarm confirmed by crops |
| Bal | -2.0900 | -1.8500 | True | True | 21 | -0.9500 | 48% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Pul | -2.0900 | -1.8500 | True | True | 20 | -0.9500 | 50% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2026-10-26 | -0.8500 | -1.7900 | Moderate (74%), issued 2026-10-26 | Healthy (50%), issued 2026-10-26 | Moderate (46%), issued 2026-10-26 | True | False |
| Lep | 2026-10-26 | -0.1700 | -1.5600 | Healthy (59%), issued 2026-10-26 | Healthy (62%), issued 2026-10-26 | Moderate (38%), issued 2026-10-26 | True | False |
| Cho | 2026-10-26 | -0.1700 | -1.5600 | Healthy (59%), issued 2026-10-26 | Healthy (62%), issued 2026-10-26 | Moderate (38%), issued 2026-10-26 | True | False |
| Sira | 2026-10-26 | 0.3100 | -1.3700 | Healthy (100%), issued 2026-10-26 | Healthy (100%), issued 2026-10-26 | Moderate (56%), issued 2026-10-26 | True | False |
| Ped | 2026-10-26 | -2.4600 | -2.3600 | Severe (76%), issued 2026-10-26 | Moderate (76%), issued 2026-10-26 | Moderate (76%), issued 2026-10-26 | True | True |
| Din | 2026-10-26 | -2.2600 | -2.1200 | Severe (89%), issued 2026-10-26 | Moderate (66%), issued 2026-10-26 | Moderate (67%), issued 2026-10-26 | True | True |
| Bal | 2026-10-26 | -2.0900 | -1.8500 | Moderate (62%), issued 2026-10-26 | Moderate (55%), issued 2026-10-26 | Moderate (61%), issued 2026-10-26 | True | True |
| Pul | 2026-10-26 | -2.0900 | -1.8500 | Moderate (62%), issued 2026-10-26 | Moderate (55%), issued 2026-10-26 | Moderate (61%), issued 2026-10-26 | True | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 19 | 10.0000 | -2.2200 | 89% | 89% | True | True |
| Lep | 17 | 12.0000 | -0.9900 | 47% | 41% | True | False |
| Cho | 14 | 12.0000 | -1.3600 | 64% | 43% | True | True |
| Sira | 23 | 12.0000 | -1.3700 | 74% | 35% | True | True |
| Ped | 20 | 14.0000 | -0.4100 | 10% | 5% | True | False |
| Din | 19 | 7.0000 | -1.0500 | 53% | 16% | True | True |
| Bal | 21 | 7.0000 | -0.9500 | 48% | 24% | True | False |
| Pul | 20 | 7.0000 | -0.9500 | 50% | 20% | True | False |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Som | stressed now (satellite candidate) | 1 | Som_368139334_36 | 13.9828 | 77.6036 | 0.3600 | 0 | -4.0000 | 10.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (50%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 2 | Som_1954019573_71 | 13.9824 | 77.6294 | 0.7100 | 0 | -4.0000 | 10.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (50%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 3 | Som_723176683_114 | 14.0169 | 77.6372 | 1.1400 | 0 | -3.8200 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (50%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 4 | Som_35281328_83 | 14.0148 | 77.6425 | 0.8300 | 0 | -3.4800 | 10.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (50%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 5 | Som_1395702516_75 | 14.0131 | 77.6280 | 0.7500 | 0 | -2.8900 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (50%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 1 | Lep_1787383937_34 | 13.8011 | 77.6304 | 0.3400 | 0 | -4.0000 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 2 | Lep_1366978471_115 | 13.7921 | 77.6394 | 1.1500 | 0 | -4.0000 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 3 | Lep_-1245907324_61 | 13.7997 | 77.6202 | 0.6100 | 0 | -3.3500 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 4 | Lep_107279785_69 | 13.8102 | 77.6318 | 0.6900 | 0 | -2.1400 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 5 | Lep_-875948390_67 | 13.7806 | 77.6332 | 0.6700 | 0 | -2.0600 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | at risk (normal now) | 1 | Lep_-2104840171_73 | 13.7786 | 77.6119 | 0.7300 | 0 | 0.1200 |  | 0.6200 | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 1 | Cho_-256237829_41 | 13.7926 | 77.5875 | 0.4100 | 0 | -2.9400 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 2 | Cho_2091637640_84 | 13.8226 | 77.5618 | 0.8400 | 0 | -2.7700 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 3 | Cho_-1929682815_75 | 13.8219 | 77.5890 | 0.7500 | 0 | -2.5500 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 4 | Cho_747050785_68 | 13.8093 | 77.5802 | 0.6800 | 0 | -1.6700 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 5 | Cho_510176073_113 | 13.8216 | 77.5545 | 1.1300 | 0 | -1.6000 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_384305002_59 | 13.8013 | 76.9684 | 0.5900 | 0 | -2.5700 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (100%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 2 | Sira_-854967134_68 | 13.8034 | 76.9954 | 0.6800 | 0 | -2.4900 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (100%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 3 | Sira_-429783427_42 | 13.8001 | 76.9492 | 0.4200 | 0 | -2.3600 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (100%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 4 | Sira_73696548_81 | 13.7786 | 76.9926 | 0.8100 | 0 | -1.9900 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (100%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 5 | Sira_665615161_56 | 13.7788 | 76.9734 | 0.5600 | 0 | -1.9900 | 10.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (100%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | at risk (normal now) | 1 | Sira_1175395443_77 | 13.8203 | 76.9634 | 0.7700 | 0 | 0.0900 |  | 0.6600 | 2026-10-26 | 2026-10-26 | Healthy (100%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_-1766731421_34 | 15.7902 | 77.2761 | 0.3400 | 0 | -1.6300 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (76%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 2 | Ped_1438855646_93 | 15.7982 | 77.2488 | 0.9300 | 0 | -1.2500 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (76%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 1 | Ped_39074240_94 | 15.7868 | 77.2379 | 0.9400 | 0 | 0.1100 |  | 0.7800 | 2026-10-26 | 2026-10-26 | Moderate (76%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 2 | Ped_-1262508654_56 | 15.8026 | 77.2659 | 0.5600 | 0 | 0.4900 |  | 0.7700 | 2026-10-26 | 2026-10-26 | Moderate (76%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 3 | Ped_-298653457_90 | 15.8017 | 77.2383 | 0.9000 | 0 | 0.2200 |  | 0.7400 | 2026-10-26 | 2026-10-26 | Moderate (76%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 4 | Ped_1077002314_56 | 15.7976 | 77.2537 | 0.5600 | 0 | 0.5600 |  | 0.7100 | 2026-10-26 | 2026-10-26 | Moderate (76%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 5 | Ped_979873077_45 | 15.7878 | 77.2793 | 0.4500 | 0 | 0.2800 |  | 0.6600 | 2026-10-26 | 2026-10-26 | Moderate (76%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 1 | Din_447276050_76 | 15.7762 | 78.0378 | 0.7600 | 0 | -2.2100 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 2 | Din_1654695847_52 | 15.7808 | 78.0356 | 0.5200 | 0 | -2.0800 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 3 | Din_886971862_71 | 15.7670 | 78.0510 | 0.7100 | 0 | -1.6000 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 4 | Din_860056604_97 | 15.7623 | 78.0258 | 0.9700 | 0 | -1.5000 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 5 | Din_1948219898_56 | 15.7763 | 78.0408 | 0.5600 | 0 | -1.4900 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 1 | Bal_-552641801_47 | 15.7866 | 78.0395 | 0.4700 | 0 | -4.0000 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 2 | Bal_-884957212_73 | 15.7787 | 78.0744 | 0.7300 | 0 | -2.4900 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 3 | Bal_-1067433852_104 | 15.7855 | 78.0679 | 1.0400 | 0 | -2.3700 | 17.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 4 | Bal_1251611755_72 | 15.7881 | 78.0674 | 0.7200 | 0 | -2.1700 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 5 | Bal_-2042269998_34 | 15.7853 | 78.0657 | 0.3400 | 0 | -1.6600 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_-676507978_78 | 15.8158 | 78.0816 | 0.7800 | 0 | -2.3200 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 2 | Pul_596494743_57 | 15.7984 | 78.0719 | 0.5700 | 0 | -1.9200 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 3 | Pul_-1645792705_69 | 15.8025 | 78.0881 | 0.6900 | 0 | -1.7900 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 4 | Pul_1631148664_34 | 15.7997 | 78.0741 | 0.3400 | 0 | -1.6500 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 5 | Pul_-1341461071_99 | 15.7824 | 78.0776 | 0.9900 | 0 | -1.2800 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 1 | Pul_718805493_50 | 15.7839 | 78.0804 | 0.5000 | 0 | 0.6800 |  | 0.7800 | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 2 | Pul_1171905605_46 | 15.8054 | 78.0975 | 0.4600 | 0 | 0.4200 |  | 0.6700 | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 3 | Pul_509973208_86 | 15.8239 | 78.0802 | 0.8600 | 0 | 0.3800 |  | 0.6600 | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 4 | Pul_1636779139_51 | 15.8060 | 78.0845 | 0.5100 | 0 | 0.3200 |  | 0.6100 | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 5 | Pul_463099816_79 | 15.8068 | 78.0861 | 0.7900 | 0 | 0.4500 |  | 0.5600 | 2026-10-26 | 2026-10-26 | Moderate (55%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
