# Weather drought -> crop stress

## A. Lag correlation (Spearman rho between SVI on day t and SPEI-k on day t-lag)

Descriptive association over all available years, best of 3 scales x 19 lags (not a causal lag; SPEI-90 at lag 0 already summarises the previous 90 days of weather).

Crop-season steps (Jul-Nov) with a label. Positive rho = wetter weather, healthier crops.

### Median over sites (rows: irrigated 0/1, SPEI scale; columns: lag in days)

| irrigated | spei_scale | 0 | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 | 70 | 75 | 80 | 85 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 30 | 0.3900 | 0.4200 | 0.4000 | 0.3700 | 0.3400 | 0.3200 | 0.3300 | 0.3300 | 0.3500 | 0.3600 | 0.3700 | 0.3700 | 0.3400 | 0.3100 | 0.2700 | 0.2300 | 0.1700 | 0.1000 | 0.0500 |
| 0 | 60 | 0.4500 | 0.4400 | 0.4400 | 0.4200 | 0.4100 | 0.4000 | 0.4000 | 0.3900 | 0.3800 | 0.3700 | 0.3500 | 0.3100 | 0.2700 | 0.2300 | 0.2000 | 0.1700 | 0.1300 | 0.1200 | 0.1300 |
| 0 | 90 | 0.4900 | 0.4800 | 0.4600 | 0.4400 | 0.4100 | 0.3600 | 0.3400 | 0.3300 | 0.3300 | 0.3400 | 0.3300 | 0.3100 | 0.3000 | 0.2900 | 0.2900 | 0.2900 | 0.2800 | 0.2600 | 0.2500 |
| 1 | 30 | 0.2900 | 0.2900 | 0.2500 | 0.2000 | 0.1700 | 0.1700 | 0.1900 | 0.2000 | 0.2100 | 0.2100 | 0.2000 | 0.1800 | 0.1600 | 0.1400 | 0.1600 | 0.1800 | 0.1700 | 0.1400 | 0.1100 |
| 1 | 60 | 0.2600 | 0.2500 | 0.2300 | 0.2100 | 0.2000 | 0.1900 | 0.2000 | 0.2200 | 0.2100 | 0.2000 | 0.1900 | 0.1800 | 0.1900 | 0.1900 | 0.1700 | 0.1600 | 0.1400 | 0.1200 | 0.1100 |
| 1 | 90 | 0.2700 | 0.2700 | 0.2600 | 0.2500 | 0.2300 | 0.2200 | 0.2300 | 0.2400 | 0.2200 | 0.2100 | 0.2000 | 0.1900 | 0.1900 | 0.1800 | 0.1700 | 0.1800 | 0.1800 | 0.1700 | 0.1700 |

### Strongest link per site

| site | irrigated | spei_scale | lag_days | rho | n |
|---|---|---|---|---|---|
| Bal | 0 | 60 | 5 | 0.4030 | 1776 |
| Bal | 1 | 30 | 0 | 0.2690 | 813 |
| Cho | 0 | 90 | 10 | 0.5150 | 930 |
| Cho | 1 | 90 | 0 | 0.6000 | 548 |
| Din | 0 | 30 | 5 | 0.5600 | 1622 |
| Din | 1 | 60 | 0 | 0.2090 | 811 |
| Lep | 0 | 90 | 0 | 0.5360 | 767 |
| Lep | 1 | 90 | 0 | 0.5320 | 329 |
| Ped | 0 | 60 | 0 | 0.3320 | 2069 |
| Ped | 1 | 60 | 0 | 0.2240 | 832 |
| Pul | 0 | 60 | 5 | 0.2900 | 1226 |
| Pul | 1 | 60 | 0 | 0.1940 | 1253 |
| Sira | 0 | 90 | 0 | 0.4840 | 1866 |
| Sira | 1 | 60 | 0 | 0.4210 | 902 |
| Som | 0 | 90 | 85 | 0.5810 | 1024 |
| Som | 1 | 90 | 80 | 0.5120 | 535 |

## B. Does a weather alarm predict satellite-confirmed stress?

