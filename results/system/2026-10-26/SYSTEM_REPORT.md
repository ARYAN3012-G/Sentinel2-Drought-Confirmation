# Drought system report - 2026-10-26

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | ALARM | median_SVI | fields_below_normal | CONFIRMED | status |
|---|---|---|---|---|---|---|---|
| Som | -0.8500 | -1.7900 | False | -2.5400 | 85% | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Lep | -0.1700 | -1.5600 | False | -1.2900 | 59% | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Cho | -0.1700 | -1.5600 | False | -1.5400 | 71% | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Sira | 0.3100 | -1.3700 | False | -1.1600 | 65% | True | DROUGHT continuing: crops stressed, 90-day deficit persists |
| Ped | -2.4500 | -2.3600 | True | -0.0600 | 20% | False | WATCH: weather alarm, crops not yet stressed |
| Din | -2.2600 | -2.1200 | True | -0.9700 | 40% | False | WATCH: weather alarm, crops not yet stressed |
| Bal | -2.0900 | -1.8500 | True | -0.7300 | 45% | False | WATCH: weather alarm, crops not yet stressed |
| Pul | -2.2700 | -1.8200 | True | -0.8500 | 40% | False | WATCH: weather alarm, crops not yet stressed |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | ALARM |
|---|---|---|---|---|---|---|---|
| Som | 2026-10-26 | -0.8500 | -1.7900 | Healthy (66%) | Healthy (89%) | Moderate (67%) | False |
| Lep | 2026-10-26 | -0.1700 | -1.5600 | Healthy (91%) | Healthy (87%) | Moderate (43%) | False |
| Cho | 2026-10-26 | -0.1700 | -1.5600 | Healthy (91%) | Healthy (87%) | Moderate (43%) | False |
| Sira | 2026-10-26 | 0.3100 | -1.3700 | Healthy (91%) | Healthy (92%) | Moderate (41%) | False |
| Ped | 2026-10-26 | -2.4500 | -2.3600 | Severe (80%) | Moderate (64%) | Moderate (57%) | True |
| Din | 2026-10-26 | -2.2600 | -2.1200 | Severe (76%) | Moderate (68%) | Moderate (64%) | True |
| Bal | 2026-10-26 | -2.0900 | -1.8500 | Moderate (59%) | Moderate (66%) | Moderate (49%) | True |
| Pul | 2026-10-26 | -2.2700 | -1.8200 | Moderate (56%) | Moderate (68%) | Moderate (52%) | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_SVI | fields_below_normal | fields_severe | CONFIRMED |
|---|---|---|---|---|---|
| Som | 20 | -2.5400 | 85% | 70% | True |
| Lep | 17 | -1.2900 | 59% | 41% | True |
| Cho | 17 | -1.5400 | 71% | 53% | True |
| Sira | 20 | -1.1600 | 65% | 35% | True |
| Ped | 20 | -0.0600 | 20% | 20% | False |
| Din | 20 | -0.9700 | 40% | 15% | False |
| Bal | 20 | -0.7300 | 45% | 0% | False |
| Pul | 20 | -0.8500 | 40% | 20% | False |

CONFIRMED = median rainfed SVI < -1.

## Stage 3: fields to fly

