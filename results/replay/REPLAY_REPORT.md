# Operational replay of the integrated system, kharif 2023-2026

Every 5 days from 1 Jun to 30 Nov, or to the end of the data, with weather 7 days late (AgERA5) and satellite 2 days late; weather older than 5 days is not used. Alarm = SPEI-30 < -1.0 or a Severe +15-day forecast; confirmed = median rainfed SVI < -1 from >= 5 fields. No crop model is used.

**Data ends.** 2026: partial season, last issue date 2026-10-24.

**Retrospective vs prospective.** The farmland mask, field segments and irrigation flag were derived from 2019-2023 imagery, so 2023 is RETROSPECTIVE (field selection saw that season; the SVI normal excludes 2023). 2024-2026 are PROSPECTIVE with respect to every fitted or selected component.

**Thresholds fixed in advance.** SPEI < -1 (moderate drought, McKee et al. 1993 / WMO convention), SVI < -1 (one standard deviation below the field's normal), >= 5 fields and the data delays were set in run_system.py before this replay was written; they were not tuned on it.

## Agreement with official declarations, site-seasons

| site-seasons | severe: confirmed (eventually) | severe: confirmed before order | moderate: confirmed (eventually) | moderate: confirmed before order | not declared: confirmed (false alarm) |
|---|---|---|---|---|---|
| 2023 (retrospective) | 3/3 | 2/3 | 3/3 | 3/3 | 1/1 |
| 2024-2026 (prospective) | 6/6 | 3/6 | 0/3 | 0/3 | 0/10 |
| all | 9/9 | 5/9 | 3/6 | 3/6 | 1/11 |

Median lead before the order, declared site-seasons confirmed in advance: 7 days.

## Each official decision counted once (mandal x season)

Lepakshi and Cholasamudram lie in Lepakshi mandal and share one weather cell; Balaji Villas and Pullaiah lie in Kurnool Urban and share one weather cell. Here each mandal-season is one event (confirmed if any of its sites is confirmed; the Adoni / Peddakadubur border site is excluded).

| mandal-seasons | severe: confirmed (eventually) | severe: confirmed before order | moderate: confirmed (eventually) | moderate: confirmed before order | not declared: confirmed (false alarm) |
|---|---|---|---|---|---|
| all | 6/6 | 5/6 | 2/4 | 2/4 | 1/8 |

| year | mandal | sites | weather_cells | official | order_date | system_first_confirmed | confirmed | before_order | partial_season |
|---|---|---|---|---|---|---|---|---|---|
| 2023 | Kurnool Rural | Din | 1 | Not declared | 2023-10-31 | 2023-09-04 | True | True | False |
| 2023 | Kurnool Urban | Bal, Pul | 1 | Severe | 2023-10-31 | 2023-10-29 | True | True | False |
| 2023 | Lepakshi | Cho, Lep | 1 | Moderate | 2023-10-31 | 2023-10-19 | True | True | False |
| 2023 | Sira taluk | Sira | 1 | Severe | 2023-09-14 | 2023-09-09 | True | True | False |
| 2023 | Somandepalle | Som | 1 | Moderate | 2023-10-31 | 2023-10-29 | True | True | False |
| 2024 | Kurnool Rural | Din | 1 | Not declared | 2024-10-29 | None | False | False | False |
| 2024 | Kurnool Urban | Bal, Pul | 1 | Not declared | 2024-10-29 | None | False | False | False |
| 2024 | Lepakshi | Cho, Lep | 1 | Not declared | 2024-10-29 | None | False | False | False |
| 2024 | Somandepalle | Som | 1 | Not declared | 2024-10-29 | None | False | False | False |
| 2025 | Adoni (border with Peddakadubur) | Ped | 1 | Not declared | 2025-10-31 | None | False | False | False |
| 2025 | Kurnool Rural | Din | 1 | Not declared | 2025-10-31 | None | False | False | False |
| 2025 | Kurnool Urban | Bal, Pul | 1 | Not declared | 2025-10-31 | None | False | False | False |
| 2025 | Lepakshi | Cho, Lep | 1 | Moderate | 2025-10-31 | None | False | False | False |
| 2025 | Somandepalle | Som | 1 | Moderate | 2025-10-31 | None | False | False | False |
| 2026 | Kurnool Rural | Din | 1 | Severe | 2026-10-01 | 2026-09-09 | True | True | True |
| 2026 | Kurnool Urban | Bal, Pul | 1 | Severe | 2026-10-01 | 2026-09-09 | True | True | True |
| 2026 | Lepakshi | Cho, Lep | 1 | Severe | 2026-10-01 | 2026-09-24 | True | True | True |
| 2026 | Somandepalle | Som | 1 | Severe | 2026-10-01 | 2026-10-14 | True | False | True |

## Season summary per site

| year | site | mandal | weather_cell | design | season_end | partial_season | official | official_level | GO_date | first_alarm | first_confirmed | confirmed_dates | dates_with_satellite | confirmed_before_GO | lead_days_before_GO |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | Bal | Kurnool Urban | 15.8N 78.1E | retrospective | 2023-11-28 | False | Severe | 2.0000 | 2023-10-31 | 2023-06-01 | 2023-10-29 | 4 | 18 | True | 2.0000 |
| 2023 | Cho | Lepakshi | 13.8N 77.6E | retrospective | 2023-11-28 | False | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-19 | 7 | 14 | True | 12.0000 |
| 2023 | Din | Kurnool Rural | 15.8N 78.0E | retrospective | 2023-11-28 | False | Not declared | 0.0000 | 2023-10-31 | 2023-06-01 | 2023-09-04 | 12 | 18 | True | 57.0000 |
| 2023 | Lep | Lepakshi | 13.8N 77.6E | retrospective | 2023-11-28 | False | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-24 | 5 | 15 | True | 7.0000 |
| 2023 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | retrospective | 2023-11-28 | False | Moderate (Adoni) / Severe (Peddakadubur) |  | 2023-10-31 | 2023-06-16 | None | 0 | 17 | False |  |
| 2023 | Pul | Kurnool Urban | 15.8N 78.1E | retrospective | 2023-11-28 | False | Severe | 2.0000 | 2023-10-31 | 2023-06-01 | 2023-11-03 | 2 | 18 | False |  |
| 2023 | Sira | Sira taluk | 13.8N 77.0E | retrospective | 2023-11-28 | False | Severe | 2.0000 | 2023-09-14 | 2023-06-26 | 2023-09-09 | 15 | 27 | True | 5.0000 |
| 2023 | Som | Somandepalle | 14.0N 77.6E | retrospective | 2023-11-28 | False | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-29 | 5 | 15 | True | 2.0000 |
| 2024 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 19 | False |  |
| 2024 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | 2024-10-09 | None | 0 | 21 | False |  |
| 2024 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 22 | False |  |
| 2024 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | 2024-10-09 | None | 0 | 20 | False |  |
| 2024 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2024-11-28 | False | Not declared (Adoni) / Moderate (Peddakadubur) |  | 2024-10-29 | None | None | 0 | 20 | False |  |
| 2024 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 21 | False |  |
| 2024 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2024-11-28 | False | Unknown |  | 2024-10-29 | 2024-09-29 | None | 0 | 33 | False |  |
| 2024 | Som | Somandepalle | 14.0N 77.6E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None | 0 | 22 | False |  |
| 2025 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | None | None | 0 | 17 | False |  |
| 2025 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2025-11-28 | False | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None | 0 | 18 | False |  |
| 2025 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | 2025-10-19 | None | 0 | 16 | False |  |
| 2025 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2025-11-28 | False | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None | 0 | 16 | False |  |
| 2025 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | 2025-10-19 | None | 0 | 16 | False |  |
| 2025 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | None | None | 0 | 23 | False |  |
| 2025 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2025-11-28 | False | Unknown |  | 2025-10-31 | 2025-09-24 | None | 0 | 30 | False |  |
| 2025 | Som | Somandepalle | 14.0N 77.6E | prospective | 2025-11-28 | False | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None | 0 | 18 | False |  |
| 2026 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-09-09 | 3 | 10 | True | 22.0000 |
| 2026 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-10-04 | 4 | 11 | False |  |
| 2026 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-01 | 2026-09-09 | 6 | 15 | True | 22.0000 |
| 2026 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-09-24 | 4 | 14 | True | 7.0000 |
| 2026 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2026-10-24 | True | Severe (Adoni) / Not declared (Peddakadubur) |  | 2026-10-01 | 2026-07-21 | None | 0 | 10 | False |  |
| 2026 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-10-19 | 1 | 13 | False |  |
| 2026 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2026-10-24 | True | Unknown (likely declared) |  | 2026-10-01 | 2026-07-26 | 2026-07-26 | 13 | 25 | True | 67.0000 |
| 2026 | Som | Somandepalle | 14.0N 77.6E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-16 | 2026-10-14 | 3 | 13 | False |  |

Small sample (one area per mandal, 4 seasons): read as case evidence, not a statistical test.

## Sensitivity to the confirmation threshold (robustness check; the rule stays SVI < -1)

| confirmation threshold (SVI <) | severe confirmed | moderate confirmed | not declared but confirmed | declared, confirmed before order |
|---|---|---|---|---|
| -1.0000 | 9/9 | 3/6 | 1/11 | 8/15 |
| -0.7500 | 9/9 | 3/6 | 1/11 | 10/15 |
| -1.2500 | 6/9 | 3/6 | 1/11 | 6/15 |
