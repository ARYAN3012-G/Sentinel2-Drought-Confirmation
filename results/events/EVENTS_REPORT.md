# Drought events and label checks

## A. Drought seasons (2023, 2026 dry; 2025 normal)

Rain = Jun-Oct total vs 1979-2011 normal (AgERA5). SVI < 0 = greener-than-normal is lost. Field shares: rainfed sampled fields with mean Sep-Oct SVI < -1 (below normal) or < -1.5 (severe). official_declaration = Andhra Pradesh G.O. drought mandal lists (data/official/; Karnataka not checked).

| site | year | rain_jun_oct_mm | rain_vs_normal_% | SPEI30_aug_oct | SPEI90_aug_oct | SVI_rainfed_aug_nov | SVI_irrigated_aug_nov | rainfed_fields_below_normal_% | rainfed_fields_severe_% | rainfed_fields_n | mandal | official_declaration |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bal | 2023 | 570 | -6 | 0.0600 | 0.4300 | -1.1300 | -0.0300 | 38 | 24 | 21 | Kurnool Urban (likely) | Severe |
| Bal | 2025 | 817 | 35 | 0.9900 | 1.2200 | 0.2500 | 0.1900 | 10 | 0 | 21 | Kurnool Urban (likely) | Not declared |
| Bal | 2026 | 344 | -43 | -1.0600 | -1.3300 | -1.0300 | -0.1700 | 33 | 14 | 21 | Kurnool Urban (likely) | Severe |
| Cho | 2023 | 350 | -31 | -1.0400 | -0.3600 | -1.4600 | -0.9400 | 24 | 24 | 17 | Lepakshi | Moderate |
| Cho | 2025 | 568 | 12 | 0.5000 | 1.2800 | 0.5000 | 0.2900 | 6 | 6 | 17 | Lepakshi | Moderate |
| Cho | 2026 | 300 | -41 | -1.3800 | -1.6900 | -1.4000 | -1.7800 | 59 | 35 | 17 | Lepakshi | Severe |
| Din | 2023 | 492 | -9 | -0.0900 | 0.5500 | -1.5700 | -0.1300 | 53 | 26 | 19 | Kurnool Rural | Not declared |
| Din | 2025 | 758 | 39 | 1.1000 | 1.4600 | 0.2700 | 0.6800 | 5 | 0 | 19 | Kurnool Rural | Not declared |
| Din | 2026 | 273 | -50 | -1.2700 | -1.4500 | -1.2700 | -1.3700 | 68 | 37 | 19 | Kurnool Rural | Severe |
| Lep | 2023 | 350 | -31 | -1.0400 | -0.3600 | -1.2400 | -0.0100 | 28 | 17 | 18 | Lepakshi | Moderate |
| Lep | 2025 | 568 | 12 | 0.5000 | 1.2800 | 0.3200 | -0.3300 | 6 | 6 | 18 | Lepakshi | Moderate |
| Lep | 2026 | 300 | -41 | -1.3800 | -1.6900 | -1.2200 | -0.6400 | 56 | 39 | 18 | Lepakshi | Severe |
| Ped | 2023 | 495 | -10 | -0.1500 | 0.5700 | -0.5600 | -0.6000 | 40 | 15 | 20 | Adoni / Peddakadubur border | Moderate (Adoni) / Severe (Peddakadubur) |
| Ped | 2025 | 756 | 37 | 1.1300 | 1.7100 | 0.0900 | 0.0800 | 5 | 0 | 20 | Adoni / Peddakadubur border | Not declared |
| Ped | 2026 | 239 | -57 | -1.6300 | -1.7400 | -0.3100 | 0.1100 | 25 | 5 | 20 | Adoni / Peddakadubur border | Severe (Adoni) / Not declared (Peddakadubur) |
| Pul | 2023 | 570 | -6 | 0.0600 | 0.4300 | -0.1900 | -0.2600 | 30 | 20 | 20 | Kurnool Urban (likely) | Severe |
| Pul | 2025 | 817 | 35 | 0.9900 | 1.2200 | 0.0400 | 0.6400 | 5 | 0 | 20 | Kurnool Urban (likely) | Not declared |
| Pul | 2026 | 344 | -43 | -1.0600 | -1.3300 | -0.6500 | -0.3200 | 30 | 10 | 20 | Kurnool Urban (likely) | Severe |
| Sira | 2023 | 431 | -23 | -0.8900 | -0.1000 | -1.9500 | -0.9300 | 83 | 57 | 23 | Sira taluk | Unknown |
| Sira | 2025 | 649 | 15 | 0.5000 | 1.3100 | 0.1200 | 0.1300 | 0 | 0 | 23 | Sira taluk | Unknown |
| Sira | 2026 | 390 | -31 | -1.2600 | -1.5200 | -1.5900 | -0.6000 | 70 | 57 | 23 | Sira taluk | Unknown |
| Som | 2023 | 283 | -36 | -1.0200 | -0.4100 | -0.8900 | -0.3000 | 30 | 20 | 20 | Somandepalli | Moderate |
| Som | 2025 | 486 | 11 | 0.4700 | 1.1700 | 0.8200 | 0.8200 | 0 | 0 | 20 | Somandepalli | Moderate |
| Som | 2026 | 209 | -52 | -1.5500 | -1.8000 | -1.7700 | -0.7200 | 85 | 65 | 20 | Somandepalli | Severe |

