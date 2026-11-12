# Drought system report - 2023-10-27

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | weather_ok | ALARM | rainfed_fields_with_data | median_SVI | fields_below_normal | satellite_ok | CONFIRMED | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Som | -2.2400 | -2.2300 | True | True | 8 | -1.6000 | 75% | True | True | DROUGHT: alarm confirmed by crops |
| Lep | -2.1300 | -2.5200 | True | True | 8 | -0.9200 | 50% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Cho | -2.1300 | -2.5200 | True | True | 6 | -2.6300 | 67% | True | True | DROUGHT: alarm confirmed by crops |
| Sira | -2.1700 | -2.2600 | True | True | 22 | -2.2700 | 91% | True | True | DROUGHT: alarm confirmed by crops |
| Ped | -2.5200 | -1.9100 | True | True | 20 | -0.7400 | 45% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |
| Din | -2.3700 | -1.8500 | True | True | 19 | -1.9200 | 89% | True | True | DROUGHT: alarm confirmed by crops |
| Bal | -2.0300 | -1.5900 | True | True | 19 | -1.2900 | 58% | True | True | DROUGHT: alarm confirmed by crops |
| Pul | -2.0300 | -1.5900 | True | True | 19 | -0.4300 | 37% | True | False | WATCH: weather alarm, rainfed crops observed not below normal |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | weather_ok | ALARM |
|---|---|---|---|---|---|---|---|---|
| Som | 2023-10-27 | -2.2400 | -2.2300 | Severe (88%), issued 2023-10-27 | Moderate (70%), issued 2023-10-27 | Healthy (43%), issued 2023-10-27 | True | True |
| Lep | 2023-10-27 | -2.1300 | -2.5200 | Severe (85%), issued 2023-10-27 | Moderate (64%), issued 2023-10-27 | Healthy (42%), issued 2023-10-27 | True | True |
| Cho | 2023-10-27 | -2.1300 | -2.5200 | Severe (85%), issued 2023-10-27 | Moderate (64%), issued 2023-10-27 | Healthy (42%), issued 2023-10-27 | True | True |
| Sira | 2023-10-27 | -2.1700 | -2.2600 | Severe (89%), issued 2023-10-27 | Moderate (60%), issued 2023-10-27 | Moderate (40%), issued 2023-10-27 | True | True |
| Ped | 2023-10-27 | -2.5200 | -1.9100 | Severe (95%), issued 2023-10-27 | Severe (46%), issued 2023-10-27 | Moderate (60%), issued 2023-10-27 | True | True |
| Din | 2023-10-27 | -2.3700 | -1.8500 | Severe (94%), issued 2023-10-27 | Severe (59%), issued 2023-10-27 | Moderate (61%), issued 2023-10-27 | True | True |
| Bal | 2023-10-27 | -2.0300 | -1.5900 | Severe (96%), issued 2023-10-27 | Severe (84%), issued 2023-10-27 | Moderate (67%), issued 2023-10-27 | True | True |
| Pul | 2023-10-27 | -2.0300 | -1.5900 | Severe (96%), issued 2023-10-27 | Severe (84%), issued 2023-10-27 | Moderate (67%), issued 2023-10-27 | True | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_image_age_days | median_SVI | fields_below_normal | fields_strongly_below | satellite_ok | CONFIRMED |
|---|---|---|---|---|---|---|---|
| Som | 8 | 2.0000 | -1.6000 | 75% | 62% | True | True |
| Lep | 8 | 2.0000 | -0.9200 | 50% | 50% | True | False |
| Cho | 6 | 2.0000 | -2.6300 | 67% | 50% | True | True |
| Sira | 22 | 3.0000 | -2.2700 | 91% | 77% | True | True |
| Ped | 20 | 9.0000 | -0.7400 | 45% | 10% | True | False |
| Din | 19 | 2.0000 | -1.9200 | 89% | 63% | True | True |
| Bal | 19 | 2.0000 | -1.2900 | 58% | 37% | True | True |
| Pul | 19 | 2.0000 | -0.4300 | 37% | 21% | True | False |

CONFIRMED = median rainfed SVI < -1, from at least 5 rainfed fields with an image at most 30 days old; fewer = INSUFFICIENT satellite data (never read as 'not stressed'). Weather older than 5 days or a forecast issued more than 5 days before the date is not used.

## Stage 3: fields to fly

