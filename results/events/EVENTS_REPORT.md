# Drought events and label checks

## A. Drought seasons (2023, 2026 dry; 2025 normal)

Rain = Jun-Oct total vs 1979-2011 normal (AgERA5). SVI < 0 = greener-than-normal is lost. Field shares: rainfed sampled fields with mean Sep-Oct SVI < -1 (below normal) or < -1.5 (severe). official_declaration = Andhra Pradesh G.O. drought mandal lists (data/official/; Karnataka not checked).

| site | year | rain_jun_oct_mm | rain_vs_normal_% | SPEI30_aug_oct | SPEI90_aug_oct | SVI_rainfed_aug_nov | SVI_irrigated_aug_nov | rainfed_fields_below_normal_% | rainfed_fields_severe_% | rainfed_fields_n | mandal | official_declaration |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bal | 2023 | 570 | -6 | 0.0600 | 0.4300 | -0.8000 | -0.0300 | 45 | 25 | 20 | Kurnool Urban (likely) | Severe |
| Bal | 2025 | 817 | 35 | 0.9900 | 1.2200 | 0.7500 | 0.6500 | 5 | 0 | 20 |  | not checked (rain above normal) |
| Bal | 2026 | 344 | -43 | -1.0600 | -1.3300 | -0.9000 | -0.1600 | 55 | 15 | 20 | Kurnool Urban (likely) | Severe |
| Cho | 2023 | 350 | -31 | -1.0400 | -0.3600 | -1.4400 | -1.1200 | 50 | 35 | 20 | Lepakshi | Moderate |
| Cho | 2025 | 568 | 12 | 0.5000 | 1.2800 | 0.8800 | 0.4900 | 5 | 5 | 20 |  | not checked (rain above normal) |
| Cho | 2026 | 300 | -41 | -1.3800 | -1.6900 | -1.7100 | -1.2500 | 70 | 50 | 20 | Lepakshi | Severe |
| Din | 2023 | 492 | -9 | -0.0900 | 0.5500 | -0.9100 | -0.6500 | 40 | 5 | 20 | Kurnool Rural | Not declared |
| Din | 2025 | 758 | 39 | 1.1000 | 1.4600 | 0.7600 | 0.2400 | 5 | 0 | 20 |  | not checked (rain above normal) |
| Din | 2026 | 273 | -50 | -1.2700 | -1.4500 | -1.1900 | -0.6900 | 45 | 25 | 20 | Kurnool Rural | Severe |
| Lep | 2023 | 350 | -31 | -1.0400 | -0.3600 | -0.6900 | -0.4700 | 20 | 5 | 20 | Lepakshi | Moderate |
| Lep | 2025 | 568 | 12 | 0.5000 | 1.2800 | 0.3300 | 0.0000 | 5 | 5 | 20 |  | not checked (rain above normal) |
| Lep | 2026 | 300 | -41 | -1.3800 | -1.6900 | -1.4900 | -1.9400 | 45 | 35 | 20 | Lepakshi | Severe |
| Ped | 2023 | 495 | -10 | -0.1400 | 0.5700 | -0.8000 | -0.2200 | 25 | 10 | 20 | Adoni / Peddakadubur border | Moderate (Adoni) / Severe (Peddakadubur) |
| Ped | 2025 | 756 | 37 | 1.1300 | 1.7100 | 0.1800 | -0.5500 | 0 | 0 | 20 |  | not checked (rain above normal) |
| Ped | 2026 | 239 | -57 | -1.6300 | -1.7300 | -0.2200 | -0.3000 | 20 | 10 | 20 | Adoni / Peddakadubur border | Severe (Adoni) / Not declared (Peddakadubur) |
| Pul | 2023 | 554 | -11 | -0.0600 | 0.2700 | -0.3700 | -0.2400 | 20 | 10 | 20 | Kurnool Urban (likely) | Severe |
| Pul | 2025 | 724 | 17 | 0.7600 | 0.9800 | 0.4500 | 0.2400 | 5 | 5 | 20 |  | not checked (rain above normal) |
| Pul | 2026 | 351 | -43 | -1.1800 | -1.3400 | -0.6300 | -0.6600 | 25 | 15 | 20 | Kurnool Urban (likely) | Severe |
| Sira | 2023 | 431 | -23 | -0.8900 | -0.1000 | -1.5300 | -0.0800 | 80 | 60 | 20 | Sira taluk | Unknown |
| Sira | 2025 | 649 | 15 | 0.5000 | 1.3100 | 0.1900 | 0.2300 | 5 | 0 | 20 |  | not checked (rain above normal) |
| Sira | 2026 | 390 | -31 | -1.2600 | -1.5200 | -1.2700 | -0.6900 | 55 | 45 | 20 | Sira taluk | Unknown |
| Som | 2023 | 283 | -36 | -1.0200 | -0.4100 | -0.7200 | -0.5600 | 45 | 25 | 20 | Somandepalli | Moderate |
| Som | 2025 | 486 | 11 | 0.4700 | 1.1700 | 0.9700 | 0.7700 | 5 | 0 | 20 |  | not checked (rain above normal) |
| Som | 2026 | 209 | -52 | -1.5500 | -1.8000 | -2.2000 | -1.2300 | 85 | 75 | 20 | Somandepalli | Severe |

