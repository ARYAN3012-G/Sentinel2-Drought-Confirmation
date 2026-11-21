# Exploratory rabi diagnostics (retrospective, end of season)

**Exploratory and retrospective.** Added after the main analysis showed that the greenness of rainfed kharif fields hardly responds in rabi. These are END-OF-SEASON diagnostics computed from the whole season's cleaned series, not early warnings issued during the season. Rules fixed before comparing with the declarations (see the script header): A = vegetation activity (NDVI p90 > 0.35 and p90 - p10 > 0.15) in < 75% of the site's normal share of sampled fields (normal = rabi 2019-20 to 2022-23; all fields, rainfed and irrigated equally weighted - not a mandal cropped-area estimate); B = median Dec-Feb SVI of the irrigated fields < -1. Few cases (4 severe = 2 mandals x 2 seasons): read as indication, not proof.

**Activity is not sowing.** The rule detects greenness plus variation; a late kharif crop drying in December passes it. December dominates: median share of ACTIVE rainfed fields over rabi 2023-24 .. 2025-26 is 83% on Dec-Mar but 29% on Jan-Mar only. Whether low January-March activity means no crop, normal senescence, late planting or failed establishment is not resolved here (needs a phenology / crop-calendar check).

## Each official decision once (mandal x rabi season)

| indicator | severe declared: flagged | not declared: flagged (false alarm) |
|---|---|---|
| A vegetation activity (< 75 % of normal) | 1/4 | 0/10 |
| B irrigated SVI (< -1) | 0/4 | 0/10 |
| A or B | 1/4 | 0/10 |

| rabi_label | mandal | official | sites | sown_pct_of_normal | A | rainfed_pct | irrigated_pct | rainfed_janmar_pct | irr_svi_median | B |
|---|---|---|---|---|---|---|---|---|---|---|
| 2023-24 | Kurnool Rural | Severe | Din | 103.0000 | False | 83.0000 | 144.0000 | 21.0000 | 0.0100 | False |
| 2023-24 | Kurnool Urban | Severe | Bal, Pul | 93.0000 | False | 92.0000 | 94.0000 | 85.0000 | -0.1300 | False |
| 2023-24 | Lepakshi | Not declared | Cho, Lep | 109.0000 | False | 111.0000 | 100.0000 | 0.0000 | 0.0600 | False |
| 2023-24 | Somandepalle | Not declared | Som | 117.0000 | False | 118.0000 | 114.0000 | 74.0000 | 0.2300 | False |
| 2024-25 | Adoni (border with Peddakadubur) | Not declared | Ped | 99.0000 | False | 103.0000 | 92.0000 | 116.0000 | -0.1000 | False |
| 2024-25 | Kurnool Rural | Severe | Din | 72.0000 | True | 45.0000 | 128.0000 | 42.0000 | -0.6000 | False |
| 2024-25 | Kurnool Urban | Severe | Bal, Pul | 75.0000 | False | 62.0000 | 106.0000 | 85.0000 | 0.0100 | False |
| 2024-25 | Lepakshi | Not declared | Cho, Lep | 104.0000 | False | 119.0000 | 71.0000 | 100.0000 | 0.1300 | False |
| 2024-25 | Somandepalle | Not declared | Som | 117.0000 | False | 118.0000 | 114.0000 | 133.0000 | 0.4200 | False |
| 2025-26 | Adoni (border with Peddakadubur) | Not declared | Ped | 95.0000 | False | 103.0000 | 82.0000 | 124.0000 | -0.0900 | False |
| 2025-26 | Kurnool Rural | Not declared | Din | 138.0000 | False | 121.0000 | 176.0000 | 105.0000 | -0.5700 | False |
| 2025-26 | Kurnool Urban | Not declared | Bal, Pul | 86.0000 | False | 92.0000 | 71.0000 | 85.0000 | -0.0400 | False |
| 2025-26 | Lepakshi | Not declared | Cho, Lep | 112.0000 | False | 98.0000 | 126.0000 | 44.0000 | -0.2000 | False |
| 2025-26 | Somandepalle | Not declared | Som | 108.0000 | False | 98.0000 | 129.0000 | 59.0000 | -0.0600 | False |

## Per site