Rainfed fields only; up to 5 per site and list. Map: `fields_to_fly.kml` (Google Earth; red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 (below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score >= 0.5 (a ranking score, not a calibrated probability). For an unbiased check, also visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the selection used).

At-risk ranking skipped: 2023 is inside the crop model's training years (2019-2024), so its predictions would be in-sample.

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | image_age_days | risk_score_15d | issue_date | weather_obs_date | weather_forecast_+15d | crop_model | svi_reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Som | stressed now (satellite candidate) | 1 | Som_-223763135_122 | 14.0222 | 77.6125 | 1.2200 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (70%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 2 | Som_35281328_83 | 14.0148 | 77.6425 | 0.8300 | 0 | -2.1300 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (70%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 3 | Som_-1925665651_37 | 14.0086 | 77.6145 | 0.3700 | 0 | -1.6700 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (70%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 4 | Som_1482689627_50 | 14.0087 | 77.6485 | 0.5000 | 0 | -1.6200 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (70%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Som | stressed now (satellite candidate) | 5 | Som_-1542221172_63 | 13.9866 | 77.6259 | 0.6300 | 0 | -1.5800 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (70%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 1 | Lep_-1546782791_66 | 13.8003 | 77.6149 | 0.6600 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 2 | Lep_-1812797810_63 | 13.7933 | 77.6033 | 0.6300 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 3 | Lep_-393847897_93 | 13.7894 | 77.6325 | 0.9300 | 0 | -2.9000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Lep | stressed now (satellite candidate) | 4 | Lep_1366978471_115 | 13.7921 | 77.6394 | 1.1500 | 0 | -1.5200 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 1 | Cho_-1219185741_62 | 13.7969 | 77.5868 | 0.6200 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 2 | Cho_906555622_62 | 13.8059 | 77.5884 | 0.6200 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 3 | Cho_129924392_60 | 13.7863 | 77.5719 | 0.6000 | 0 | -3.9200 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Cho | stressed now (satellite candidate) | 4 | Cho_-1929682815_75 | 13.8219 | 77.5890 | 0.7500 | 0 | -1.3400 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (64%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 1 | Sira_-987710890_81 | 13.7767 | 76.9592 | 0.8100 | 0 | -4.0000 | 4.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 2 | Sira_-854967134_68 | 13.8034 | 76.9954 | 0.6800 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 3 | Sira_384305002_59 | 13.8013 | 76.9684 | 0.5900 | 0 | -4.0000 | 4.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 4 | Sira_1763389266_55 | 13.8228 | 76.9837 | 0.5500 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Sira | stressed now (satellite candidate) | 5 | Sira_677356488_49 | 13.8222 | 76.9790 | 0.4900 | 0 | -3.8600 | 4.0000 |  | 2023-10-27 | 2023-10-27 | Moderate (60%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 1 | Ped_1760488617_38 | 15.8089 | 77.2495 | 0.3800 | 0 | -2.8700 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (46%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 2 | Ped_-889960087_38 | 15.7629 | 77.2693 | 0.3800 | 0 | -2.4300 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (46%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 3 | Ped_-575438081_75 | 15.7860 | 77.2343 | 0.7500 | 0 | -1.5000 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (46%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 4 | Ped_979873077_45 | 15.7878 | 77.2793 | 0.4500 | 0 | -1.4700 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (46%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Ped | stressed now (satellite candidate) | 5 | Ped_382106004_80 | 15.7902 | 77.2739 | 0.8000 | 0 | -1.4000 | 9.0000 |  | 2023-10-27 | 2023-10-27 | Severe (46%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 1 | Din_-1891079513_44 | 15.7721 | 78.0324 | 0.4400 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (59%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 2 | Din_948347010_42 | 15.7742 | 78.0497 | 0.4200 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (59%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 3 | Din_1784106062_75 | 15.7777 | 78.0379 | 0.7500 | 0 | -3.5600 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (59%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 4 | Din_-1238525482_49 | 15.7781 | 78.0396 | 0.4900 | 0 | -2.7400 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (59%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Din | stressed now (satellite candidate) | 5 | Din_1654695847_52 | 15.7808 | 78.0356 | 0.5200 | 0 | -2.5800 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (59%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 1 | Bal_1503534318_44 | 15.7838 | 78.0687 | 0.4400 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 2 | Bal_-552641801_47 | 15.7866 | 78.0395 | 0.4700 | 0 | -3.5700 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 3 | Bal_1963738580_62 | 15.7844 | 78.0470 | 0.6200 | 0 | -3.2700 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 4 | Bal_-1704278698_80 | 15.7841 | 78.0722 | 0.8000 | 0 | -2.6800 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Bal | stressed now (satellite candidate) | 5 | Bal_1133572988_39 | 15.7699 | 78.0708 | 0.3900 | 0 | -2.5200 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 1 | Pul_-391022102_74 | 15.8129 | 78.0682 | 0.7400 | 0 | -4.0000 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 2 | Pul_509973208_86 | 15.8239 | 78.0802 | 0.8600 | 0 | -3.0900 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 3 | Pul_463099816_79 | 15.8068 | 78.0861 | 0.7900 | 0 | -1.9200 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 4 | Pul_1245157234_56 | 15.8047 | 78.0891 | 0.5600 | 0 | -1.6100 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
| Pul | stressed now (satellite candidate) | 5 | Pul_-831687081_86 | 15.7869 | 78.1027 | 0.8600 | 0 | -1.4900 | 2.0000 |  | 2023-10-27 | 2023-10-27 | Severe (84%), issued 2023-10-27 |  | 2019-2023, own year excluded |
