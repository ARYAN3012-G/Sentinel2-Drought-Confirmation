# Operational replay of the integrated system: kharif and rabi, 2023-2026

Every 5 days; kharif = 1 Jun - 30 Nov, rabi = 1 Dec - 31 Mar; weather 7 days late (AgERA5), satellite 2 days late; weather older than 5 days is not used. Alarm = SPEI-30 < -1.0 or a Severe +15-day forecast; confirmed = median rainfed SVI < -1 from >= 5 fields, each field's latest image at most 30 days old on the issue date. No crop model is used.

**Carry-over vs in-season.** A confirmation counts as *in-season* only if every image behind it was taken inside the evaluated season. Early in a season (especially 1 December, the first rabi issue date) the latest images still show the end of the previous season, so a confirmation then reports CONTINUING earlier stress, not new stress in the season's own crops. Both counts are shown; 'drought continuing' (SVI low while SPEI-90 < -1) is carry-over of weather drought by construction.

**Data ends.** kharif 2026: partial, last issue date 2026-10-24.

**Retrospective vs prospective.** The farmland mask, field segments and irrigation flag were derived from 2019-2023 imagery, so kharif 2023 and rabi 2023-24 are RETROSPECTIVE; later seasons are PROSPECTIVE with respect to every fitted or selected component.

