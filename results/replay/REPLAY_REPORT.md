# Operational replay of the integrated system, kharif 2023-2026

Every 5 days, 1 Jun - 30 Nov, with weather 7 days late (AgERA5) and satellite 2 days late; alarm = SPEI-30 < -1.0 or a Severe +15-day forecast; confirmed = median rainfed SVI < -1 from >= 5 fields. No crop model is used, so all years are out-of-sample. Official = AP G.O. drought mandal lists (Sira/Karnataka and the Adoni-Peddakadubur border site are excluded where unknown or ambiguous).

## Season summary per site

| year | site | official | official_level | GO_date | first_alarm | first_confirmed | confirmed_dates | dates_with_satellite | confirmed_before_GO | lead_days_before_GO |
|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | Bal | Severe | 2.0000 | 2023-10-31 | 2023-06-01 | 2023-10-29 | 4 | 18 | True | 2.0000 |
| 2023 | Cho | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-19 | 7 | 14 | True | 12.0000 |
| 2023 | Din | Not declared | 0.0000 | 2023-10-31 | 2023-06-01 | 2023-09-04 | 12 | 18 | True | 57.0000 |
| 2023 | Lep | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-24 | 5 | 15 | True | 7.0000 |
| 2023 | Ped | Moderate (Adoni) / Severe (Peddakadubur) |  | 2023-10-31 | 2023-06-16 | None | 0 | 17 | False |  |
| 2023 | Pul | Severe | 2.0000 | 2023-10-31 | 2023-06-01 | 2023-11-03 | 2 | 18 | False |  |
| 2023 | Sira | Unknown |  | 2023-10-31 | 2023-06-26 | 2023-09-09 | 15 | 27 | True | 52.0000 |
| 2023 | Som | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-29 | 5 | 15 | True | 2.0000 |
| 2024 | Bal | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 19 | False |  |
| 2024 | Cho | Not declared | 0.0000 | 2024-10-29 | 2024-10-09 | None | 0 | 21 | False |  |
| 2024 | Din | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 22 | False |  |
| 2024 | Lep | Not declared | 0.0000 | 2024-10-29 | 2024-10-09 | None | 0 | 20 | False |  |
| 2024 | Ped | Not declared (Adoni) / Moderate (Peddakadubur) |  | 2024-10-29 | None | None | 0 | 20 | False |  |
| 2024 | Pul | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 21 | False |  |
| 2024 | Sira | Unknown |  | 2024-10-29 | 2024-09-29 | None | 0 | 33 | False |  |
| 2024 | Som | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 22 | False |  |
| 2025 | Bal | Not declared | 0.0000 | 2025-10-31 | None | None | 0 | 17 | False |  |
| 2025 | Cho | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None | 0 | 18 | False |  |
| 2025 | Din | Not declared | 0.0000 | 2025-10-31 | 2025-10-19 | None | 0 | 16 | False |  |
| 2025 | Lep | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None | 0 | 16 | False |  |
| 2025 | Ped | Not declared | 0.0000 | 2025-10-31 | 2025-10-19 | None | 0 | 16 | False |  |
| 2025 | Pul | Not declared | 0.0000 | 2025-10-31 | None | None | 0 | 23 | False |  |
| 2025 | Sira | Unknown |  | 2025-10-31 | 2025-09-24 | None | 0 | 30 | False |  |
| 2025 | Som | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None | 0 | 18 | False |  |
| 2026 | Bal | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-09-09 | 3 | 11 | True | 22.0000 |
| 2026 | Cho | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-10-04 | 5 | 12 | False |  |
| 2026 | Din | Severe | 2.0000 | 2026-10-01 | 2026-07-01 | 2026-09-09 | 7 | 16 | True | 22.0000 |
| 2026 | Lep | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-09-24 | 4 | 15 | True | 7.0000 |
| 2026 | Ped | Severe (Adoni) / Not declared (Peddakadubur) |  | 2026-10-01 | 2026-07-21 | None | 0 | 11 | False |  |
| 2026 | Pul | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-10-19 | 1 | 14 | False |  |
| 2026 | Sira | Unknown |  | 2026-10-01 | 2026-07-26 | 2026-07-26 | 14 | 26 | True | 67.0000 |
| 2026 | Som | Severe | 2.0000 | 2026-10-01 | 2026-07-16 | 2026-10-14 | 4 | 14 | False |  |

## Agreement with official declarations (site-seasons with a known declaration)

| official | False | True |
|---|---|---|
| moderate | 3 | 3 |
| not declared | 10 | 1 |
| severe | 0 | 8 |

Declared site-seasons confirmed by the system before the G.O. date: 7 of 14; median lead 7 days.

Small sample (one area per mandal, 4 seasons): read as case evidence, not a statistical test.

## Sensitivity to the confirmation threshold (robustness check; the rule stays SVI < -1)

| confirmation threshold (SVI <) | severe confirmed | moderate confirmed | not declared but confirmed | declared, confirmed before G.O. |
|---|---|---|---|---|
| -1.0000 | 8/8 | 3/6 | 1/11 | 7/14 |
| -0.7500 | 8/8 | 3/6 | 1/11 | 9/14 |
| -1.2500 | 5/8 | 3/6 | 1/11 | 5/14 |
