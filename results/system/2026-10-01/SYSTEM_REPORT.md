# Drought system report - 2026-10-01

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -2.1400 | -2.1800 | True | True | 9 | -2.5200 | 89% | True | True | DROUGHT: alarm confirmed by crops |
| Lep | -1.9900 | -2.3400 | True | True | 10 | -1.0800 | 60% | True | True | DROUGHT: alarm confirmed by crops |
| Cho | -1.9900 | -2.3400 | True | True | 11 | -2.2500 | 82% | True | True | DROUGHT: alarm confirmed by crops |
| Sira | -1.7700 | -2.0600 | True | True | 19 | -1.6900 | 58% | True | True | DROUGHT: alarm confirmed by crops |
| Ped | -1.8000 | -2.0700 | True | True | 22 | -0.0100 | 14% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Din | -1.2100 | -1.7600 | True | True | 16 | -1.6800 | 81% | True | True | DROUGHT: alarm confirmed by crops |
| Bal | -0.5800 | -1.4700 | True | False | 21 | -1.3200 | 71% | True | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Pul | -0.5800 | -1.4700 | True | False | 14 | -0.8400 | 43% | True | False | normal (observed) |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2026-10-01 | -2.1400 | -2.1800 | Moderate (76%), issued 2026-10-01 | Moderate (80%), issued 2026-10-01 | Moderate (44%), issued 2026-10-01 | True | True |
| Lep | 2026-10-01 | -1.9900 | -2.3400 | Moderate (91%), issued 2026-10-01 | Moderate (79%), issued 2026-10-01 | Moderate (47%), issued 2026-10-01 | True | True |
| Cho | 2026-10-01 | -1.9900 | -2.3400 | Moderate (91%), issued 2026-10-01 | Moderate (79%), issued 2026-10-01 | Moderate (47%), issued 2026-10-01 | True | True |
| Sira | 2026-10-01 | -1.7700 | -2.0600 | Moderate (93%), issued 2026-10-01 | Moderate (81%), issued 2026-10-01 | Moderate (61%), issued 2026-10-01 | True | True |
| Ped | 2026-10-01 | -1.8000 | -2.0700 | Moderate (61%), issued 2026-10-01 | Moderate (73%), issued 2026-10-01 | Moderate (46%), issued 2026-10-01 | True | True |
| Din | 2026-10-01 | -1.2100 | -1.7600 | Moderate (93%), issued 2026-10-01 | Moderate (66%), issued 2026-10-01 | Moderate (45%), issued 2026-10-01 | True | True |
| Bal | 2026-10-01 | -0.5800 | -1.4700 | Moderate (92%), issued 2026-10-01 | Moderate (71%), issued 2026-10-01 | Moderate (50%), issued 2026-10-01 | True | False |
| Pul | 2026-10-01 | -0.5800 | -1.4700 | Moderate (92%), issued 2026-10-01 | Moderate (71%), issued 2026-10-01 | Moderate (50%), issued 2026-10-01 | True | False |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 9 | 25.0000 | -2.5200 | 89% | 89% | True | True |
| Lep | 10 | 2.0000 | -1.0800 | 60% | 30% | True | True |
| Cho | 11 | 2.0000 | -2.2500 | 82% | 82% | True | True |
| Sira | 19 | 4.0000 | -1.6900 | 58% | 53% | True | True |
| Ped | 22 | 4.0000 | -0.0100 | 14% | 9% | True | False |
| Din | 16 | 17.0000 | -1.6800 | 81% | 56% | True | True |
| Bal | 21 | 22.0000 | -1.3200 | 71% | 33% | True | True |
| Pul | 14 | 17.0000 | -0.8400 | 43% | 21% | True | False |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Som | stressed now (satellite candidate) | 1 | Som_1464160869_79 | 14.0109 | 77.5845 | 0.7900 | 0 | -4.0000 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (80%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 2 | Som_920238639_59 | 13.9967 | 77.5949 | 0.5900 | 0 | -3.2100 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (80%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 3 | Som_362814257_52 | 14.0324 | 77.6027 | 0.5200 | 0 | -2.9400 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (80%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 4 | Som_2097648969_50 | 14.0233 | 77.6040 | 0.5000 | 0 | -2.6100 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (80%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 5 | Som_1097302293_56 | 13.9855 | 77.5978 | 0.5600 | 0 | -2.5200 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (80%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 1 | Lep_1522682864_56 | 13.8138 | 77.6312 | 0.5600 | 0 | -3.9500 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 2 | Lep_-1698579646_103 | 13.8131 | 77.6328 | 1.0300 | 0 | -3.8200 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 3 | Lep_459778305_53 | 13.8110 | 77.6425 | 0.5300 | 0 | -3.7000 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 4 | Lep_-264524700_49 | 13.7931 | 77.6119 | 0.4900 | 0 | -1.3300 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 5 | Lep_-1743579144_59 | 13.8016 | 77.6216 | 0.5900 | 0 | -1.1500 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 1 | Cho_-472169848_43 | 13.8375 | 77.5747 | 0.4300 | 0 | -4.0000 | 27.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 2 | Cho_-46773438_75 | 13.7864 | 77.5755 | 0.7500 | 0 | -3.3200 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 3 | Cho_-1661137969_44 | 13.8187 | 77.5916 | 0.4400 | 0 | -2.8700 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 4 | Cho_-252629698_73 | 13.7891 | 77.5816 | 0.7300 | 0 | -2.7800 | 2.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 5 | Cho_-592418679_91 | 13.8372 | 77.5677 | 0.9100 | 0 | -2.5600 | 27.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (79%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_-1344237192_63 | 13.8020 | 76.9669 | 0.6300 | 0 | -3.4800 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (81%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 2 | Sira_2018929124_87 | 13.7848 | 76.9683 | 0.8700 | 0 | -3.0700 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (81%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 3 | Sira_1795621425_56 | 13.7737 | 76.9868 | 0.5600 | 0 | -2.3900 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (81%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 4 | Sira_516408832_81 | 13.7840 | 76.9633 | 0.8100 | 0 | -2.3300 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (81%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 5 | Sira_-1874373028_58 | 13.8139 | 76.9605 | 0.5800 | 0 | -2.3000 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (81%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Sira | at risk (normal now) | 1 | Sira_-1027103336_36 | 13.8056 | 76.9916 | 0.3600 | 0 | 0.0800 |  | 0.6000 | 2026-10-01 | 2026-10-01 | Moderate (81%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_-687601348_57 | 15.7605 | 77.2635 | 0.5700 | 0 | -2.1100 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 2 | Ped_-1627922839_44 | 15.8078 | 77.2467 | 0.4400 | 0 | -1.5300 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 3 | Ped_-1000886989_32 | 15.8019 | 77.2414 | 0.3200 | 0 | -1.4200 | 4.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 1 | Ped_-2000856864_111 | 15.7713 | 77.2694 | 1.1100 | 0 | 0.0100 |  | 0.8900 | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 2 | Ped_-117238212_73 | 15.7779 | 77.2491 | 0.7300 | 0 | 0.6900 |  | 0.8600 | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 3 | Ped_23224963_43 | 15.7606 | 77.2660 | 0.4300 | 0 | 0.1100 |  | 0.8300 | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 4 | Ped_-383613436_58 | 15.7877 | 77.2364 | 0.5800 | 0 | 0.0400 |  | 0.7600 | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Ped | at risk (normal now) | 5 | Ped_-503391457_56 | 15.7868 | 77.2614 | 0.5600 | 0 | 0.5300 |  | 0.7300 | 2026-10-01 | 2026-10-01 | Moderate (73%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 1 | Din_929501593_81 | 15.7850 | 78.0379 | 0.8100 | 0 | -3.9600 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (66%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 2 | Din_894904914_53 | 15.7858 | 78.0388 | 0.5300 | 0 | -3.3300 | 22.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (66%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 3 | Din_2049257924_64 | 15.7728 | 78.0336 | 0.6400 | 0 | -2.7300 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (66%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 4 | Din_4358011_38 | 15.7773 | 78.0357 | 0.3800 | 0 | -2.5900 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (66%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 5 | Din_1028714085_104 | 15.7771 | 78.0349 | 1.0400 | 0 | -2.5500 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (66%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 1 | Bal_1078425042_89 | 15.7702 | 78.0764 | 0.8900 | 0 | -2.5100 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 2 | Bal_1108221314_76 | 15.7685 | 78.0780 | 0.7600 | 0 | -2.3000 | 25.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 3 | Bal_1017553099_41 | 15.7850 | 78.0506 | 0.4100 | 0 | -2.2800 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 4 | Bal_-67821535_75 | 15.7780 | 78.0611 | 0.7500 | 0 | -2.2500 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 5 | Bal_-172550388_101 | 15.7701 | 78.0787 | 1.0100 | 0 | -1.7400 | 22.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Bal | at risk (normal now) | 1 | Bal_-1567632517_33 | 15.7720 | 78.0796 | 0.3300 | 0 | 0.3500 |  | 0.7500 | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_-1093009035_51 | 15.7787 | 78.0991 | 0.5100 | 0 | -3.8100 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 2 | Pul_-1723364789_65 | 15.7850 | 78.0875 | 0.6500 | 0 | -2.5300 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 3 | Pul_-1844622635_33 | 15.7881 | 78.0895 | 0.3300 | 0 | -1.8500 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 4 | Pul_693464584_75 | 15.7852 | 78.0726 | 0.7500 | 0 | -1.4000 | 22.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 5 | Pul_-2111834955_52 | 15.7738 | 78.0837 | 0.5200 | 0 | -1.1400 | 17.0000 |  | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
| Pul | at risk (normal now) | 1 | Pul_331786056_66 | 15.7868 | 78.0753 | 0.6600 | 0 | 0.4100 |  | 0.7200 | 2026-10-01 | 2026-10-01 | Moderate (71%), issued 2026-10-01 | crop_xgb_sat_weatherforecast_h15.json | 2019-2023, own year excluded |
