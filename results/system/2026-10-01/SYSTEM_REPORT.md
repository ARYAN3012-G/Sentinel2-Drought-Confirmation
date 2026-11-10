# Drought system report - 2026-10-01

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | ALARM | median_SVI | fields_below_normal | CONFIRMED | status |
|---|---|---|---|---|---|---|
| Som | -2.1400 | True | -2.5200 | 89% | True | DROUGHT: alarm confirmed by crops |
| Lep | -1.9900 | True | -1.0800 | 60% | True | DROUGHT: alarm confirmed by crops |
| Cho | -1.9900 | True | -2.2500 | 82% | True | DROUGHT: alarm confirmed by crops |
| Sira | -1.7700 | True | -1.7200 | 63% | True | DROUGHT: alarm confirmed by crops |
| Ped | -1.7800 | True | 0.0200 | 10% | False | WATCH: weather alarm, crops not yet stressed |
| Din | -1.2100 | True | -1.6800 | 81% | True | DROUGHT: alarm confirmed by crops |
| Bal | -0.5800 | False | -1.2900 | 70% | True | CROP STRESS without weather alarm |
| Pul | -0.7600 | False | -0.7200 | 32% | False | normal |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | ALARM |
|---|---|---|---|---|---|---|---|
| Som | 2026-10-01 | -2.1400 | -2.1800 | Moderate (76%) | Moderate (80%) | Moderate (44%) | True |
| Lep | 2026-10-01 | -1.9900 | -2.3400 | Moderate (91%) | Moderate (79%) | Moderate (47%) | True |
| Cho | 2026-10-01 | -1.9900 | -2.3400 | Moderate (91%) | Moderate (79%) | Moderate (47%) | True |
| Sira | 2026-10-01 | -1.7700 | -2.0600 | Moderate (93%) | Moderate (81%) | Moderate (61%) | True |
| Ped | 2026-10-01 | -1.7800 | -2.0500 | Moderate (60%) | Moderate (72%) | Moderate (49%) | True |
| Din | 2026-10-01 | -1.2100 | -1.7600 | Moderate (93%) | Moderate (66%) | Moderate (45%) | True |
| Bal | 2026-10-01 | -0.5800 | -1.4700 | Moderate (92%) | Moderate (71%) | Moderate (50%) | False |
| Pul | 2026-10-01 | -0.7600 | -1.6100 | Moderate (93%) | Moderate (72%) | Severe (37%) | False |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_SVI | fields_below_normal | fields_severe | CONFIRMED |
|---|---|---|---|---|---|
| Som | 9 | -2.5200 | 89% | 89% | True |
| Lep | 10 | -1.0800 | 60% | 30% | True |
| Cho | 11 | -2.2500 | 82% | 82% | True |
| Sira | 19 | -1.7200 | 63% | 58% | True |
| Ped | 20 | 0.0200 | 10% | 5% | False |
| Din | 16 | -1.6800 | 81% | 56% | True |
| Bal | 20 | -1.2900 | 70% | 30% | True |
| Pul | 19 | -0.7200 | 32% | 16% | False |

CONFIRMED = median rainfed SVI < -1.

## Stage 3: fields to fly