## B. Irrigation label check

Drought SVI = mean SVI in Aug-Nov of 2023 and 2026. A real irrigated field should stay above its site's rainfed median. Doubtful = as low as the rainfed median AND as weather-driven (Spearman rho with SPEI-90) as the rainfed median.

| site | irrigated_fields | doubtful | drought_SVI_rainfed_median | drought_SVI_irrigated_median | rho_rainfed_median | rho_irrigated_median | doubtful_field_ids |
|---|---|---|---|---|---|---|---|
| Bal | 10 | 0 | -0.8800 | -0.0400 | 0.4800 | 0.2300 |  |
| Cho | 10 | 0 | -1.5100 | -1.3100 | 0.5800 | 0.6500 |  |
| Din | 10 | 0 | -1.0600 | -0.5300 | 0.6300 | 0.2200 |  |
| Lep | 10 | 2 | -1.0700 | -0.8300 | 0.5800 | 0.4700 | Lep_-1716647714_53 Lep_105608633_69 |
| Ped | 10 | 2 | -0.6600 | -0.0800 | 0.2900 | 0.1700 | Ped_-1627922839_44 Ped_1951979809_83 |
| Pul | 10 | 3 | -0.4500 | -0.1500 | 0.2100 | 0.1400 | Pul_-714521376_48 Pul_1665428792_76 Pul_1815014780_35 |
| Sira | 10 | 1 | -1.6300 | -0.1100 | 0.5500 | 0.2200 | Sira_1105854812_72 |
| Som | 10 | 1 | -1.3900 | -0.9600 | 0.5200 | 0.3200 | Som_1128382370_72 |

## C. Lag robustness (rainfed fields, site median SVI, one year left out at a time)

If the best scale/lag changes when one year is left out, that year drives the result.

| left_out_year | Bal | Cho | Din | Lep | Ped | Pul | Sira | Som |
|---|---|---|---|---|---|---|---|---|
| 2019 | 0 | 0 | 0 | 0 | 5 | 5 | 0 | 80 |
| 2020 | 0 | 10 | 0 | 0 | 5 | 0 | 5 | 80 |
| 2021 | 15 | 10 | 0 | 0 | 0 | 0 | 0 | 80 |
| 2022 | 5 | 10 | 0 | 0 | 5 | 5 | 0 | 80 |
| 2023 | 45 | 10 | 0 | 0 | 5 | 90 | 20 | 80 |
| 2024 | 5 | 15 | 0 | 0 | 0 | 90 | 0 | 80 |
| 2025 | 5 | 5 | 0 | 0 | 5 | 35 | 0 | 0 |
| 2026 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 80 |
| none | 0 | 10 | 0 | 0 | 5 | 0 | 0 | 80 |

