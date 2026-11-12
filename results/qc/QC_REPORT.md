# Satellite data quality report

Real Sentinel-2 SR (Cloud Score+ and SCL masked), 240 sampled farmland segments.
Observation kept if >= 60% of the field's pixels are clear; same-day duplicates merged. Isolated NDVI spikes > 0.15 are removed from the label series only (that check looks at the next image); model inputs use every accepted image up to the date. Reference (normal) = observations up to 2023-12-31 only.

## Observations per site (irrigated 0 = rainfed)

| site_code | irrigated | fields | raw_obs | clear | merged | final | median_gap_days |
|---|---|---|---|---|---|---|---|
| Bal | 0 | 21 | 6535 | 6306 | 6263 | 6255 | 5.0000 |
| Bal | 1 | 9 | 2813 | 2679 | 2661 | 2649 | 5.0000 |
| Cho | 0 | 17 | 4951 | 4717 | 4715 | 4709 | 5.0000 |
| Cho | 1 | 13 | 3783 | 3585 | 3583 | 3568 | 5.0000 |
| Din | 0 | 19 | 5904 | 5693 | 5655 | 5649 | 5.0000 |
| Din | 1 | 11 | 3441 | 3301 | 3279 | 3248 | 5.0000 |
| Lep | 0 | 18 | 5231 | 4954 | 4937 | 4927 | 5.0000 |
| Lep | 1 | 12 | 3471 | 3297 | 3296 | 3282 | 5.0000 |
| Ped | 0 | 20 | 6555 | 6323 | 6260 | 6236 | 5.0000 |
| Ped | 1 | 10 | 3297 | 3186 | 3151 | 3129 | 5.0000 |
| Pul | 0 | 20 | 6469 | 6233 | 6199 | 6177 | 5.0000 |
| Pul | 1 | 10 | 3235 | 3127 | 3112 | 3103 | 5.0000 |
| Sira | 0 | 23 | 10310 | 9751 | 9611 | 9600 | 3.0000 |
| Sira | 1 | 7 | 2497 | 2378 | 2350 | 2340 | 5.0000 |
| Som | 0 | 20 | 6034 | 5741 | 5657 | 5655 | 5.0000 |
| Som | 1 | 10 | 2966 | 2827 | 2786 | 2770 | 5.0000 |

## Crop-condition labels (SVI) by period

SVI = standardized NDVI anomaly; reference = training years 2019-2023 only, +-15 days of the same day of year, labelled year fully excluded. Classes (SPEI thresholds of the weather module): normal or above z >= 0, below normal -1.5 to 0, strongly below normal < -1.5. Steps without a normal crop signal are unlabelled.

| period | Normal or above % | Below normal % | Strongly below normal % | labelled steps |
|---|---|---|---|---|
| test | 51.6000 | 41.4000 | 7.1000 | 16615 |
| train | 47.5000 | 44.0000 | 8.5000 | 43382 |
| val | 48.2000 | 47.3000 | 4.5000 | 9256 |

## Labels by year (rainfed fields) — drought years should show more stress

| year | Normal or above % | Below normal % | Strongly below normal % | labelled steps |
|---|---|---|---|---|
| 2019 | 30.6000 | 46.5000 | 22.9000 | 4881 |
| 2020 | 45.5000 | 52.4000 | 2.2000 | 5128 |
| 2021 | 58.3000 | 39.2000 | 2.5000 | 4713 |
| 2022 | 57.7000 | 39.7000 | 2.6000 | 5167 |
| 2023 | 43.4000 | 42.4000 | 14.1000 | 5181 |
| 2024 | 47.3000 | 49.4000 | 3.3000 | 5547 |
| 2025 | 59.1000 | 37.4000 | 3.4000 | 5488 |
| 2026 | 40.1000 | 49.0000 | 10.9000 | 4050 |

## Labels by site

| site_code | irrigated | Normal or above % | Below normal % | Strongly below normal % | labelled steps |
|---|---|---|---|---|---|
| Bal | 0 | 46.2000 | 45.0000 | 8.8000 | 4777 |
| Bal | 1 | 46.2000 | 48.7000 | 5.1000 | 3188 |
| Cho | 0 | 48.5000 | 43.5000 | 8.0000 | 3934 |
| Cho | 1 | 53.5000 | 37.4000 | 9.1000 | 4444 |
| Din | 0 | 46.3000 | 46.2000 | 7.5000 | 4372 |
| Din | 1 | 45.3000 | 46.0000 | 8.7000 | 4225 |
| Lep | 0 | 49.5000 | 41.6000 | 9.0000 | 4440 |
| Lep | 1 | 51.3000 | 39.1000 | 9.6000 | 3993 |
| Ped | 0 | 46.1000 | 47.7000 | 6.2000 | 5525 |
| Ped | 1 | 43.7000 | 48.4000 | 7.9000 | 3760 |
| Pul | 0 | 42.0000 | 52.7000 | 5.4000 | 6114 |
| Pul | 1 | 47.3000 | 46.2000 | 6.5000 | 3652 |
| Sira | 0 | 51.2000 | 41.4000 | 7.4000 | 6714 |
| Sira | 1 | 53.9000 | 40.6000 | 5.6000 | 2547 |
| Som | 0 | 56.3000 | 34.4000 | 9.3000 | 4279 |
| Som | 1 | 54.8000 | 37.9000 | 7.3000 | 3289 |

## Frozen field flags (training years only)

Earth Engine script A v2 flags irrigation per pixel from 2019-2023 imagery; the flag is also recomputed per field from the 2019-2023 Sentinel-2 series (same rule), and that field-level flag is the one used everywhere (models, rainfed/irrigated results).

| Earth Engine flag (pixel level, 2019-23) | 0 | 1 |
|---|---|---|
| 0 | 153 | 7 |
| 1 | 5 | 75 |

Fields without a crop cycle in >= 2 of the 5 training years, dropped: 0.

## Whole-area farmland zones

| zone_id | raw | after_spike_removal | median_gap_days |
|---|---|---|---|
| Bal_irrigated | 378 | 298 | 5.0000 |
| Bal_rainfed | 385 | 297 | 5.0000 |
| Cho_irrigated | 395 | 277 | 5.0000 |
| Cho_rainfed | 395 | 277 | 5.0000 |
| Din_irrigated | 386 | 305 | 5.0000 |
| Din_rainfed | 389 | 298 | 5.0000 |
| Lep_irrigated | 390 | 272 | 5.0000 |
| Lep_rainfed | 389 | 271 | 5.0000 |
| Ped_irrigated | 415 | 309 | 5.0000 |
| Ped_rainfed | 419 | 311 | 5.0000 |
| Pul_irrigated | 405 | 316 | 5.0000 |
| Pul_rainfed | 403 | 315 | 5.0000 |
| Sira_irrigated | 762 | 444 | 3.0000 |
| Sira_rainfed | 767 | 402 | 5.0000 |
| Som_irrigated | 395 | 280 | 5.0000 |
| Som_rainfed | 400 | 284 | 5.0000 |