Up to 5 fields per site and list. Map: `fields_to_fly.kml` (open in Google Earth; red = damaged now, orange = at risk). Table: `fields_to_fly.csv`.

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | onset_risk_15d |
|---|---|---|---|---|---|---|---|---|---|
| Som | damaged now | 1 | Som_982738382_60 | 13.9977 | 77.6037 | 0.6000 | 1 | -4.0000 |  |
| Som | damaged now | 2 | Som_-302553309_38 | 14.0101 | 77.5937 | 0.3800 | 0 | -3.9700 |  |
| Som | damaged now | 3 | Som_1464160869_79 | 14.0108 | 77.5845 | 0.7900 | 0 | -3.9500 |  |
| Som | damaged now | 4 | Som_-705821922_59 | 14.0095 | 77.5837 | 0.5900 | 0 | -3.8400 |  |
| Som | damaged now | 5 | Som_1087396711_50 | 14.0207 | 77.6019 | 0.5000 | 0 | -3.5200 |  |
| Som | at risk (healthy now) | 1 | Som_2059159336_108 | 13.9945 | 77.6253 | 1.0800 | 1 | 0.0100 | 0.6300 |
| Som | at risk (healthy now) | 2 | Som_170025400_45 | 14.0049 | 77.6256 | 0.4500 | 1 | 0.9000 | 0.2000 |
| Som | at risk (healthy now) | 3 | Som_-1210511476_65 | 14.0029 | 77.6262 | 0.6500 | 0 | 1.2800 | 0.1100 |
| Lep | damaged now | 1 | Lep_-1716647714_53 | 13.8026 | 77.6180 | 0.5300 | 1 | -3.8800 |  |
| Lep | damaged now | 2 | Lep_1522682864_56 | 13.8139 | 77.6311 | 0.5600 | 0 | -3.0600 |  |
| Lep | damaged now | 3 | Lep_-1698579646_103 | 13.8131 | 77.6328 | 1.0300 | 0 | -2.8600 |  |
| Lep | damaged now | 4 | Lep_459778305_53 | 13.8110 | 77.6425 | 0.5300 | 0 | -2.8500 |  |
| Lep | damaged now | 5 | Lep_381130640_83 | 13.8192 | 77.6077 | 0.8300 | 0 | -2.6700 |  |
| Lep | at risk (healthy now) | 1 | Lep_1259953916_73 | 13.8132 | 77.6227 | 0.7300 | 0 | 0.3700 | 0.3500 |
| Lep | at risk (healthy now) | 2 | Lep_1563079934_81 | 13.7872 | 77.6318 | 0.8100 | 0 | 0.4000 | 0.3300 |
| Lep | at risk (healthy now) | 3 | Lep_-444824672_46 | 13.8182 | 77.6175 | 0.4600 | 1 | 0.3900 | 0.2700 |
| Lep | at risk (healthy now) | 4 | Lep_-850369929_83 | 13.7845 | 77.6347 | 0.8300 | 0 | 1.5300 | 0.0800 |
| Lep | at risk (healthy now) | 5 | Lep_-171177260_37 | 13.8123 | 77.6180 | 0.3700 | 0 | 0.7800 | 0.0800 |
| Cho | damaged now | 1 | Cho_-472169848_43 | 13.8375 | 77.5747 | 0.4300 | 0 | -4.0000 |  |
| Cho | damaged now | 2 | Cho_-113624334_61 | 13.8282 | 77.5753 | 0.6100 | 0 | -3.3100 |  |
| Cho | damaged now | 3 | Cho_1850924706_89 | 13.8231 | 77.5907 | 0.8900 | 1 | -2.2600 |  |
| Cho | damaged now | 4 | Cho_483835477_71 | 13.7922 | 77.5571 | 0.7100 | 1 | -2.2200 |  |
| Cho | damaged now | 5 | Cho_-592418679_91 | 13.8373 | 77.5676 | 0.9100 | 0 | -2.1300 |  |
| Cho | at risk (healthy now) | 1 | Cho_252379585_63 | 13.8327 | 77.5574 | 0.6300 | 1 | 1.3900 | 0.3800 |
| Cho | at risk (healthy now) | 2 | Cho_1740444464_44 | 13.8294 | 77.5479 | 0.4400 | 1 | 1.4400 | 0.2700 |
| Sira | damaged now | 1 | Sira_-1874373028_58 | 13.8139 | 76.9604 | 0.5800 | 0 | -4.0000 |  |
| Sira | damaged now | 2 | Sira_-1779215393_70 | 13.7848 | 76.9662 | 0.7000 | 0 | -3.3100 |  |
| Sira | damaged now | 3 | Sira_2018929124_87 | 13.7849 | 76.9682 | 0.8700 | 0 | -2.8000 |  |
| Sira | damaged now | 4 | Sira_-1344237192_63 | 13.8021 | 76.9669 | 0.6300 | 0 | -2.7400 |  |
| Sira | damaged now | 5 | Sira_-882723474_54 | 13.8179 | 76.9612 | 0.5400 | 1 | -2.5700 |  |
| Sira | at risk (healthy now) | 1 | Sira_62646517_62 | 13.8057 | 76.9979 | 0.6200 | 0 | 0.3000 | 0.4000 |
| Sira | at risk (healthy now) | 2 | Sira_1541163073_39 | 13.8084 | 76.9855 | 0.3900 | 1 | 0.1900 | 0.3800 |
| Sira | at risk (healthy now) | 3 | Sira_1956716179_63 | 13.8031 | 76.9685 | 0.6300 | 1 | 0.7700 | 0.3400 |
| Sira | at risk (healthy now) | 4 | Sira_-1027103336_36 | 13.8055 | 76.9915 | 0.3600 | 0 | 0.6900 | 0.3000 |
| Sira | at risk (healthy now) | 5 | Sira_-33407465_52 | 13.7950 | 76.9700 | 0.5200 | 0 | 0.3000 | 0.2700 |
| Ped | damaged now | 1 | Ped_-687601348_57 | 15.7605 | 77.2635 | 0.5700 | 0 | -3.5200 |  |
| Ped | damaged now | 2 | Ped_-608278541_33 | 15.7668 | 77.2429 | 0.3300 | 1 | -2.9300 |  |
| Ped | damaged now | 3 | Ped_-1631088024_86 | 15.7917 | 77.2350 | 0.8600 | 0 | -1.7600 |  |
| Ped | damaged now | 4 | Ped_1967810900_76 | 15.7691 | 77.2698 | 0.7600 | 0 | -1.7400 |  |
| Ped | damaged now | 5 | Ped_-1627922839_44 | 15.8078 | 77.2467 | 0.4400 | 1 | -1.5900 |  |
| Ped | at risk (healthy now) | 1 | Ped_-503391457_56 | 15.7869 | 77.2614 | 0.5600 | 0 | 0.3700 | 0.5300 |
| Ped | at risk (healthy now) | 2 | Ped_-383613436_58 | 15.7877 | 77.2362 | 0.5800 | 0 | 0.0300 | 0.4900 |
| Ped | at risk (healthy now) | 3 | Ped_1965703412_70 | 15.7891 | 77.2737 | 0.7000 | 0 | 0.2800 | 0.4900 |
| Ped | at risk (healthy now) | 4 | Ped_-430971332_39 | 15.8054 | 77.2495 | 0.3900 | 0 | 0.2900 | 0.3600 |
| Ped | at risk (healthy now) | 5 | Ped_-1476327318_73 | 15.8020 | 77.2392 | 0.7300 | 0 | 0.7400 | 0.3100 |
| Din | damaged now | 1 | Din_929501593_81 | 15.7850 | 78.0380 | 0.8100 | 0 | -3.8000 |  |
| Din | damaged now | 2 | Din_894904914_53 | 15.7857 | 78.0388 | 0.5300 | 0 | -3.6800 |  |
| Din | damaged now | 3 | Din_2064016870_80 | 15.7620 | 78.0673 | 0.8000 | 1 | -2.0000 |  |
| Din | damaged now | 4 | Din_432345629_54 | 15.7657 | 78.0676 | 0.5400 | 1 | -1.8800 |  |
| Din | damaged now | 5 | Din_238962175_80 | 15.7633 | 78.0676 | 0.8000 | 1 | -1.6700 |  |
| Din | at risk (healthy now) | 1 | Din_697481584_87 | 15.7499 | 78.0623 | 0.8700 | 1 | 0.5400 | 0.4000 |
| Din | at risk (healthy now) | 2 | Din_-1900680950_53 | 15.7495 | 78.0606 | 0.5300 | 1 | 1.8900 | 0.2500 |
| Din | at risk (healthy now) | 3 | Din_-1012988290_83 | 15.7492 | 78.0591 | 0.8300 | 0 | 1.8200 | 0.2400 |
| Bal | damaged now | 1 | Bal_-640754940_44 | 15.7681 | 78.0684 | 0.4400 | 1 | -1.5900 |  |
| Bal | damaged now | 2 | Bal_-67821535_75 | 15.7781 | 78.0611 | 0.7500 | 0 | -1.4300 |  |
| Bal | damaged now | 3 | Bal_246590930_48 | 15.7846 | 78.0665 | 0.4800 | 0 | -1.4300 |  |
| Bal | damaged now | 4 | Bal_337843304_63 | 15.7848 | 78.0485 | 0.6300 | 0 | -1.3600 |  |
| Bal | damaged now | 5 | Bal_-66539026_55 | 15.7686 | 78.0683 | 0.5500 | 1 | -1.2900 |  |
| Bal | at risk (healthy now) | 1 | Bal_-1567632517_33 | 15.7720 | 78.0795 | 0.3300 | 0 | 0.0100 | 0.7600 |
| Bal | at risk (healthy now) | 2 | Bal_1133572988_37 | 15.7701 | 78.0709 | 0.3700 | 0 | 0.0200 | 0.7300 |
| Bal | at risk (healthy now) | 3 | Bal_1690366839_89 | 15.7871 | 78.0669 | 0.8900 | 0 | 0.0800 | 0.6600 |
| Bal | at risk (healthy now) | 4 | Bal_-820752182_61 | 15.7661 | 78.0746 | 0.6100 | 1 | 1.0100 | 0.4600 |
| Bal | at risk (healthy now) | 5 | Bal_37731501_52 | 15.7641 | 78.0712 | 0.5200 | 1 | 0.4700 | 0.4300 |
| Pul | damaged now | 1 | Pul_-1093009035_51 | 15.7786 | 78.0989 | 0.5100 | 0 | -3.5800 |  |
| Pul | damaged now | 2 | Pul_-684475182_101 | 15.7971 | 78.0964 | 1.0100 | 1 | -2.5100 |  |
| Pul | damaged now | 3 | Pul_-1723364789_65 | 15.7849 | 78.0875 | 0.6500 | 0 | -2.2100 |  |
| Pul | damaged now | 4 | Pul_693464584_75 | 15.7853 | 78.0725 | 0.7500 | 0 | -2.1200 |  |
| Pul | damaged now | 5 | Pul_-714521376_48 | 15.8144 | 78.0704 | 0.4800 | 1 | -1.6900 |  |
| Pul | at risk (healthy now) | 1 | Pul_752319359_61 | 15.8132 | 78.1004 | 0.6100 | 0 | 0.1100 | 0.6400 |
| Pul | at risk (healthy now) | 2 | Pul_-1049707192_96 | 15.7722 | 78.0841 | 0.9600 | 1 | 0.1400 | 0.5700 |
| Pul | at risk (healthy now) | 3 | Pul_94858241_37 | 15.7765 | 78.0924 | 0.3700 | 1 | 0.2300 | 0.4800 |
| Pul | at risk (healthy now) | 4 | Pul_1670711306_77 | 15.8139 | 78.0934 | 0.7700 | 0 | 0.6600 | 0.2400 |
| Pul | at risk (healthy now) | 5 | Pul_894423709_38 | 15.8234 | 78.0878 | 0.3800 | 0 | 0.9800 | 0.1800 |