Up to 5 fields per site and list. Map: `fields_to_fly.kml` (open in Google Earth; red = damaged now, orange = at risk). Table: `fields_to_fly.csv`.

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | onset_risk_15d |
|---|---|---|---|---|---|---|---|---|---|
| Som | damaged now | 1 | Som_1464160869_79 | 14.0108 | 77.5845 | 0.7900 | 0 | -4.0000 |  |
| Som | damaged now | 2 | Som_920238639_59 | 13.9967 | 77.5949 | 0.5900 | 0 | -3.2100 |  |
| Som | damaged now | 3 | Som_362814257_52 | 14.0324 | 77.6027 | 0.5200 | 0 | -2.9400 |  |
| Som | damaged now | 4 | Som_2097648969_50 | 14.0232 | 77.6041 | 0.5000 | 0 | -2.6100 |  |
| Som | damaged now | 5 | Som_1097302293_56 | 13.9855 | 77.5978 | 0.5600 | 0 | -2.5200 |  |
| Lep | damaged now | 1 | Lep_1522682864_56 | 13.8139 | 77.6311 | 0.5600 | 0 | -3.9500 |  |
| Lep | damaged now | 2 | Lep_-1698579646_103 | 13.8131 | 77.6328 | 1.0300 | 0 | -3.8200 |  |
| Lep | damaged now | 3 | Lep_459778305_53 | 13.8110 | 77.6425 | 0.5300 | 0 | -3.7000 |  |
| Lep | damaged now | 4 | Lep_-1716647714_53 | 13.8026 | 77.6180 | 0.5300 | 1 | -3.4700 |  |
| Lep | damaged now | 5 | Lep_-264524700_49 | 13.7930 | 77.6118 | 0.4900 | 0 | -1.3300 |  |
| Lep | at risk (healthy now) | 1 | Lep_-171177260_37 | 13.8123 | 77.6180 | 0.3700 | 0 | 0.3800 | 0.2600 |
| Lep | at risk (healthy now) | 2 | Lep_-850369929_83 | 13.7845 | 77.6347 | 0.8300 | 0 | 0.7100 | 0.2000 |
| Cho | damaged now | 1 | Cho_-472169848_43 | 13.8375 | 77.5747 | 0.4300 | 0 | -4.0000 |  |
| Cho | damaged now | 2 | Cho_1850924706_89 | 13.8231 | 77.5907 | 0.8900 | 1 | -3.3300 |  |
| Cho | damaged now | 3 | Cho_-46773438_75 | 13.7864 | 77.5756 | 0.7500 | 0 | -3.3200 |  |
| Cho | damaged now | 4 | Cho_-1661137969_44 | 13.8187 | 77.5916 | 0.4400 | 0 | -2.8700 |  |
| Cho | damaged now | 5 | Cho_-252629698_73 | 13.7891 | 77.5817 | 0.7300 | 0 | -2.7800 |  |
| Cho | at risk (healthy now) | 1 | Cho_1740444464_44 | 13.8294 | 77.5479 | 0.4400 | 1 | 0.0300 | 0.3900 |
| Sira | damaged now | 1 | Sira_-1344237192_63 | 13.8021 | 76.9669 | 0.6300 | 0 | -3.4800 |  |
| Sira | damaged now | 2 | Sira_1105854812_72 | 13.7860 | 76.9637 | 0.7200 | 1 | -3.1100 |  |
| Sira | damaged now | 3 | Sira_2018929124_87 | 13.7849 | 76.9682 | 0.8700 | 0 | -3.0700 |  |
| Sira | damaged now | 4 | Sira_157775990_72 | 13.7817 | 76.9793 | 0.7200 | 0 | -2.6700 |  |
| Sira | damaged now | 5 | Sira_1795621425_56 | 13.7735 | 76.9867 | 0.5600 | 0 | -2.3900 |  |
| Sira | at risk (healthy now) | 1 | Sira_-1027103336_36 | 13.8055 | 76.9915 | 0.3600 | 0 | 0.0800 | 0.6000 |
| Sira | at risk (healthy now) | 2 | Sira_285194755_164 | 13.8223 | 76.9808 | 1.6400 | 1 | 0.5600 | 0.2900 |
| Sira | at risk (healthy now) | 3 | Sira_1956716179_63 | 13.8031 | 76.9685 | 0.6300 | 1 | 1.0800 | 0.2700 |
| Sira | at risk (healthy now) | 4 | Sira_-606204293_121 | 13.8063 | 76.9522 | 1.2100 | 1 | 1.2700 | 0.1900 |
| Sira | at risk (healthy now) | 5 | Sira_2112442363_57 | 13.8115 | 76.9826 | 0.5700 | 1 | 1.6100 | 0.0900 |
| Ped | damaged now | 1 | Ped_-687601348_57 | 15.7605 | 77.2635 | 0.5700 | 0 | -2.1100 |  |
| Ped | damaged now | 2 | Ped_-1627922839_44 | 15.8078 | 77.2467 | 0.4400 | 1 | -1.5300 |  |
| Ped | damaged now | 3 | Ped_-1000886989_32 | 15.8020 | 77.2413 | 0.3200 | 0 | -1.4200 |  |
| Ped | damaged now | 4 | Ped_-1695147411_51 | 15.7962 | 77.2524 | 0.5100 | 1 | -1.1700 |  |
| Ped | damaged now | 5 | Ped_-608278541_33 | 15.7668 | 77.2429 | 0.3300 | 1 | -1.0300 |  |
| Ped | at risk (healthy now) | 1 | Ped_-2000856864_111 | 15.7712 | 77.2693 | 1.1100 | 0 | 0.0100 | 0.7700 |
| Ped | at risk (healthy now) | 2 | Ped_-383613436_58 | 15.7877 | 77.2362 | 0.5800 | 0 | 0.0400 | 0.7200 |
| Ped | at risk (healthy now) | 3 | Ped_23224963_43 | 15.7604 | 77.2660 | 0.4300 | 1 | 0.1100 | 0.7100 |
| Ped | at risk (healthy now) | 4 | Ped_-503391457_56 | 15.7869 | 77.2614 | 0.5600 | 0 | 0.5300 | 0.7000 |
| Ped | at risk (healthy now) | 5 | Ped_-117238212_73 | 15.7777 | 77.2490 | 0.7300 | 0 | 0.6900 | 0.6500 |
| Din | damaged now | 1 | Din_929501593_81 | 15.7850 | 78.0380 | 0.8100 | 0 | -3.9600 |  |
| Din | damaged now | 2 | Din_2064016870_80 | 15.7620 | 78.0673 | 0.8000 | 1 | -3.6800 |  |
| Din | damaged now | 3 | Din_894904914_53 | 15.7857 | 78.0388 | 0.5300 | 0 | -3.3300 |  |
| Din | damaged now | 4 | Din_684289867_59 | 15.7557 | 78.0605 | 0.5900 | 1 | -3.3100 |  |
| Din | damaged now | 5 | Din_2049257924_64 | 15.7726 | 78.0334 | 0.6400 | 0 | -2.7300 |  |
| Din | at risk (healthy now) | 1 | Din_697481584_87 | 15.7499 | 78.0623 | 0.8700 | 1 | 0.9300 | 0.4600 |
| Din | at risk (healthy now) | 2 | Din_676828463_40 | 15.7659 | 78.0258 | 0.4000 | 1 | 1.3400 | 0.1900 |
| Bal | damaged now | 1 | Bal_-820752182_61 | 15.7661 | 78.0746 | 0.6100 | 1 | -2.9200 |  |
| Bal | damaged now | 2 | Bal_1078425042_89 | 15.7702 | 78.0765 | 0.8900 | 0 | -2.5100 |  |
| Bal | damaged now | 3 | Bal_1108221314_76 | 15.7684 | 78.0778 | 0.7600 | 0 | -2.3000 |  |
| Bal | damaged now | 4 | Bal_1017553099_41 | 15.7850 | 78.0505 | 0.4100 | 0 | -2.2800 |  |
| Bal | damaged now | 5 | Bal_-67821535_75 | 15.7781 | 78.0611 | 0.7500 | 0 | -2.2500 |  |
| Bal | at risk (healthy now) | 1 | Bal_-1567632517_33 | 15.7720 | 78.0795 | 0.3300 | 0 | 0.3500 | 0.6200 |
| Bal | at risk (healthy now) | 2 | Bal_85063551_54 | 15.7639 | 78.0750 | 0.5400 | 1 | 0.1500 | 0.5700 |
| Bal | at risk (healthy now) | 3 | Bal_-97984970_75 | 15.7649 | 78.0707 | 0.7500 | 1 | 2.9300 | 0.3100 |
| Bal | at risk (healthy now) | 4 | Bal_37731501_52 | 15.7641 | 78.0712 | 0.5200 | 1 | 1.3800 | 0.3000 |
| Pul | damaged now | 1 | Pul_-1093009035_51 | 15.7786 | 78.0989 | 0.5100 | 0 | -3.8100 |  |
| Pul | damaged now | 2 | Pul_387252711_43 | 15.8104 | 78.0967 | 0.4300 | 1 | -2.6300 |  |
| Pul | damaged now | 3 | Pul_-1723364789_65 | 15.7849 | 78.0875 | 0.6500 | 0 | -2.5300 |  |
| Pul | damaged now | 4 | Pul_-684475182_101 | 15.7971 | 78.0964 | 1.0100 | 1 | -2.2600 |  |
| Pul | damaged now | 5 | Pul_-1844622635_33 | 15.7880 | 78.0895 | 0.3300 | 0 | -1.8500 |  |
| Pul | at risk (healthy now) | 1 | Pul_-1520453160_52 | 15.7829 | 78.0975 | 0.5200 | 1 | 0.1500 | 0.5600 |
| Pul | at risk (healthy now) | 2 | Pul_94858241_37 | 15.7765 | 78.0924 | 0.3700 | 1 | 0.1000 | 0.5500 |
| Pul | at risk (healthy now) | 3 | Pul_331786056_66 | 15.7869 | 78.0752 | 0.6600 | 0 | 0.4100 | 0.4200 |
| Pul | at risk (healthy now) | 4 | Pul_1878893000_41 | 15.7790 | 78.0999 | 0.4100 | 0 | 0.2900 | 0.4200 |
| Pul | at risk (healthy now) | 5 | Pul_894423709_38 | 15.8234 | 78.0878 | 0.3800 | 0 | 0.8500 | 0.2900 |
