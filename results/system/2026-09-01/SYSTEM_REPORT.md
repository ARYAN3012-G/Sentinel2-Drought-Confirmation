# Drought system report - 2026-09-01

Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.

## Status per site

| site | SPEI30 | SPEI90 | ALARM | median_SVI | fields_below_normal | CONFIRMED | status |
|---|---|---|---|---|---|---|---|
| Som | -1.3700 | -1.8800 | True | -1.1200 | 60% | True | DROUGHT: alarm confirmed by crops |
| Lep | -1.1400 | -1.7000 | True | 0.0100 | 0% | False | WATCH: weather alarm, crops not yet stressed |
| Cho | -1.1400 | -1.7000 | True | -0.9200 | 50% | False | WATCH: weather alarm, crops not yet stressed |
| Sira | -1.0900 | -1.3900 | True | -1.5900 | 100% | True | DROUGHT: alarm confirmed by crops |
| Ped | -1.3800 | -1.6600 | True | 1.3600 | 33% | False | WATCH: weather alarm, crops not yet stressed |
| Din | -1.1200 | -1.3500 | True | 0.3300 | 0% | False | WATCH: weather alarm, crops not yet stressed |
| Bal | -1.0600 | -1.3300 | True |  |  | False | WATCH: weather alarm, crops not yet stressed |
| Pul | -1.0700 | -1.2500 | True | -0.5700 | 50% | False | WATCH: weather alarm, crops not yet stressed |

## Stage 1: weather

| site | weather_date | SPEI30 | SPEI90 | forecast_+7d | forecast_+15d | forecast_+30d | ALARM |
|---|---|---|---|---|---|---|---|
| Som | 2026-09-01 | -1.3700 | -1.8800 | Severe (50%) | Moderate (66%) | Moderate (52%) | True |
| Lep | 2026-09-01 | -1.1400 | -1.7000 | Severe (53%) | Moderate (78%) | Moderate (61%) | True |
| Cho | 2026-09-01 | -1.1400 | -1.7000 | Severe (53%) | Moderate (78%) | Moderate (61%) | True |
| Sira | 2026-09-01 | -1.0900 | -1.3900 | Moderate (79%) | Moderate (89%) | Moderate (60%) | True |
| Ped | 2026-09-01 | -1.3800 | -1.6600 | Severe (71%) | Moderate (73%) | Moderate (57%) | True |
| Din | 2026-09-01 | -1.1200 | -1.3500 | Severe (64%) | Moderate (70%) | Moderate (46%) | True |
| Bal | 2026-09-01 | -1.0600 | -1.3300 | Moderate (50%) | Moderate (67%) | Moderate (46%) | True |
| Pul | 2026-09-01 | -1.0700 | -1.2500 | Moderate (57%) | Moderate (80%) | Moderate (59%) | True |

ALARM = SPEI-30 < -1.0 on the date, or the +15-day forecast class is Severe. DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and SPEI-90 < -1.0.

## Stage 2: satellite

| site | rainfed_fields_with_data | median_SVI | fields_below_normal | fields_severe | CONFIRMED |
|---|---|---|---|---|---|
| Som | 5 | -1.1200 | 60% | 40% | True |
| Lep | 1 | 0.0100 | 0% | 0% | False |
| Cho | 4 | -0.9200 | 50% | 0% | False |
| Sira | 2 | -1.5900 | 100% | 50% | True |
| Ped | 3 | 1.3600 | 33% | 33% | False |
| Din | 1 | 0.3300 | 0% | 0% | False |
| Bal | 0 |  |  |  | False |
| Pul | 4 | -0.5700 | 50% | 25% | False |

CONFIRMED = median rainfed SVI < -1.

## Stage 3: fields to fly

Up to 5 fields per site and list. Map: `fields_to_fly.kml` (open in Google Earth; red = damaged now, orange = at risk). Table: `fields_to_fly.csv`.

| site | reason | rank | field_id | lat | lon | area_ha | irrigated | SVI_now | onset_risk_15d |
|---|---|---|---|---|---|---|---|---|---|
| Som | damaged now | 1 | Som_210526987_57 | 14.0015 | 77.6009 | 0.5700 | 0 | -1.7300 |  |
| Som | damaged now | 2 | Som_2097648969_50 | 14.0232 | 77.6041 | 0.5000 | 0 | -1.6800 |  |
| Som | damaged now | 3 | Som_1700228554_34 | 14.0118 | 77.5916 | 0.3400 | 0 | -1.1200 |  |
| Lep | at risk (healthy now) | 1 | Lep_-171177260_37 | 13.8123 | 77.6180 | 0.3700 | 0 | 0.0100 | 0.7200 |
| Cho | damaged now | 1 | Cho_1817686041_58 | 13.8261 | 77.5736 | 0.5800 | 0 | -1.2300 |  |
| Cho | damaged now | 2 | Cho_-113624334_61 | 13.8282 | 77.5753 | 0.6100 | 0 | -1.1000 |  |
| Sira | damaged now | 1 | Sira_1795621425_56 | 13.7735 | 76.9867 | 0.5600 | 0 | -1.8600 |  |
| Sira | damaged now | 2 | Sira_1383822971_35 | 13.7751 | 76.9837 | 0.3500 | 0 | -1.3200 |  |
| Ped | damaged now | 1 | Ped_-430971332_39 | 15.8054 | 77.2495 | 0.3900 | 0 | -1.6900 |  |
| Ped | at risk (healthy now) | 1 | Ped_-608278541_33 | 15.7668 | 77.2429 | 0.3300 | 1 | 2.8100 | 0.2700 |
| Ped | at risk (healthy now) | 2 | Ped_-2133758636_51 | 15.7657 | 77.2410 | 0.5100 | 1 | 0.4100 | 0.2700 |
| Ped | at risk (healthy now) | 3 | Ped_-1473159057_38 | 15.7563 | 77.2549 | 0.3800 | 0 | 1.3600 | 0.1900 |
| Ped | at risk (healthy now) | 4 | Ped_-503391457_56 | 15.7869 | 77.2614 | 0.5600 | 0 | 3.3000 | 0.1300 |
| Din | at risk (healthy now) | 1 | Din_-1012988290_83 | 15.7492 | 78.0591 | 0.8300 | 0 | 0.3300 | 0.4100 |
| Pul | damaged now | 1 | Pul_-1093009035_51 | 15.7786 | 78.0989 | 0.5100 | 0 | -2.3000 |  |
| Pul | damaged now | 2 | Pul_1815014780_35 | 15.7894 | 78.0909 | 0.3500 | 1 | -2.1700 |  |
| Pul | damaged now | 3 | Pul_-684475182_101 | 15.7971 | 78.0964 | 1.0100 | 1 | -1.2400 |  |
| Pul | damaged now | 4 | Pul_-1723364789_65 | 15.7849 | 78.0875 | 0.6500 | 0 | -1.1700 |  |
| Pul | at risk (healthy now) | 1 | Pul_-1520453160_52 | 15.7829 | 78.0975 | 0.5200 | 1 | 0.2400 | 0.8300 |
| Pul | at risk (healthy now) | 2 | Pul_-2111834955_52 | 15.7738 | 78.0837 | 0.5200 | 0 | 0.0300 | 0.8300 |
| Pul | at risk (healthy now) | 3 | Pul_1878893000_41 | 15.7790 | 78.0999 | 0.4100 | 0 | 0.0800 | 0.5300 |