## B. Irrigation label check

Drought SVI = mean SVI in Aug-Nov of 2023 and 2026. A real irrigated field should stay above its site's rainfed median. Doubtful = as low as the rainfed median AND as weather-driven (Spearman rho with SPEI-90) as the rainfed median.

| site | irrigated_fields | doubtful | drought_SVI_rainfed_median | drought_SVI_irrigated_median | rho_rainfed_median | rho_irrigated_median | doubtful_field_ids |
|---|---|---|---|---|---|---|---|
| Bal | 9 | 0 | -1.1800 | -0.2200 | 0.4700 | 0.1000 |  |
| Cho | 13 | 2 | -1.4300 | -1.0900 | 0.6100 | 0.4100 | Cho_-1917245961_93 Cho_1611879882_52 |
| Din | 11 | 1 | -1.3600 | -0.7000 | 0.5600 | 0.4000 | Din_-498760764_47 |
| Lep | 11 | 2 | -0.9900 | -0.5100 | 0.5700 | 0.5100 | Lep_-258478907_34 Lep_-612546177_81 |
| Ped | 10 | 3 | -0.4500 | -0.3400 | 0.2000 | 0.2300 | Ped_-1577668363_65 Ped_1032501944_59 Ped_1839477079_95 |
| Pul | 10 | 3 | -0.4800 | -0.2300 | 0.1400 | 0.2500 | Pul_-1316884246_59 Pul_-1367791998_62 Pul_491465183_54 |
| Sira | 7 | 0 | -1.6400 | -0.7800 | 0.6200 | 0.4800 |  |
| Som | 10 | 0 | -1.2400 | -0.5000 | 0.4300 | 0.2600 |  |

## C. Lag robustness (rainfed fields, site median SVI, one year left out at a time)

If the best scale/lag changes when one year is left out, that year drives the result.

| left_out_year | Bal | Cho | Din | Lep | Ped | Pul | Sira | Som |
|---|---|---|---|---|---|---|---|---|
| 2019 | 0 | 0 | 5 | 0 | 15 | 5 | 0 | 15 |
| 2020 | 5 | 0 | 0 | 0 | 15 | 0 | 0 | 75 |
| 2021 | 0 | 5 | 20 | 5 | 0 | 5 | 0 | 50 |
| 2022 | 5 | 0 | 5 | 0 | 20 | 5 | 0 | 75 |
| 2023 | 5 | 5 | 5 | 0 | 15 | 0 | 0 | 75 |
| 2024 | 5 | 0 | 5 | 0 | 20 | 5 | 0 | 90 |
| 2025 | 5 | 0 | 5 | 0 | 15 | 0 | 0 | 45 |
| 2026 | 0 | 5 | 5 | 0 | 0 | 5 | 0 | 75 |
| none | 5 | 0 | 5 | 0 | 15 | 5 | 0 | 75 |