Alarm: SPEI-30 < -1.0 after >= 30 days above, in Jul-Nov. Confirmed: rainfed farmland SVI < -1 within 60 days. Base rate = same check for every crop-season date. An alarm is informative only if its confirmation rate is clearly above the base rate. Descriptive: alarms come from OBSERVED SPEI-30 (not from the weather module's forecasts), sites sharing a weather cell (Lepakshi, Cholasamudram) share alarm dates, and 3-7 alarms per site are too few for site-level tests. already_stressed_at_alarm = crops were below the threshold when the alarm fired (not a new onset); new_onset_confirmed counts only the others.

Two sources of site SVI (same label rules): median of the sampled rainfed fields, and the whole-area rainfed farmland. Share of Jul-Oct 2026 dates with an SVI value:

| site_code | median of sampled fields | whole-area farmland |
|---|---|---|
| Bal | 46% | 38% |
| Cho | 71% | 4% |
| Din | 46% | 38% |
| Lep | 58% | 0% |
| Ped | 54% | 33% |
| Pul | 62% | 33% |
| Sira | 71% | 33% |
| Som | 96% | 8% |

### Source: median of sampled fields

| site | alarms | confirmed | already_stressed_at_alarm | new_onset_confirmed | follow_up_incomplete | confirmation_rate | base_rate_any_date | median_delay_days |
|---|---|---|---|---|---|---|---|---|
| Bal | 7 | 5 | 0 | 5/7 | 1 | 0.7140 | 0.2120 | 5.0000 |
| Cho | 6 | 3 | 0 | 3/6 | 0 | 0.5000 | 0.3000 | 45.0000 |
| Din | 4 | 3 | 0 | 3/4 | 0 | 0.7500 | 0.2370 | 20.0000 |
| Lep | 6 | 3 | 0 | 3/6 | 0 | 0.5000 | 0.3560 | 55.0000 |
| Ped | 3 | 2 | 0 | 2/3 | 0 | 0.6670 | 0.1870 | 40.0000 |
| Pul | 7 | 3 | 1 | 2/6 | 1 | 0.4290 | 0.2390 | 10.0000 |
| Sira | 6 | 2 | 1 | 1/5 | 0 | 0.3330 | 0.2640 | 17.5000 |
| Som | 5 | 2 | 0 | 2/5 | 0 | 0.4000 | 0.4000 | 22.5000 |

### Source: whole-area farmland

| site | alarms | confirmed | already_stressed_at_alarm | new_onset_confirmed | follow_up_incomplete | confirmation_rate | base_rate_any_date | median_delay_days |
|---|---|---|---|---|---|---|---|---|
| Bal | 6 | 4 | 1 | 3/5 | 0 | 0.6670 | 0.3880 | 30.0000 |
| Cho | 4 | 1 | 0 | 1/4 | 0 | 0.2500 | 0.2960 | 30.0000 |
| Din | 4 | 3 | 1 | 2/3 | 0 | 0.7500 | 0.3480 | 5.0000 |
| Lep | 4 | 1 | 0 | 1/4 | 0 | 0.2500 | 0.2060 | 30.0000 |
| Ped | 2 | 2 | 0 | 2/2 | 0 | 1.0000 | 0.3680 | 25.0000 |
| Pul | 5 | 2 | 0 | 2/5 | 0 | 0.4000 | 0.2710 | 35.0000 |
| Sira | 6 | 4 | 0 | 4/6 | 0 | 0.6670 | 0.3170 | 37.5000 |
| Som | 2 | 0 | 0 | 0/2 | 0 | 0.0000 | 0.2460 |  |

## C. Mean Aug-Nov SVI of rainfed farmland per year (negative = worse than normal)

Compare with official drought declarations (data/official/drought_declarations.csv).

### Source: median of sampled fields

| site_code | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| Bal | 0.2900 | 0.4600 | -0.3400 | 0.5800 | -0.7800 | 0.1800 | 0.4500 | -0.9800 |
| Cho | 0.2300 | 0.4100 | 0.1200 | 0.5100 | -1.7600 | 0.8600 | 0.6900 | -1.6000 |
| Din | 0.4700 | 0.8400 | -1.3800 | 0.4200 | -0.9800 | 0.2400 | 0.6800 | -1.1700 |
| Lep | 0.1000 | 0.9900 | 0.6100 | -0.1600 | -0.8700 | 0.8900 | 0.7300 | -1.8800 |
| Ped | 0.2600 | 0.7700 | -0.2300 | 0.2600 | -0.7800 | 0.3100 | 0.0700 | -0.2900 |
| Pul | 0.0200 | -0.4700 | -0.2600 | 0.1400 | -0.0500 | -0.3500 | 0.5700 | -0.7300 |
| Sira | 0.2300 | 1.2000 | 0.5600 | -0.2400 | -1.3600 | 0.4500 | 0.2300 | -1.3400 |
| Som | -1.2300 | -0.0500 | 0.4000 | 0.7900 | -0.9500 | 0.7600 | 1.0900 | -2.1600 |

### Source: whole-area farmland

| site_code | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| Bal | 0.2700 | 0.6900 | -1.2300 | 1.3700 | -1.5800 | -0.2600 | 0.5300 | -1.5100 |
| Cho | 1.5700 |  |  | -0.2900 |  | 2.3500 | 0.9300 | -1.3900 |
| Din | 0.2100 | 0.6600 | -1.7800 | 0.5800 | -2.3100 | 0.5500 | 1.0600 | -2.3000 |
| Lep |  | 0.4400 |  | -1.1700 | -0.7700 | 1.5100 | 0.6600 |  |
| Ped | 1.3300 | 0.6000 | -0.8000 | 0.2700 | -1.2100 | 0.5200 | 0.1100 | -0.9300 |
| Pul | 0.5500 | 1.1200 | -1.1700 | 1.0100 | -0.1600 | 0.0600 | 1.1700 | -1.4700 |
| Sira | 0.8500 | 0.6700 | 0.4100 | -0.2700 | -3.2200 | 0.8100 | 0.0500 | -1.6400 |
| Som |  | 0.9400 |  |  | -0.2400 | 1.9700 | 1.8400 | -3.2500 |
