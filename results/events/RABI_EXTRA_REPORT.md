# Exploratory rabi indicators

**Exploratory.** Added after the main analysis showed that the greenness of rainfed kharif fields hardly responds in rabi. Rules fixed before comparing with the declarations (see the script header): A = a rabi crop cycle is found in < 75% of the site's normal share of fields (normal = rabi 2019-20 to 2022-23); B = median Dec-Feb SVI of the irrigated fields < -1. Few cases: read as indication, not proof. Caveat: the Dec-Mar window also catches late kharif crops (e.g. cotton still green in December), so the sown share mixes late kharif and true rabi crops.

## Each official decision once (mandal x rabi season)

| indicator | severe declared: flagged | not declared: flagged (false alarm) |
|---|---|---|
| A sowing (< 75 % of normal) | 1/4 | 0/10 |
| B irrigated SVI (< -1) | 0/4 | 0/10 |
| A or B | 1/4 | 0/10 |

| rabi_label | mandal | official | sites | sown_pct_of_normal | A | irr_svi_median | B |
|---|---|---|---|---|---|---|---|
| 2023-24 | Kurnool Rural | Severe | Din | 103.0000 | False | 0.0100 | False |
| 2023-24 | Kurnool Urban | Severe | Bal, Pul | 93.0000 | False | -0.1300 | False |
| 2023-24 | Lepakshi | Not declared | Cho, Lep | 109.0000 | False | 0.0600 | False |
| 2023-24 | Somandepalle | Not declared | Som | 117.0000 | False | 0.2300 | False |
| 2024-25 | Adoni (border with Peddakadubur) | Not declared | Ped | 99.0000 | False | -0.1000 | False |
| 2024-25 | Kurnool Rural | Severe | Din | 72.0000 | True | -0.6000 | False |
| 2024-25 | Kurnool Urban | Severe | Bal, Pul | 75.0000 | False | 0.0100 | False |
| 2024-25 | Lepakshi | Not declared | Cho, Lep | 104.0000 | False | 0.1300 | False |
| 2024-25 | Somandepalle | Not declared | Som | 117.0000 | False | 0.4200 | False |
| 2025-26 | Adoni (border with Peddakadubur) | Not declared | Ped | 95.0000 | False | -0.0900 | False |
| 2025-26 | Kurnool Rural | Not declared | Din | 138.0000 | False | -0.5700 | False |
| 2025-26 | Kurnool Urban | Not declared | Bal, Pul | 86.0000 | False | -0.0400 | False |
| 2025-26 | Lepakshi | Not declared | Cho, Lep | 112.0000 | False | -0.2000 | False |
| 2025-26 | Somandepalle | Not declared | Som | 108.0000 | False | -0.0600 | False |

## Per site

| rabi_label | site | mandal | official | sown_pct_of_normal | A_sowing_flag | irr_svi_median | irr_fields_below_normal | B_irrigated_flag | irr_fields |
|---|---|---|---|---|---|---|---|---|---|
| 2023-24 | Bal | Kurnool Urban | Severe | 93.0000 | False | -0.1300 | 0.0000 | False | 9 |
| 2023-24 | Cho | Lepakshi | Not declared | 117.0000 | False | 0.0600 | 0.0000 | False | 13 |
| 2023-24 | Din | Kurnool Rural | Severe | 103.0000 | False | 0.0100 | 0.0000 | False | 11 |
| 2023-24 | Lep | Lepakshi | Not declared | 109.0000 | False | 0.2300 | 0.0000 | False | 12 |
| 2023-24 | Ped | Adoni (border with Peddakadubur) | Severe (Adoni) / Not declared (Peddakadubur) | 79.0000 | False | -0.1600 | 0.1000 | False | 10 |
| 2023-24 | Pul | Kurnool Urban | Severe | 107.0000 | False | -0.0100 | 0.2000 | False | 10 |
| 2023-24 | Sira | Sira taluk | Unknown | 82.0000 | False | 0.3300 | 0.0000 | False | 7 |
| 2023-24 | Som | Somandepalle | Not declared | 117.0000 | False | 0.2300 | 0.0000 | False | 10 |
| 2024-25 | Bal | Kurnool Urban | Severe | 75.0000 | False | 0.6000 | 0.0000 | False | 9 |
| 2024-25 | Cho | Lepakshi | Not declared | 112.0000 | False | 0.4900 | 0.0000 | False | 13 |
| 2024-25 | Din | Kurnool Rural | Severe | 72.0000 | True | -0.6000 | 0.1800 | False | 11 |
| 2024-25 | Lep | Lepakshi | Not declared | 104.0000 | False | 0.1300 | 0.0800 | False | 12 |
| 2024-25 | Ped | Adoni (border with Peddakadubur) | Not declared | 99.0000 | False | -0.1000 | 0.1000 | False | 10 |
| 2024-25 | Pul | Kurnool Urban | Severe | 107.0000 | False | 0.0100 | 0.1000 | False | 10 |
| 2024-25 | Sira | Sira taluk | Unknown | 73.0000 | True | 0.2600 | 0.0000 | False | 7 |
| 2024-25 | Som | Somandepalle | Not declared | 117.0000 | False | 0.4200 | 0.0000 | False | 10 |
| 2025-26 | Bal | Kurnool Urban | Not declared | 86.0000 | False | -0.0400 | 0.2200 | False | 9 |
| 2025-26 | Cho | Lepakshi | Not declared | 112.0000 | False | 0.1400 | 0.1500 | False | 13 |
| 2025-26 | Din | Kurnool Rural | Not declared | 138.0000 | False | -0.5700 | 0.0900 | False | 11 |
| 2025-26 | Lep | Lepakshi | Not declared | 119.0000 | False | -0.2000 | 0.2500 | False | 12 |
| 2025-26 | Ped | Adoni (border with Peddakadubur) | Not declared | 95.0000 | False | -0.0900 | 0.1000 | False | 10 |
| 2025-26 | Pul | Kurnool Urban | Not declared | 103.0000 | False | 0.1100 | 0.2000 | False | 10 |
| 2025-26 | Sira | Sira taluk | Unknown | 39.0000 | True | 0.4700 | 0.0000 | False | 7 |
| 2025-26 | Som | Somandepalle | Not declared | 108.0000 | False | -0.0600 | 0.0000 | False | 10 |
