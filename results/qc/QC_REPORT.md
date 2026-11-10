# Satellite data quality report

Real Sentinel-2 SR (Cloud Score+ and SCL masked), 240 sampled farmland segments.
Observation kept if >= 60% of the field's pixels are clear; same-day duplicates merged; isolated NDVI spikes > 0.15 removed.

## Observations per site (irrigated 0 = rainfed)

| site_code | irrigated | fields | raw_obs | clear | merged | final | median_gap_days |
|---|---|---|---|---|---|---|---|
| Bal | 0 | 20 | 6232 | 6018 | 5974 | 5967 | 5.0000 |
| Bal | 1 | 10 | 3123 | 2993 | 2973 | 2956 | 5.0000 |
| Cho | 0 | 20 | 5835 | 5553 | 5549 | 5545 | 5.0000 |
| Cho | 1 | 10 | 2921 | 2797 | 2795 | 2788 | 5.0000 |
| Din | 0 | 20 | 6208 | 5990 | 5948 | 5939 | 5.0000 |
| Din | 1 | 10 | 3117 | 2999 | 2977 | 2954 | 5.0000 |
| Lep | 0 | 20 | 5734 | 5457 | 5416 | 5409 | 5.0000 |
| Lep | 1 | 10 | 2913 | 2754 | 2750 | 2742 | 5.0000 |
| Ped | 0 | 20 | 6587 | 6324 | 6253 | 6223 | 5.0000 |
| Ped | 1 | 10 | 3257 | 3156 | 3117 | 3078 | 5.0000 |
| Pul | 0 | 20 | 6450 | 6225 | 6165 | 6145 | 5.0000 |
| Pul | 1 | 10 | 3227 | 3109 | 3085 | 3070 | 5.0000 |
| Sira | 0 | 20 | 8895 | 8461 | 8343 | 8330 | 4.0000 |
| Sira | 1 | 10 | 3895 | 3634 | 3588 | 3576 | 5.0000 |
| Som | 0 | 20 | 5997 | 5769 | 5690 | 5683 | 5.0000 |
| Som | 1 | 10 | 3002 | 2840 | 2798 | 2781 | 5.0000 |

## Crop-condition labels (SVI) by period

SVI = standardized NDVI anomaly; reference = training years 2019-2023 only, +-15 days of the same day of year, labelled year excluded. Classes as SPEI in the weather module: Healthy z >= 0, Moderate -1.5 to 0, Severe < -1.5. Steps without a normal crop signal are unlabelled.

| period | Healthy % | Moderate % | Severe % | labelled steps |
|---|---|---|---|---|
| test | 53.0000 | 40.0000 | 7.0000 | 16453 |
| train | 47.6000 | 43.3000 | 9.1000 | 44559 |
| val | 50.7000 | 44.4000 | 4.9000 | 9364 |

## Labels by year (rainfed fields) — drought years should show more stress

| year | Healthy % | Moderate % | Severe % | labelled steps |
|---|---|---|---|---|
| 2019 | 30.3000 | 42.9000 | 26.7000 | 5046 |
| 2020 | 45.4000 | 51.6000 | 3.0000 | 5265 |
| 2021 | 59.5000 | 37.9000 | 2.6000 | 4820 |
| 2022 | 60.6000 | 35.6000 | 3.7000 | 5521 |
| 2023 | 39.3000 | 48.2000 | 12.5000 | 5497 |
| 2024 | 47.3000 | 48.2000 | 4.5000 | 5645 |
| 2025 | 57.9000 | 37.5000 | 4.6000 | 5464 |
| 2026 | 37.6000 | 49.8000 | 12.6000 | 4118 |

## Labels by site

| site_code | irrigated | Healthy % | Moderate % | Severe % | labelled steps |
|---|---|---|---|---|---|
| Bal | 0 | 46.7000 | 45.8000 | 7.5000 | 5068 |
| Bal | 1 | 49.4000 | 44.7000 | 5.9000 | 3711 |
| Cho | 0 | 47.9000 | 42.7000 | 9.4000 | 4991 |
| Cho | 1 | 59.0000 | 33.6000 | 7.4000 | 3580 |
| Din | 0 | 46.4000 | 43.7000 | 9.9000 | 4491 |
| Din | 1 | 48.9000 | 43.7000 | 7.4000 | 3675 |
| Lep | 0 | 48.3000 | 41.3000 | 10.4000 | 4897 |
| Lep | 1 | 55.0000 | 36.3000 | 8.6000 | 3379 |
| Ped | 0 | 45.3000 | 47.4000 | 7.4000 | 5322 |
| Ped | 1 | 44.6000 | 47.5000 | 7.9000 | 3694 |
| Pul | 0 | 45.8000 | 47.4000 | 6.8000 | 6022 |
| Pul | 1 | 46.9000 | 46.2000 | 6.9000 | 3750 |
| Sira | 0 | 48.0000 | 43.7000 | 8.3000 | 5802 |
| Sira | 1 | 58.1000 | 36.0000 | 5.9000 | 3786 |
| Som | 0 | 52.6000 | 37.5000 | 9.9000 | 4783 |
| Som | 1 | 52.6000 | 39.4000 | 7.9000 | 3425 |

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