| rabi_label | site | mandal | official | sown_pct_of_normal | A_sowing_flag | rainfed_pct_of_normal | irrigated_pct_of_normal | rainfed_janmar_pct_of_normal | irr_svi_median | irr_fields_below_normal | B_irrigated_flag | irr_fields |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023-24 | Bal | Kurnool Urban | Severe | 93.0000 | False | 92.0000 | 94.0000 | 85.0000 | -0.1300 | 0.0000 | False | 9 |
| 2023-24 | Cho | Lepakshi | Not declared | 117.0000 | False | 111.0000 | 126.0000 | 40.0000 | 0.0600 | 0.0000 | False | 13 |
| 2023-24 | Din | Kurnool Rural | Severe | 103.0000 | False | 83.0000 | 144.0000 | 21.0000 | 0.0100 | 0.0000 | False | 11 |
| 2023-24 | Lep | Lepakshi | Not declared | 109.0000 | False | 113.0000 | 100.0000 | 0.0000 | 0.2300 | 0.0000 | False | 12 |
| 2023-24 | Ped | Adoni (border with Peddakadubur) | Severe (Adoni) / Not declared (Peddakadubur) | 79.0000 | False | 84.0000 | 72.0000 | 71.0000 | -0.1600 | 0.1000 | False | 10 |
| 2023-24 | Pul | Kurnool Urban | Severe | 107.0000 | False | 111.0000 | 100.0000 | 107.0000 | -0.0100 | 0.2000 | False | 10 |
| 2023-24 | Sira | Sira taluk | Unknown | 82.0000 | False | 78.0000 | 95.0000 | 53.0000 | 0.3300 | 0.0000 | False | 7 |
| 2023-24 | Som | Somandepalle | Not declared | 117.0000 | False | 118.0000 | 114.0000 | 74.0000 | 0.2300 | 0.0000 | False | 10 |
| 2024-25 | Bal | Kurnool Urban | Severe | 75.0000 | False | 62.0000 | 106.0000 | 85.0000 | 0.6000 | 0.0000 | False | 9 |
| 2024-25 | Cho | Lepakshi | Not declared | 112.0000 | False | 119.0000 | 103.0000 | 100.0000 | 0.4900 | 0.0000 | False | 13 |
| 2024-25 | Din | Kurnool Rural | Severe | 72.0000 | True | 45.0000 | 128.0000 | 42.0000 | -0.6000 | 0.1800 | False | 11 |
| 2024-25 | Lep | Lepakshi | Not declared | 104.0000 | False | 121.0000 | 71.0000 | 133.0000 | 0.1300 | 0.0800 | False | 12 |
| 2024-25 | Ped | Adoni (border with Peddakadubur) | Not declared | 99.0000 | False | 103.0000 | 92.0000 | 116.0000 | -0.1000 | 0.1000 | False | 10 |
| 2024-25 | Pul | Kurnool Urban | Severe | 107.0000 | False | 105.0000 | 112.0000 | 107.0000 | 0.0100 | 0.1000 | False | 10 |
| 2024-25 | Sira | Sira taluk | Unknown | 73.0000 | True | 83.0000 | 38.0000 | 27.0000 | 0.2600 | 0.0000 | False | 7 |
| 2024-25 | Som | Somandepalle | Not declared | 117.0000 | False | 118.0000 | 114.0000 | 133.0000 | 0.4200 | 0.0000 | False | 10 |
| 2025-26 | Bal | Kurnool Urban | Not declared | 86.0000 | False | 92.0000 | 71.0000 | 85.0000 | -0.0400 | 0.2200 | False | 9 |
| 2025-26 | Cho | Lepakshi | Not declared | 112.0000 | False | 104.0000 | 126.0000 | 100.0000 | 0.1400 | 0.1500 | False | 13 |
| 2025-26 | Din | Kurnool Rural | Not declared | 138.0000 | False | 121.0000 | 176.0000 | 105.0000 | -0.5700 | 0.0900 | False | 11 |
| 2025-26 | Lep | Lepakshi | Not declared | 119.0000 | False | 98.0000 | 157.0000 | 44.0000 | -0.2000 | 0.2500 | False | 12 |
| 2025-26 | Ped | Adoni (border with Peddakadubur) | Not declared | 95.0000 | False | 103.0000 | 82.0000 | 124.0000 | -0.0900 | 0.1000 | False | 10 |
| 2025-26 | Pul | Kurnool Urban | Not declared | 103.0000 | False | 105.0000 | 100.0000 | 86.0000 | 0.1100 | 0.2000 | False | 10 |
| 2025-26 | Sira | Sira taluk | Unknown | 39.0000 | True | 39.0000 | 38.0000 | 80.0000 | 0.4700 | 0.0000 | False | 7 |
| 2025-26 | Som | Somandepalle | Not declared | 108.0000 | False | 98.0000 | 129.0000 | 59.0000 | -0.0600 | 0.0000 | False | 10 |

