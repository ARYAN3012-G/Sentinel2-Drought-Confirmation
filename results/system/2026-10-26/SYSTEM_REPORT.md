# Drought system report - 2026-10-26

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -0.8500 | -1.7900 | True | False | 19 | -2.5400 | 84% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Lep | -0.1700 | -1.5600 | True | False | 17 | -1.2900 | 59% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Cho | -0.1700 | -1.5600 | True | False | 18 | -1.4100 | 67% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Sira | 0.3100 | -1.3700 | True | False | 21 | -1.1400 | 62% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Ped | -2.4600 | -2.3600 | True | True | 22 | -0.0600 | 23% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Din | -2.2600 | -2.1200 | True | True | 20 | -0.9700 | 40% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Bal | -2.0900 | -1.8500 | True | True | 21 | -0.6600 | 43% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Pul | -2.0900 | -1.8500 | True | True | 15 | -1.0900 | 53% | True | True | DROUGHT: alarm confirmed by crops |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2026-10-26 | -0.8500 | -1.7900 | Healthy (66%), issued 2026-10-26 | Healthy (89%), issued 2026-10-26 | Moderate (67%), issued 2026-10-26 | True | False |
| Lep | 2026-10-26 | -0.1700 | -1.5600 | Healthy (91%), issued 2026-10-26 | Healthy (87%), issued 2026-10-26 | Moderate (43%), issued 2026-10-26 | True | False |
| Cho | 2026-10-26 | -0.1700 | -1.5600 | Healthy (91%), issued 2026-10-26 | Healthy (87%), issued 2026-10-26 | Moderate (43%), issued 2026-10-26 | True | False |
| Sira | 2026-10-26 | 0.3100 | -1.3700 | Healthy (91%), issued 2026-10-26 | Healthy (92%), issued 2026-10-26 | Moderate (41%), issued 2026-10-26 | True | False |
| Ped | 2026-10-26 | -2.4600 | -2.3600 | Severe (78%), issued 2026-10-26 | Moderate (62%), issued 2026-10-26 | Moderate (56%), issued 2026-10-26 | True | True |
| Din | 2026-10-26 | -2.2600 | -2.1200 | Severe (76%), issued 2026-10-26 | Moderate (68%), issued 2026-10-26 | Moderate (64%), issued 2026-10-26 | True | True |
| Bal | 2026-10-26 | -2.0900 | -1.8500 | Moderate (59%), issued 2026-10-26 | Moderate (66%), issued 2026-10-26 | Moderate (49%), issued 2026-10-26 | True | True |
| Pul | 2026-10-26 | -2.0900 | -1.8500 | Moderate (59%), issued 2026-10-26 | Moderate (66%), issued 2026-10-26 | Moderate (49%), issued 2026-10-26 | True | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 19 | 10.0000 | -2.5400 | 84% | 74% | True | True |
| Lep | 17 | 12.0000 | -1.2900 | 59% | 41% | True | True |
| Cho | 18 | 11.0000 | -1.4100 | 67% | 50% | True | True |
| Sira | 21 | 12.0000 | -1.1400 | 62% | 33% | True | True |
| Ped | 22 | 14.0000 | -0.0600 | 23% | 23% | True | False |
| Din | 20 | 7.0000 | -0.9700 | 40% | 15% | True | False |
| Bal | 21 | 7.0000 | -0.6600 | 43% | 0% | True | False |
| Pul | 15 | 12.0000 | -1.0900 | 53% | 27% | True | True |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Som | stressed now (satellite candidate) | 1 | Som_-302553309_38 | 14.0101 | 77.5937 | 0.3800 | 0 | -3.9700 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (89%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 2 | Som_1464160869_79 | 14.0109 | 77.5845 | 0.7900 | 0 | -3.9500 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (89%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 3 | Som_-705821922_59 | 14.0096 | 77.5839 | 0.5900 | 0 | -3.8400 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (89%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 4 | Som_1087396711_50 | 14.0208 | 77.6019 | 0.5000 | 0 | -3.5200 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (89%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 5 | Som_920238639_59 | 13.9967 | 77.5949 | 0.5900 | 0 | -3.3100 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (89%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 1 | Lep_1522682864_56 | 13.8138 | 77.6312 | 0.5600 | 0 | -3.0600 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 2 | Lep_-1698579646_103 | 13.8131 | 77.6328 | 1.0300 | 0 | -2.8600 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 3 | Lep_459778305_53 | 13.8110 | 77.6425 | 0.5300 | 0 | -2.8500 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 4 | Lep_381130640_83 | 13.8192 | 77.6077 | 0.8300 | 0 | -2.6700 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 5 | Lep_-682021274_65 | 13.8023 | 77.6267 | 0.6500 | 0 | -2.5300 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | at risk (normal now) | 1 | Lep_1259953916_73 | 13.8133 | 77.6228 | 0.7300 | 0 | 0.3700 |  | 0.5100 | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 1 | Cho_-472169848_43 | 13.8375 | 77.5747 | 0.4300 | 0 | -4.0000 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 2 | Cho_483835477_71 | 13.7922 | 77.5571 | 0.7100 | 0 | -2.2200 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 3 | Cho_-592418679_91 | 13.8372 | 77.5677 | 0.9100 | 0 | -2.1300 | 10.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 4 | Cho_-1848777060_91 | 13.7943 | 77.5832 | 0.9100 | 0 | -2.0300 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 5 | Cho_-252629698_73 | 13.7891 | 77.5816 | 0.7300 | 0 | -1.7500 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (87%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_-1874373028_58 | 13.8139 | 76.9605 | 0.5800 | 0 | -4.0000 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (92%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 2 | Sira_-1779215393_70 | 13.7848 | 76.9662 | 0.7000 | 0 | -3.3100 | 10.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (92%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 3 | Sira_2018929124_87 | 13.7848 | 76.9683 | 0.8700 | 0 | -2.8000 | 10.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (92%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 4 | Sira_-1344237192_63 | 13.8020 | 76.9669 | 0.6300 | 0 | -2.7400 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (92%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 5 | Sira_-882723474_54 | 13.8179 | 76.9613 | 0.5400 | 0 | -2.5700 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Healthy (92%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_-687601348_57 | 15.7605 | 77.2635 | 0.5700 | 0 | -3.5200 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 2 | Ped_-1631088024_86 | 15.7918 | 77.2352 | 0.8600 | 0 | -1.7600 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 3 | Ped_1967810900_76 | 15.7691 | 77.2698 | 0.7600 | 0 | -1.7400 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 4 | Ped_-1627922839_44 | 15.8078 | 77.2467 | 0.4400 | 0 | -1.5900 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 5 | Ped_-1000886989_32 | 15.8019 | 77.2414 | 0.3200 | 0 | -1.5000 | 14.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 1 | Ped_-503391457_56 | 15.7868 | 77.2614 | 0.5600 | 0 | 0.3700 |  | 0.8400 | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 2 | Ped_1965703412_70 | 15.7892 | 77.2737 | 0.7000 | 0 | 0.2800 |  | 0.7100 | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 3 | Ped_-383613436_58 | 15.7877 | 77.2364 | 0.5800 | 0 | 0.0300 |  | 0.6700 | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 4 | Ped_-430971332_39 | 15.8054 | 77.2495 | 0.3900 | 0 | 0.2900 |  | 0.5900 | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 5 | Ped_-654890566_69 | 15.7955 | 77.2519 | 0.6900 | 0 | 0.8400 |  | 0.5600 | 2026-10-26 | 2026-10-26 | Moderate (62%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 1 | Din_929501593_81 | 15.7850 | 78.0379 | 0.8100 | 0 | -3.8000 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (68%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 2 | Din_894904914_53 | 15.7858 | 78.0388 | 0.5300 | 0 | -3.6800 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (68%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 3 | Din_-181753811_57 | 15.7836 | 78.0377 | 0.5700 | 0 | -1.5700 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (68%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 4 | Din_2049257924_64 | 15.7728 | 78.0336 | 0.6400 | 0 | -1.2500 | 17.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (68%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 5 | Din_1993066397_52 | 15.7815 | 78.0432 | 0.5200 | 0 | -1.2400 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (68%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 1 | Bal_-67821535_75 | 15.7780 | 78.0611 | 0.7500 | 0 | -1.4300 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 2 | Bal_246590930_48 | 15.7846 | 78.0663 | 0.4800 | 0 | -1.4300 | 17.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 3 | Bal_337843304_63 | 15.7849 | 78.0485 | 0.6300 | 0 | -1.3600 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 4 | Bal_-915454758_79 | 15.7848 | 78.0461 | 0.7900 | 0 | -1.1400 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 5 | Bal_1109714483_55 | 15.7822 | 78.0736 | 0.5500 | 0 | -1.1100 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 1 | Bal_1133572988_37 | 15.7700 | 78.0709 | 0.3700 | 0 | 0.0200 |  | 0.8600 | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 2 | Bal_-1567632517_33 | 15.7720 | 78.0796 | 0.3300 | 0 | 0.0100 |  | 0.8200 | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 3 | Bal_1690366839_89 | 15.7870 | 78.0671 | 0.8900 | 0 | 0.0800 |  | 0.7300 | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 4 | Bal_-1059541894_63 | 15.7832 | 78.0634 | 0.6300 | 0 | 0.2400 |  | 0.5500 | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_-1093009035_51 | 15.7787 | 78.0991 | 0.5100 | 0 | -3.5800 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 2 | Pul_-1723364789_65 | 15.7850 | 78.0875 | 0.6500 | 0 | -2.2100 | 22.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 3 | Pul_693464584_75 | 15.7852 | 78.0726 | 0.7500 | 0 | -2.1200 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 4 | Pul_331786056_66 | 15.7868 | 78.0753 | 0.6600 | 0 | -1.6500 | 7.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 5 | Pul_-236412164_88 | 15.8075 | 78.0922 | 0.8800 | 0 | -1.4400 | 12.0000 |  | 2026-10-26 | 2026-10-26 | Moderate (66%), issued 2026-10-26 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