**Thresholds fixed in advance.** SPEI < -1 (moderate drought, McKee et al. 1993 / WMO convention), SVI < -1 (one standard deviation below the field's normal), >= 5 fields and the data delays were set in run_system.py before this replay was written; they were not tuned on it.

**Satellite coverage** (share of site-dates with at least 5 clear, labelled rainfed fields): kharif 51%, rabi 96%. A possible reason for the weak rabi response (a hypothesis, not tested here): fewer rainfed fields carry a crop after December, and December greenness is dominated by late kharif crops.

## Each official decision counted once (mandal x season)

Lepakshi and Cholasamudram lie in Lepakshi mandal and share one weather cell; Balaji Villas and Pullaiah lie in Kurnool Urban and share one weather cell. Each mandal-season is one event (confirmed if any of its sites is confirmed); ambiguous (Adoni / Peddakadubur border) and unknown (Sira, Karnataka rabi) cases are excluded.

| mandal-seasons | severe: confirmed (eventually) | severe: before order | severe: confirmed on in-season images | moderate: confirmed (eventually) | moderate: before order | moderate: confirmed on in-season images | not declared: confirmed (false alarm) |
|---|---|---|---|---|---|---|---|
| kharif, retrospective (2023) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/1 |
| kharif, prospective (2024-2026) | 4/4 | 3/4 | 4/4 | 0/2 | 0/2 | 0/2 | 0/7 |
| rabi, retrospective (2023-24) | 1/2 | 1/2 | 0/2 | 0/0 | 0/0 | 0/0 | 0/2 |
| rabi, prospective (2024-25, 2025-26) | 0/2 | 0/2 | 0/2 | 0/0 | 0/0 | 0/0 | 0/8 |
| all seasons | 7/10 | 6/10 | 6/10 | 2/4 | 2/4 | 2/4 | 1/18 |

## Site-seasons

| site-seasons | severe: confirmed (eventually) | severe: before order | severe: confirmed on in-season images | moderate: confirmed (eventually) | moderate: before order | moderate: confirmed on in-season images | not declared: confirmed (false alarm) |
|---|---|---|---|---|---|---|---|
| kharif, retrospective (2023) | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/1 |
| kharif, prospective (2024-2026) | 6/6 | 3/6 | 6/6 | 0/3 | 0/3 | 0/3 | 0/10 |
| rabi, retrospective (2023-24) | 1/3 | 1/3 | 0/3 | 0/0 | 0/0 | 0/0 | 0/3 |
| rabi, prospective (2024-25, 2025-26) | 0/3 | 0/3 | 0/3 | 0/0 | 0/0 | 0/0 | 0/11 |
| all seasons | 10/15 | 6/15 | 9/15 | 3/6 | 3/6 | 3/6 | 1/25 |

Median lead before the order, declared site-seasons confirmed in advance: 7 days.

## Mandal x season detail

| season | kind | design | mandal | sites | official | order_date | system_first_confirmed | first_status | first_images | first_confirmed_in_season | confirmed_dates_in_season | confirmed_before_GO | partial_season |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kharif 2023 | kharif | retrospective | Kurnool Urban | Bal, Pul | Severe | 2023-10-31 | 2023-10-29 | drought | 2023-10-25 .. 2023-10-25 | 2023-10-29 | 1 | True | False |
| kharif 2023 | kharif | retrospective | Lepakshi | Cho, Lep | Moderate | 2023-10-31 | 2023-10-19 | drought | 2023-10-15 .. 2023-10-15 | 2023-10-19 | 1 | True | False |
| kharif 2023 | kharif | retrospective | Kurnool Rural | Din | Not declared | 2023-10-31 | 2023-09-04 | drought | 2023-08-31 .. 2023-08-31 | 2023-09-04 | 1 | True | False |
| kharif 2023 | kharif | retrospective | Sira taluk | Sira | Severe | 2023-09-14 | 2023-09-09 | drought | 2023-08-16 .. 2023-08-31 | 2023-09-09 | 1 | True | False |
| kharif 2023 | kharif | retrospective | Somandepalle | Som | Moderate | 2023-10-31 | 2023-10-29 | drought | 2023-10-25 .. 2023-10-25 | 2023-10-29 | 1 | True | False |
| kharif 2024 | kharif | prospective | Kurnool Urban | Bal, Pul | Not declared | 2024-10-29 | None |  |  | None | 0 | False | False |
| kharif 2024 | kharif | prospective | Lepakshi | Cho, Lep | Not declared | 2024-10-29 | None |  |  | None | 0 | False | False |
| kharif 2024 | kharif | prospective | Kurnool Rural | Din | Not declared | 2024-10-29 | None |  |  | None | 0 | False | False |
| kharif 2024 | kharif | prospective | Somandepalle | Som | Not declared | 2024-10-29 | None |  |  | None | 0 | False | False |
| kharif 2025 | kharif | prospective | Kurnool Urban | Bal, Pul | Not declared | 2025-10-31 | None |  |  | None | 0 | False | False |
| kharif 2025 | kharif | prospective | Lepakshi | Cho, Lep | Moderate | 2025-10-31 | None |  |  | None | 0 | False | False |
| kharif 2025 | kharif | prospective | Kurnool Rural | Din | Not declared | 2025-10-31 | None |  |  | None | 0 | False | False |
| kharif 2025 | kharif | prospective | Adoni (border with Peddakadubur) | Ped | Not declared | 2025-10-31 | None |  |  | None | 0 | False | False |
| kharif 2025 | kharif | prospective | Somandepalle | Som | Moderate | 2025-10-31 | None |  |  | None | 0 | False | False |
| kharif 2026 | kharif | prospective | Kurnool Urban | Bal, Pul | Severe | 2026-10-01 | 2026-09-09 | drought | 2026-09-06 .. 2026-09-06 | 2026-09-09 | 1 | True | True |
| kharif 2026 | kharif | prospective | Lepakshi | Cho, Lep | Severe | 2026-10-01 | 2026-09-24 | drought | 2026-09-06 .. 2026-09-14 | 2026-09-24 | 1 | True | True |
| kharif 2026 | kharif | prospective | Kurnool Rural | Din | Severe | 2026-10-01 | 2026-09-09 | drought | 2026-09-06 .. 2026-09-06 | 2026-09-09 | 1 | True | True |
| kharif 2026 | kharif | prospective | Somandepalle | Som | Severe | 2026-10-01 | 2026-10-14 | drought | 2026-09-14 .. 2026-10-09 | 2026-10-14 | 1 | False | True |
| rabi 2023-24 | rabi | retrospective | Kurnool Urban | Bal, Pul | Severe | 2024-03-16 | None |  |  | None | 0 | False | False |
| rabi 2023-24 | rabi | retrospective | Lepakshi | Cho, Lep | Not declared | 2024-03-16 | None |  |  | None | 0 | False | False |
| rabi 2023-24 | rabi | retrospective | Kurnool Rural | Din | Severe | 2024-03-16 | 2023-12-06 | drought continuing | 2023-11-09 .. 2023-11-29 | None | 0 | True | False |
| rabi 2023-24 | rabi | retrospective | Somandepalle | Som | Not declared | 2024-03-16 | None |  |  | None | 0 | False | False |
| rabi 2024-25 | rabi | prospective | Kurnool Urban | Bal, Pul | Severe | 2025-03-31 | None |  |  | None | 0 | False | False |
| rabi 2024-25 | rabi | prospective | Lepakshi | Cho, Lep | Not declared | 2025-03-31 | None |  |  | None | 0 | False | False |
| rabi 2024-25 | rabi | prospective | Kurnool Rural | Din | Severe | 2025-03-31 | None |  |  | None | 0 | False | False |
| rabi 2024-25 | rabi | prospective | Adoni (border with Peddakadubur) | Ped | Not declared | 2025-03-31 | None |  |  | None | 0 | False | False |
| rabi 2024-25 | rabi | prospective | Somandepalle | Som | Not declared | 2025-03-31 | None |  |  | None | 0 | False | False |
| rabi 2025-26 | rabi | prospective | Kurnool Urban | Bal, Pul | Not declared | 2026-03-31 | None |  |  | None | 0 | False | False |
| rabi 2025-26 | rabi | prospective | Lepakshi | Cho, Lep | Not declared | 2026-03-31 | None |  |  | None | 0 | False | False |
| rabi 2025-26 | rabi | prospective | Kurnool Rural | Din | Not declared | 2026-03-31 | None |  |  | None | 0 | False | False |
| rabi 2025-26 | rabi | prospective | Adoni (border with Peddakadubur) | Ped | Not declared | 2026-03-31 | None |  |  | None | 0 | False | False |
| rabi 2025-26 | rabi | prospective | Somandepalle | Som | Not declared | 2026-03-31 | None |  |  | None | 0 | False | False |

## Season summary per site

| season | kind | year | site | mandal | weather_cell | design | season_end | partial_season | official | official_level | GO_date | first_alarm | first_confirmed | first_confirmed_status | first_confirmed_images | first_confirmed_in_season | confirmed_dates | confirmed_dates_in_season | dates_with_satellite | site_dates | confirmed_before_GO | lead_days_before_GO |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kharif 2023 | kharif | 2023 | Bal | Kurnool Urban | 15.8N 78.1E | retrospective | 2023-11-28 | False | Severe | 2.0000 | 2023-10-31 | 2023-06-01 | 2023-10-29 | drought | 2023-10-25 .. 2023-10-25 | 2023-10-29 | 4 | 4 | 18 | 37 | True | 2.0000 |
| kharif 2023 | kharif | 2023 | Cho | Lepakshi | 13.8N 77.6E | retrospective | 2023-11-28 | False | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-19 | drought | 2023-10-15 .. 2023-10-15 | 2023-10-19 | 7 | 7 | 14 | 37 | True | 12.0000 |
| kharif 2023 | kharif | 2023 | Din | Kurnool Rural | 15.8N 78.0E | retrospective | 2023-11-28 | False | Not declared | 0.0000 | 2023-10-31 | 2023-06-01 | 2023-09-04 | drought | 2023-08-31 .. 2023-08-31 | 2023-09-04 | 12 | 12 | 18 | 37 | True | 57.0000 |
| kharif 2023 | kharif | 2023 | Lep | Lepakshi | 13.8N 77.6E | retrospective | 2023-11-28 | False | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-24 | drought | 2023-10-15 .. 2023-10-20 | 2023-10-24 | 5 | 5 | 15 | 37 | True | 7.0000 |
| kharif 2023 | kharif | 2023 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | retrospective | 2023-11-28 | False | Moderate (Adoni) / Severe (Peddakadubur) |  | 2023-10-31 | 2023-06-16 | None |  |  | None | 0 | 0 | 16 | 37 | False |  |
| kharif 2023 | kharif | 2023 | Pul | Kurnool Urban | 15.8N 78.1E | retrospective | 2023-11-28 | False | Severe | 2.0000 | 2023-10-31 | 2023-06-01 | 2023-11-03 | drought | 2023-10-30 .. 2023-10-30 | 2023-11-03 | 2 | 2 | 18 | 37 | False |  |
| kharif 2023 | kharif | 2023 | Sira | Sira taluk | 13.8N 77.0E | retrospective | 2023-11-28 | False | Severe | 2.0000 | 2023-09-14 | 2023-06-26 | 2023-09-09 | drought | 2023-08-16 .. 2023-08-31 | 2023-09-09 | 15 | 15 | 26 | 37 | True | 5.0000 |
| kharif 2023 | kharif | 2023 | Som | Somandepalle | 14.0N 77.6E | retrospective | 2023-11-28 | False | Moderate | 1.0000 | 2023-10-31 | 2023-06-16 | 2023-10-29 | drought | 2023-10-25 .. 2023-10-25 | 2023-10-29 | 5 | 5 | 15 | 37 | True | 2.0000 |
| kharif 2024 | kharif | 2024 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None |  |  | None | 0 | 0 | 19 | 37 | False |  |
| kharif 2024 | kharif | 2024 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | 2024-10-09 | None |  |  | None | 0 | 0 | 21 | 37 | False |  |
| kharif 2024 | kharif | 2024 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None |  |  | None | 0 | 0 | 22 | 37 | False |  |
| kharif 2024 | kharif | 2024 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | 2024-10-09 | None |  |  | None | 0 | 0 | 20 | 37 | False |  |
| kharif 2024 | kharif | 2024 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2024-11-28 | False | Not declared (Adoni) / Moderate (Peddakadubur) |  | 2024-10-29 | None | None |  |  | None | 0 | 0 | 20 | 37 | False |  |
| kharif 2024 | kharif | 2024 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None |  |  | None | 0 | 0 | 21 | 37 | False |  |
| kharif 2024 | kharif | 2024 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2024-11-28 | False | Unknown |  | 2024-10-29 | 2024-09-29 | None |  |  | None | 0 | 0 | 32 | 37 | False |  |
| kharif 2024 | kharif | 2024 | Som | Somandepalle | 14.0N 77.6E | prospective | 2024-11-28 | False | Not declared | 0.0000 | 2024-10-29 | None | None |  |  | None | 0 | 0 | 22 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | None | None |  |  | None | 0 | 0 | 17 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2025-11-28 | False | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None |  |  | None | 0 | 0 | 18 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | 2025-10-19 | None |  |  | None | 0 | 0 | 16 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2025-11-28 | False | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None |  |  | None | 0 | 0 | 16 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | 2025-10-19 | None |  |  | None | 0 | 0 | 15 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2025-11-28 | False | Not declared | 0.0000 | 2025-10-31 | None | None |  |  | None | 0 | 0 | 23 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2025-11-28 | False | Unknown |  | 2025-10-31 | 2025-09-24 | None |  |  | None | 0 | 0 | 29 | 37 | False |  |
| kharif 2025 | kharif | 2025 | Som | Somandepalle | 14.0N 77.6E | prospective | 2025-11-28 | False | Moderate | 1.0000 | 2025-10-31 | 2025-09-24 | None |  |  | None | 0 | 0 | 18 | 37 | False |  |
| kharif 2026 | kharif | 2026 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-09-09 | drought | 2026-09-06 .. 2026-09-06 | 2026-09-09 | 3 | 3 | 10 | 30 | True | 22.0000 |
| kharif 2026 | kharif | 2026 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-10-04 | drought | 2026-09-06 .. 2026-09-29 | 2026-10-04 | 4 | 4 | 11 | 30 | False |  |
| kharif 2026 | kharif | 2026 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-01 | 2026-09-09 | drought | 2026-09-06 .. 2026-09-06 | 2026-09-09 | 6 | 6 | 15 | 30 | True | 22.0000 |
| kharif 2026 | kharif | 2026 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-09-24 | drought | 2026-09-06 .. 2026-09-14 | 2026-09-24 | 4 | 4 | 14 | 30 | True | 7.0000 |
| kharif 2026 | kharif | 2026 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2026-10-24 | True | Severe (Adoni) / Not declared (Peddakadubur) |  | 2026-10-01 | 2026-07-21 | None |  |  | None | 0 | 0 | 10 | 30 | False |  |
| kharif 2026 | kharif | 2026 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-21 | 2026-10-19 | drought | 2026-10-09 .. 2026-10-14 | 2026-10-19 | 1 | 1 | 13 | 30 | False |  |
| kharif 2026 | kharif | 2026 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2026-10-24 | True | Unknown (likely declared) |  | 2026-10-01 | 2026-07-26 | 2026-07-26 | drought | 2026-07-11 .. 2026-07-16 | 2026-07-26 | 13 | 13 | 25 | 30 | True | 67.0000 |
| kharif 2026 | kharif | 2026 | Som | Somandepalle | 14.0N 77.6E | prospective | 2026-10-24 | True | Severe | 2.0000 | 2026-10-01 | 2026-07-16 | 2026-10-14 | drought | 2026-09-14 .. 2026-10-09 | 2026-10-14 | 3 | 3 | 13 | 30 | False |  |
| rabi 2023-24 | rabi | 2023 | Bal | Kurnool Urban | 15.8N 78.1E | retrospective | 2024-03-30 | False | Severe | 2.0000 | 2024-03-16 | 2024-01-20 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2023-24 | rabi | 2023 | Cho | Lepakshi | 13.8N 77.6E | retrospective | 2024-03-30 | False | Not declared | 0.0000 | 2024-03-16 | 2024-02-19 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2023-24 | rabi | 2023 | Din | Kurnool Rural | 15.8N 78.0E | retrospective | 2024-03-30 | False | Severe | 2.0000 | 2024-03-16 | 2024-01-20 | 2023-12-06 | drought continuing | 2023-11-09 .. 2023-11-29 | None | 1 | 0 | 19 | 25 | True | 101.0000 |
| rabi 2023-24 | rabi | 2023 | Lep | Lepakshi | 13.8N 77.6E | retrospective | 2024-03-30 | False | Not declared | 0.0000 | 2024-03-16 | 2024-02-19 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2023-24 | rabi | 2023 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | retrospective | 2024-03-30 | False | Severe (Adoni) / Not declared (Peddakadubur) |  | 2024-03-16 | 2024-01-20 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2023-24 | rabi | 2023 | Pul | Kurnool Urban | 15.8N 78.1E | retrospective | 2024-03-30 | False | Severe | 2.0000 | 2024-03-16 | 2024-01-20 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2023-24 | rabi | 2023 | Sira | Sira taluk | 13.8N 77.0E | retrospective | 2024-03-30 | False | Unknown |  | 2024-03-16 | 2024-02-19 | 2023-12-01 | drought continuing | 2023-11-17 .. 2023-11-24 | None | 2 | 0 | 25 | 25 | True | 106.0000 |
| rabi 2023-24 | rabi | 2023 | Som | Somandepalle | 14.0N 77.6E | retrospective | 2024-03-30 | False | Not declared | 0.0000 | 2024-03-16 | 2024-02-14 | None |  |  | None | 0 | 0 | 24 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2025-03-31 | False | Severe | 2.0000 | 2025-03-31 | 2025-01-20 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2025-03-31 | False | Not declared | 0.0000 | 2025-03-31 | 2025-02-14 | None |  |  | None | 0 | 0 | 24 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2025-03-31 | False | Severe | 2.0000 | 2025-03-31 | 2025-02-19 | None |  |  | None | 0 | 0 | 20 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2025-03-31 | False | Not declared | 0.0000 | 2025-03-31 | 2025-02-14 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2025-03-31 | False | Not declared | 0.0000 | 2025-03-31 | 2025-02-19 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2025-03-31 | False | Severe | 2.0000 | 2025-03-31 | 2025-01-20 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2025-03-31 | False | Unknown |  | 2025-03-31 | 2025-02-19 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2024-25 | rabi | 2024 | Som | Somandepalle | 14.0N 77.6E | prospective | 2025-03-31 | False | Not declared | 0.0000 | 2025-03-31 | 2024-12-06 | None |  |  | None | 0 | 0 | 23 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Bal | Kurnool Urban | 15.8N 78.1E | prospective | 2026-03-31 | False | Not declared | 0.0000 | 2026-03-31 | 2026-02-19 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Cho | Lepakshi | 13.8N 77.6E | prospective | 2026-03-31 | False | Not declared | 0.0000 | 2026-03-31 | 2025-12-06 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Din | Kurnool Rural | 15.8N 78.0E | prospective | 2026-03-31 | False | Not declared | 0.0000 | 2026-03-31 | None | None |  |  | None | 0 | 0 | 20 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Lep | Lepakshi | 13.8N 77.6E | prospective | 2026-03-31 | False | Not declared | 0.0000 | 2026-03-31 | 2025-12-06 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Ped | Adoni (border with Peddakadubur) | 15.8N 77.3E | prospective | 2026-03-31 | False | Not declared | 0.0000 | 2026-03-31 | None | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Pul | Kurnool Urban | 15.8N 78.1E | prospective | 2026-03-31 | False | Not declared | 0.0000 | 2026-03-31 | 2026-02-19 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Sira | Sira taluk | 13.8N 77.0E | prospective | 2026-03-31 | False | Unknown |  | 2026-03-31 | 2025-12-06 | None |  |  | None | 0 | 0 | 25 | 25 | False |  |
| rabi 2025-26 | rabi | 2025 | Som | Somandepalle | 14.0N 77.6E | prospective | 2026-03-31 | False | Not declared | 0.0000 | 2026-03-31 | 2026-02-19 | None |  |  | None | 0 | 0 | 23 | 25 | False |  |

Small sample (one area per mandal; declarations are administrative decisions, not field-level ground truth): read as case evidence, not a statistical test. '0/10 false alarms' means no flag in ten undeclared cases; with so few, spatially related cases the true rate could still be about 30% (approximate 95% upper bound for 0/10). Site-to-mandal assignment uses the site centre, not a polygon overlay with official mandal boundaries.

## Sensitivity to the confirmation threshold (mandal-seasons, all seasons; the rule stays SVI < -1)

| confirmation threshold (SVI <) | severe: confirmed (eventually) | severe: before order | severe: confirmed on in-season images | moderate: confirmed (eventually) | moderate: before order | moderate: confirmed on in-season images | not declared: confirmed (false alarm) |
|---|---|---|---|---|---|---|---|
| -1.0000 | 7/10 | 6/10 | 6/10 | 2/4 | 2/4 | 2/4 | 1/18 |
| -0.7500 | 8/10 | 8/10 | 8/10 | 2/4 | 2/4 | 2/4 | 2/18 |
| -1.2500 | 5/10 | 4/10 | 5/10 | 2/4 | 2/4 | 2/4 | 1/18 |