| site | left_out_year | best_rho | best_SPEI | best_lag_days |
|---|---|---|---|---|
| Bal | none | 0.5600 | 30 | 5 |
| Bal | 2019 | 0.6000 | 30 | 0 |
| Bal | 2020 | 0.5300 | 30 | 5 |
| Bal | 2021 | 0.6300 | 30 | 0 |
| Bal | 2022 | 0.6200 | 30 | 5 |
| Bal | 2023 | 0.4800 | 30 | 5 |
| Bal | 2024 | 0.6000 | 30 | 5 |
| Bal | 2025 | 0.5200 | 30 | 5 |
| Bal | 2026 | 0.5000 | 30 | 0 |
| Cho | none | 0.8300 | 90 | 0 |
| Cho | 2019 | 0.8600 | 90 | 0 |
| Cho | 2020 | 0.8300 | 90 | 0 |
| Cho | 2021 | 0.8400 | 90 | 5 |
| Cho | 2022 | 0.8300 | 90 | 0 |
| Cho | 2023 | 0.7800 | 90 | 5 |
| Cho | 2024 | 0.8200 | 90 | 0 |
| Cho | 2025 | 0.8800 | 90 | 0 |
| Cho | 2026 | 0.7700 | 90 | 5 |
| Din | none | 0.6500 | 90 | 5 |
| Din | 2019 | 0.6700 | 90 | 5 |
| Din | 2020 | 0.6200 | 90 | 0 |
| Din | 2021 | 0.7400 | 90 | 20 |
| Din | 2022 | 0.6800 | 90 | 5 |
| Din | 2023 | 0.6200 | 60 | 5 |
| Din | 2024 | 0.6600 | 90 | 5 |
| Din | 2025 | 0.7000 | 90 | 5 |
| Din | 2026 | 0.5900 | 90 | 5 |
| Lep | none | 0.6300 | 90 | 0 |
| Lep | 2019 | 0.6500 | 90 | 0 |
| Lep | 2020 | 0.6100 | 90 | 0 |
| Lep | 2021 | 0.6500 | 90 | 5 |
| Lep | 2022 | 0.7700 | 90 | 0 |
| Lep | 2023 | 0.5000 | 90 | 0 |
| Lep | 2024 | 0.5800 | 90 | 0 |
| Lep | 2025 | 0.7100 | 90 | 0 |
| Lep | 2026 | 0.5200 | 90 | 0 |
| Ped | none | 0.4600 | 30 | 15 |
| Ped | 2019 | 0.4900 | 30 | 15 |
| Ped | 2020 | 0.4600 | 30 | 15 |
| Ped | 2021 | 0.4400 | 60 | 0 |
| Ped | 2022 | 0.5000 | 30 | 20 |
| Ped | 2023 | 0.3300 | 30 | 15 |
| Ped | 2024 | 0.4800 | 30 | 20 |
| Ped | 2025 | 0.4200 | 30 | 15 |
| Ped | 2026 | 0.5600 | 60 | 0 |
| Pul | none | 0.4900 | 60 | 5 |
| Pul | 2019 | 0.5000 | 60 | 5 |
| Pul | 2020 | 0.3900 | 30 | 0 |
| Pul | 2021 | 0.6300 | 60 | 5 |
| Pul | 2022 | 0.5300 | 60 | 5 |
| Pul | 2023 | 0.4300 | 30 | 0 |
| Pul | 2024 | 0.5000 | 60 | 5 |
| Pul | 2025 | 0.5300 | 30 | 0 |
| Pul | 2026 | 0.4100 | 60 | 5 |
| Sira | none | 0.6000 | 90 | 0 |
| Sira | 2019 | 0.6900 | 90 | 0 |
| Sira | 2020 | 0.5900 | 90 | 0 |
| Sira | 2021 | 0.6800 | 90 | 0 |
| Sira | 2022 | 0.6400 | 90 | 0 |
| Sira | 2023 | 0.4700 | 60 | 0 |
| Sira | 2024 | 0.6000 | 90 | 0 |
| Sira | 2025 | 0.6300 | 90 | 0 |
| Sira | 2026 | 0.5000 | 90 | 0 |
| Som | none | 0.5800 | 30 | 75 |
| Som | 2019 | 0.5600 | 90 | 15 |
| Som | 2020 | 0.5900 | 30 | 75 |
| Som | 2021 | 0.6300 | 60 | 50 |
| Som | 2022 | 0.5900 | 30 | 75 |
| Som | 2023 | 0.5500 | 30 | 75 |
| Som | 2024 | 0.6200 | 90 | 90 |
| Som | 2025 | 0.7700 | 60 | 45 |
| Som | 2026 | 0.4600 | 30 | 75 |