## Registered rules for rabi 2026-27 (R1 end of season, R2 early on 15 Feb)

Registered 2026-11-21 (docs/PREREGISTRATION_rabi_2026-27.md). Rainfed sampled fields only. Rows for 2023-24 .. 2025-26 are POST HOC: the rule was written after seeing them, so they show how it behaves, not how well it works. Only rabi 2026-27 is a test.

### Mandal x rabi season (each official decision once; ambiguous / unknown excluded)

| rule | design | severe: flagged | moderate: flagged | not declared: flagged |
|---|---|---|---|---|
| R1 | post hoc (not a test) | 2/4 | 0/0 | 0/10 |
| R2 | post hoc (not a test) | 3/4 | 0/0 | 0/10 |

### Per site

| rule | rabi_label | design | site | mandal | official | fields | pct_of_normal | status |
|---|---|---|---|---|---|---|---|---|
| R1 | 2023-24 | post hoc (not a test) | Bal | Kurnool Urban | Severe | 21 | 92.0000 | no flag |
| R1 | 2023-24 | post hoc (not a test) | Cho | Lepakshi | Not declared | 17 | 111.0000 | no flag |
| R1 | 2023-24 | post hoc (not a test) | Din | Kurnool Rural | Severe | 19 | 83.0000 | no flag |
| R1 | 2023-24 | post hoc (not a test) | Lep | Lepakshi | Not declared | 18 | 113.0000 | no flag |
| R1 | 2023-24 | post hoc (not a test) | Ped | Adoni (border with Peddakadubur) | Severe (Adoni) / Not declared (Peddakadubur) | 20 | 84.0000 | no flag |
| R1 | 2023-24 | post hoc (not a test) | Pul | Kurnool Urban | Severe | 20 | 111.0000 | no flag |
| R1 | 2023-24 | post hoc (not a test) | Sira | Sira taluk | Unknown | 23 | 78.0000 | no flag |
| R1 | 2023-24 | post hoc (not a test) | Som | Somandepalle | Not declared | 20 | 118.0000 | no flag |
| R1 | 2024-25 | post hoc (not a test) | Bal | Kurnool Urban | Severe | 21 | 62.0000 | flag |
| R1 | 2024-25 | post hoc (not a test) | Cho | Lepakshi | Not declared | 17 | 119.0000 | no flag |
| R1 | 2024-25 | post hoc (not a test) | Din | Kurnool Rural | Severe | 19 | 45.0000 | flag |
| R1 | 2024-25 | post hoc (not a test) | Lep | Lepakshi | Not declared | 18 | 121.0000 | no flag |
| R1 | 2024-25 | post hoc (not a test) | Ped | Adoni (border with Peddakadubur) | Not declared | 20 | 103.0000 | no flag |
| R1 | 2024-25 | post hoc (not a test) | Pul | Kurnool Urban | Severe | 20 | 105.0000 | no flag |
| R1 | 2024-25 | post hoc (not a test) | Sira | Sira taluk | Unknown | 23 | 83.0000 | no flag |
| R1 | 2024-25 | post hoc (not a test) | Som | Somandepalle | Not declared | 20 | 118.0000 | no flag |
| R1 | 2025-26 | post hoc (not a test) | Bal | Kurnool Urban | Not declared | 21 | 92.0000 | no flag |
| R1 | 2025-26 | post hoc (not a test) | Cho | Lepakshi | Not declared | 17 | 104.0000 | no flag |
| R1 | 2025-26 | post hoc (not a test) | Din | Kurnool Rural | Not declared | 19 | 121.0000 | no flag |
| R1 | 2025-26 | post hoc (not a test) | Lep | Lepakshi | Not declared | 18 | 98.0000 | no flag |
| R1 | 2025-26 | post hoc (not a test) | Ped | Adoni (border with Peddakadubur) | Not declared | 20 | 103.0000 | no flag |
| R1 | 2025-26 | post hoc (not a test) | Pul | Kurnool Urban | Not declared | 20 | 105.0000 | no flag |
| R1 | 2025-26 | post hoc (not a test) | Sira | Sira taluk | Unknown | 23 | 39.0000 | flag |
| R1 | 2025-26 | post hoc (not a test) | Som | Somandepalle | Not declared | 20 | 98.0000 | no flag |
| R2 | 2023-24 | post hoc (not a test) | Bal | Kurnool Urban | Severe | 21 | 97.0000 | no flag |
| R2 | 2023-24 | post hoc (not a test) | Cho | Lepakshi | Not declared | 17 | 137.0000 | no flag |
| R2 | 2023-24 | post hoc (not a test) | Din | Kurnool Rural | Severe | 19 | 71.0000 | flag |
| R2 | 2023-24 | post hoc (not a test) | Lep | Lepakshi | Not declared | 18 | 126.0000 | no flag |
| R2 | 2023-24 | post hoc (not a test) | Ped | Adoni (border with Peddakadubur) | Severe (Adoni) / Not declared (Peddakadubur) | 20 | 75.0000 | flag |
| R2 | 2023-24 | post hoc (not a test) | Pul | Kurnool Urban | Severe | 20 | 97.0000 | no flag |
| R2 | 2023-24 | post hoc (not a test) | Sira | Sira taluk | Unknown | 23 | 38.0000 | flag |
| R2 | 2023-24 | post hoc (not a test) | Som | Somandepalle | Not declared | 20 | 169.0000 | no flag |
| R2 | 2024-25 | post hoc (not a test) | Bal | Kurnool Urban | Severe | 21 | 69.0000 | flag |
| R2 | 2024-25 | post hoc (not a test) | Cho | Lepakshi | Not declared | 17 | 88.0000 | no flag |
| R2 | 2024-25 | post hoc (not a test) | Din | Kurnool Rural | Severe | 19 | 71.0000 | flag |
| R2 | 2024-25 | post hoc (not a test) | Lep | Lepakshi | Not declared | 18 | 137.0000 | no flag |
| R2 | 2024-25 | post hoc (not a test) | Ped | Adoni (border with Peddakadubur) | Not declared | 20 | 88.0000 | no flag |
| R2 | 2024-25 | post hoc (not a test) | Pul | Kurnool Urban | Severe | 20 | 110.0000 | no flag |
| R2 | 2024-25 | post hoc (not a test) | Sira | Sira taluk | Unknown | 23 | 94.0000 | no flag |
| R2 | 2024-25 | post hoc (not a test) | Som | Somandepalle | Not declared | 20 | 231.0000 | no flag |
| R2 | 2025-26 | post hoc (not a test) | Bal | Kurnool Urban | Not declared | 21 | 109.0000 | no flag |
| R2 | 2025-26 | post hoc (not a test) | Cho | Lepakshi | Not declared | 17 | 117.0000 | no flag |
| R2 | 2025-26 | post hoc (not a test) | Din | Kurnool Rural | Not declared | 19 | 133.0000 | no flag |
| R2 | 2025-26 | post hoc (not a test) | Lep | Lepakshi | Not declared | 18 | 137.0000 | no flag |
| R2 | 2025-26 | post hoc (not a test) | Ped | Adoni (border with Peddakadubur) | Not declared | 20 | 95.0000 | no flag |
| R2 | 2025-26 | post hoc (not a test) | Pul | Kurnool Urban | Not declared | 20 | 124.0000 | no flag |
| R2 | 2025-26 | post hoc (not a test) | Sira | Sira taluk | Unknown | 23 | 31.0000 | flag |
| R2 | 2025-26 | post hoc (not a test) | Som | Somandepalle | Not declared | 20 | 215.0000 | no flag |