| site | left_out_year | best_rho | best_SPEI | best_lag_days |
|---|---|---|---|---|
| Bal | none | 0.5000 | 30 | 0 |
| Bal | 2019 | 0.5500 | 30 | 0 |
| Bal | 2020 | 0.5600 | 30 | 0 |
| Bal | 2021 | 0.5600 | 90 | 15 |
| Bal | 2022 | 0.5700 | 30 | 5 |
| Bal | 2023 | 0.4000 | 30 | 45 |
| Bal | 2024 | 0.5700 | 30 | 5 |
| Bal | 2025 | 0.5600 | 30 | 5 |
| Bal | 2026 | 0.3900 | 30 | 0 |
| Cho | none | 0.7300 | 90 | 10 |
| Cho | 2019 | 0.7200 | 90 | 0 |
| Cho | 2020 | 0.7300 | 90 | 10 |
| Cho | 2021 | 0.7300 | 90 | 10 |
| Cho | 2022 | 0.8000 | 90 | 10 |
| Cho | 2023 | 0.6200 | 90 | 10 |
| Cho | 2024 | 0.7500 | 90 | 15 |
| Cho | 2025 | 0.8300 | 90 | 5 |
| Cho | 2026 | 0.6500 | 90 | 10 |
| Din | none | 0.5800 | 60 | 0 |
| Din | 2019 | 0.5900 | 60 | 0 |
| Din | 2020 | 0.5600 | 30 | 0 |
| Din | 2021 | 0.7600 | 90 | 0 |
| Din | 2022 | 0.5800 | 60 | 0 |
| Din | 2023 | 0.5700 | 60 | 0 |
| Din | 2024 | 0.6100 | 30 | 0 |
| Din | 2025 | 0.6000 | 60 | 0 |
| Din | 2026 | 0.5200 | 60 | 0 |
| Lep | none | 0.5400 | 90 | 0 |
| Lep | 2019 | 0.5300 | 90 | 0 |
| Lep | 2020 | 0.5900 | 90 | 0 |
| Lep | 2021 | 0.5600 | 90 | 0 |
| Lep | 2022 | 0.6400 | 90 | 0 |
| Lep | 2023 | 0.4200 | 90 | 0 |
| Lep | 2024 | 0.5400 | 90 | 0 |
| Lep | 2025 | 0.6000 | 90 | 0 |
| Lep | 2026 | 0.4500 | 90 | 0 |
| Ped | none | 0.6200 | 30 | 5 |
| Ped | 2019 | 0.6000 | 30 | 5 |
| Ped | 2020 | 0.6300 | 30 | 5 |
| Ped | 2021 | 0.6400 | 30 | 0 |
| Ped | 2022 | 0.6400 | 30 | 5 |
| Ped | 2023 | 0.5900 | 30 | 5 |
| Ped | 2024 | 0.6100 | 30 | 0 |
| Ped | 2025 | 0.6000 | 30 | 5 |
| Ped | 2026 | 0.6400 | 30 | 0 |
| Pul | none | 0.2900 | 60 | 0 |
| Pul | 2019 | 0.3200 | 30 | 5 |
| Pul | 2020 | 0.4800 | 60 | 0 |
| Pul | 2021 | 0.3800 | 60 | 0 |
| Pul | 2022 | 0.3300 | 60 | 5 |
| Pul | 2023 | 0.2100 | 90 | 90 |
| Pul | 2024 | 0.3900 | 90 | 90 |
| Pul | 2025 | 0.2400 | 30 | 35 |
| Pul | 2026 | 0.2200 | 60 | 0 |
| Sira | none | 0.6000 | 90 | 0 |
| Sira | 2019 | 0.6100 | 90 | 0 |
| Sira | 2020 | 0.6100 | 90 | 5 |
| Sira | 2021 | 0.6700 | 90 | 0 |
| Sira | 2022 | 0.6800 | 90 | 0 |
| Sira | 2023 | 0.4700 | 90 | 20 |
| Sira | 2024 | 0.6200 | 90 | 0 |
| Sira | 2025 | 0.6400 | 90 | 0 |
| Sira | 2026 | 0.5200 | 90 | 0 |
| Som | none | 0.6800 | 90 | 80 |
| Som | 2019 | 0.6400 | 90 | 80 |
| Som | 2020 | 0.7700 | 90 | 80 |
| Som | 2021 | 0.7300 | 90 | 80 |
| Som | 2022 | 0.6900 | 90 | 80 |
| Som | 2023 | 0.6500 | 90 | 80 |
| Som | 2024 | 0.6900 | 90 | 80 |
| Som | 2025 | 0.6600 | 90 | 0 |
| Som | 2026 | 0.5600 | 90 | 80 |
