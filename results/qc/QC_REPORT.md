# Satellite data quality report

Real Sentinel-2 SR (Cloud Score+ and SCL masked), 240 sampled farmland segments.
Observation kept if >= 60% of the field's pixels are clear; same-day duplicates merged. Isolated NDVI spikes > 0.15 are removed from the label series only (that check looks at the next image); model inputs use every accepted image up to the date. Reference (normal) = observations up to 2023-12-31 only.

## Observations per site (irrigated 0 = rainfed)

| site_code | irrigated | fields | raw_obs | clear | merged | final | median_gap_days |
|---|---|---|---|---|---|---|---|
| Bal | 0 | 21 | 6542 | 6311 | 6265 | 6258 | 5.0000 |
| Bal | 1 | 9 | 2813 | 2700 | 2682 | 2665 | 5.0000 |
| Cho | 0 | 21 | 6125 | 5822 | 5817 | 5811 | 5.0000 |
| Cho | 1 | 9 | 2631 | 2528 | 2527 | 2522 | 5.0000 |
| Din | 0 | 20 | 6208 | 5990 | 5948 | 5939 | 5.0000 |
| Din | 1 | 10 | 3117 | 2999 | 2977 | 2954 | 5.0000 |
| Lep | 0 | 19 | 5444 | 5184 | 5143 | 5136 | 5.0000 |
| Lep | 1 | 11 | 3203 | 3027 | 3023 | 3015 | 5.0000 |
| Ped | 0 | 22 | 7234 | 6945 | 6866 | 6828 | 5.0000 |
| Ped | 1 | 8 | 2610 | 2535 | 2504 | 2473 | 5.0000 |
| Pul | 0 | 15 | 4831 | 4658 | 4601 | 4590 | 5.0000 |
| Pul | 1 | 15 | 4846 | 4676 | 4649 | 4625 | 5.0000 |
| Sira | 0 | 21 | 8765 | 8285 | 8177 | 8164 | 5.0000 |
| Sira | 1 | 9 | 4025 | 3810 | 3754 | 3742 | 3.0000 |
| Som | 0 | 19 | 5699 | 5482 | 5407 | 5400 | 5.0000 |
| Som | 1 | 11 | 3300 | 3127 | 3081 | 3064 | 5.0000 |

## Crop-condition labels (SVI) by period

SVI = standardized NDVI anomaly; reference = training years 2019-2023 only, +-15 days of the same day of year, labelled year fully excluded. Classes (SPEI thresholds of the weather module): normal or above z >= 0, below normal -1.5 to 0, strongly below normal < -1.5. Steps without a normal crop signal are unlabelled.

| period | Normal or above % | Below normal % | Strongly below normal % | labelled steps |
|---|---|---|---|---|
| test | 53.0000 | 40.0000 | 7.0000 | 16449 |
| train | 47.4000 | 44.0000 | 8.6000 | 43059 |
| val | 50.6000 | 44.4000 | 4.9000 | 9359 |

## Labels by year (rainfed fields) — drought years should show more stress

| year | Normal or above % | Below normal % | Strongly below normal % | labelled steps |
|---|---|---|---|---|
| 2019 | 30.3000 | 46.4000 | 23.4000 | 4804 |
| 2020 | 45.1000 | 52.6000 | 2.3000 | 5032 |
| 2021 | 58.5000 | 38.9000 | 2.6000 | 4550 |
| 2022 | 58.9000 | 36.5000 | 4.6000 | 5079 |
| 2023 | 41.7000 | 44.9000 | 13.4000 | 5051 |
| 2024 | 50.2000 | 45.2000 | 4.6000 | 5553 |
| 2025 | 60.1000 | 35.2000 | 4.7000 | 5345 |
| 2026 | 40.8000 | 46.7000 | 12.5000 | 4011 |

## Labels by site

| site_code | irrigated | Normal or above % | Below normal % | Strongly below normal % | labelled steps |
|---|---|---|---|---|---|
| Bal | 0 | 47.3000 | 45.6000 | 7.1000 | 5306 |
| Bal | 1 | 48.2000 | 46.0000 | 5.8000 | 3326 |
| Cho | 0 | 49.2000 | 41.4000 | 9.4000 | 5134 |
| Cho | 1 | 57.6000 | 36.0000 | 6.4000 | 3161 |
| Din | 0 | 46.5000 | 43.9000 | 9.6000 | 4408 |
| Din | 1 | 48.8000 | 43.8000 | 7.4000 | 3622 |
| Lep | 0 | 47.5000 | 43.8000 | 8.7000 | 4418 |
| Lep | 1 | 55.4000 | 35.7000 | 8.9000 | 3593 |
| Ped | 0 | 45.5000 | 47.4000 | 7.1000 | 5939 |
| Ped | 1 | 43.6000 | 48.7000 | 7.7000 | 2982 |
| Pul | 0 | 46.2000 | 46.6000 | 7.2000 | 4091 |
| Pul | 1 | 46.1000 | 47.4000 | 6.6000 | 5464 |
| Sira | 0 | 52.5000 | 39.3000 | 8.1000 | 5816 |
| Sira | 1 | 51.1000 | 43.3000 | 5.6000 | 3643 |
| Som | 0 | 52.9000 | 37.4000 | 9.7000 | 4313 |
| Som | 1 | 51.4000 | 41.1000 | 7.5000 | 3651 |

## Frozen field flags (training years only)

The Earth Engine irrigation flag and crop check used 2019-2025 imagery (incl. validation and test years). Both are recomputed per field from 2019-2023 observations only; the frozen irrigation flag is the one used everywhere (models, rainfed/irrigated results).

| Earth Engine flag (2019-25) | 0 | 1 |
|---|---|---|
| 0 | 148 | 12 |
| 1 | 10 | 70 |

Fields without a crop cycle in >= 2 of the 5 training years, dropped: 0.

## Whole-area farmland zones

| zone_id | raw | after_spike_removal | median_gap_days |
|---|---|---|---|
| Bal_irrigated | 375 | 298 | 5.0000 |
| Bal_rainfed | 384 | 299 | 5.0000 |
| Cho_irrigated | 394 | 275 | 5.0000 |
| Cho_rainfed | 395 | 276 | 5.0000 |
| Din_irrigated | 385 | 305 | 5.0000 |
| Din_rainfed | 389 | 298 | 5.0000 |
| Lep_irrigated | 390 | 272 | 5.0000 |
| Lep_rainfed | 389 | 269 | 5.0000 |
| Ped_irrigated | 415 | 312 | 5.0000 |
| Ped_rainfed | 419 | 311 | 5.0000 |
| Pul_irrigated | 405 | 317 | 5.0000 |
| Pul_rainfed | 403 | 316 | 5.0000 |
| Sira_irrigated | 761 | 445 | 3.0000 |
| Sira_rainfed | 766 | 407 | 5.0000 |
| Som_irrigated | 397 | 283 | 5.0000 |
| Som_rainfed | 398 | 279 | 5.0000 |
