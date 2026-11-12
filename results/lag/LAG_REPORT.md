# Weather drought -> crop stress

## A. Lag correlation (Spearman rho between SVI on day t and SPEI-k on day t-lag)

Descriptive association over all available years, best of 3 scales x 19 lags (not a causal lag; SPEI-90 at lag 0 already summarises the previous 90 days of weather).

Crop-season steps (Jul-Nov) with a label. Positive rho = wetter weather, healthier crops.

### Median over sites (rows: irrigated 0/1, SPEI scale; columns: lag in days)

| irrigated | spei_scale | 0 | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 | 70 | 75 | 80 | 85 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 30 | 0.4000 | 0.4300 | 0.4200 | 0.4000 | 0.3600 | 0.3200 | 0.3000 | 0.3300 | 0.3500 | 0.3600 | 0.3800 | 0.3700 | 0.3500 | 0.3100 | 0.2800 | 0.2600 | 0.2300 | 0.1900 | 0.1500 |
| 0 | 60 | 0.4200 | 0.4300 | 0.4300 | 0.4300 | 0.4100 | 0.4000 | 0.4100 | 0.4000 | 0.3900 | 0.3800 | 0.3700 | 0.3400 | 0.3100 | 0.3000 | 0.2800 | 0.2600 | 0.2200 | 0.2000 | 0.1900 |
| 0 | 90 | 0.4700 | 0.4700 | 0.4600 | 0.4500 | 0.4300 | 0.4000 | 0.3500 | 0.3600 | 0.3700 | 0.3700 | 0.3700 | 0.3500 | 0.3400 | 0.3300 | 0.3200 | 0.3100 | 0.2900 | 0.2700 | 0.2600 |
| 1 | 30 | 0.2400 | 0.2600 | 0.2700 | 0.2500 | 0.2200 | 0.2000 | 0.2000 | 0.2000 | 0.2100 | 0.2100 | 0.2200 | 0.2100 | 0.1800 | 0.1600 | 0.1500 | 0.1400 | 0.1000 | 0.0600 | 0.0400 |
| 1 | 60 | 0.2800 | 0.2700 | 0.2600 | 0.2600 | 0.2500 | 0.2500 | 0.2400 | 0.2400 | 0.2300 | 0.2200 | 0.2100 | 0.1900 | 0.1700 | 0.1400 | 0.1200 | 0.1100 | 0.0900 | 0.0900 | 0.1000 |
| 1 | 90 | 0.2800 | 0.2700 | 0.2600 | 0.2600 | 0.2400 | 0.2100 | 0.2000 | 0.1800 | 0.1700 | 0.1700 | 0.1700 | 0.1800 | 0.1700 | 0.1500 | 0.1600 | 0.1600 | 0.1600 | 0.1500 | 0.1300 |

### Strongest link per site

| site | irrigated | spei_scale | lag_days | rho | n |
|---|---|---|---|---|---|
| Bal | 0 | 30 | 5 | 0.4090 | 1686 |
| Bal | 1 | 30 | 5 | 0.1090 | 777 |
| Cho | 0 | 90 | 0 | 0.5770 | 732 |
| Cho | 1 | 30 | 5 | 0.3620 | 572 |
| Din | 0 | 90 | 0 | 0.5930 | 1468 |
| Din | 1 | 60 | 0 | 0.3370 | 1040 |
| Lep | 0 | 90 | 0 | 0.5050 | 854 |
| Lep | 1 | 90 | 10 | 0.3190 | 505 |
| Ped | 0 | 30 | 10 | 0.2120 | 2013 |
| Ped | 1 | 30 | 10 | 0.2890 | 1051 |
| Pul | 0 | 60 | 5 | 0.2460 | 1893 |
| Pul | 1 | 90 | 0 | 0.2600 | 883 |
| Sira | 0 | 60 | 0 | 0.6160 | 2201 |
| Sira | 1 | 60 | 0 | 0.4180 | 486 |
| Som | 0 | 30 | 75 | 0.5750 | 812 |
| Som | 1 | 60 | 50 | 0.3030 | 423 |

## B. Does a weather alarm predict satellite-confirmed stress?

Alarm: SPEI-30 < -1.0 after >= 30 days above, in Jul-Nov. Confirmed: rainfed farmland SVI < -1 within 60 days. Base rate = same check for every crop-season date. An alarm is informative only if its confirmation rate is clearly above the base rate. Descriptive: alarms come from OBSERVED SPEI-30 (not from the weather module's forecasts), sites sharing a weather cell (Lepakshi, Cholasamudram) share alarm dates, and 3-7 alarms per site are too few for site-level tests. already_stressed_at_alarm = crops were below the threshold when the alarm fired (not a new onset); new_onset_confirmed counts only the others.

Two sources of site SVI (same label rules): median of the sampled rainfed fields, and the whole-area rainfed farmland. Share of Jul-Oct 2026 dates with an SVI value:

| site_code | median of sampled fields | whole-area farmland |
|---|---|---|
| Bal | 46% | 38% |
| Cho | 58% | 4% |
| Din | 46% | 38% |
| Lep | 46% | 0% |
| Ped | 79% | 33% |
| Pul | 67% | 33% |
| Sira | 71% | 33% |
| Som | 58% | 8% |

### Source: median of sampled fields

| site | alarms | confirmed | already_stressed_at_alarm | new_onset_confirmed | follow_up_incomplete | confirmation_rate | base_rate_any_date | median_delay_days |
|---|---|---|---|---|---|---|---|---|
| Bal | 7 | 6 | 1 | 5/6 | 1 | 0.8570 | 0.2900 | 17.5000 |
| Cho | 6 | 4 | 0 | 4/6 | 0 | 0.6670 | 0.3760 | 32.5000 |
| Din | 4 | 3 | 1 | 2/3 | 0 | 0.7500 | 0.3550 | 10.0000 |
| Lep | 6 | 3 | 1 | 2/5 | 0 | 0.5000 | 0.3440 | 55.0000 |
| Ped | 3 | 0 | 0 | 0/3 | 0 | 0.0000 | 0.0560 |  |
| Pul | 7 | 2 | 0 | 2/7 | 1 | 0.2860 | 0.1030 | 7.5000 |
| Sira | 6 | 3 | 1 | 2/5 | 0 | 0.5000 | 0.2890 | 30.0000 |
| Som | 5 | 1 | 0 | 1/5 | 0 | 0.2000 | 0.3940 | 55.0000 |

### Source: whole-area farmland

| site | alarms | confirmed | already_stressed_at_alarm | new_onset_confirmed | follow_up_incomplete | confirmation_rate | base_rate_any_date | median_delay_days |
|---|---|---|---|---|---|---|---|---|
| Bal | 6 | 4 | 1 | 3/5 | 0 | 0.6670 | 0.3700 | 30.0000 |
| Cho | 4 | 1 | 0 | 1/4 | 0 | 0.2500 | 0.2960 | 30.0000 |
| Din | 4 | 3 | 1 | 2/3 | 0 | 0.7500 | 0.3480 | 5.0000 |
| Lep | 4 | 1 | 0 | 1/4 | 0 | 0.2500 | 0.2060 | 30.0000 |
| Ped | 2 | 2 | 0 | 2/2 | 0 | 1.0000 | 0.3680 | 25.0000 |
| Pul | 5 | 2 | 0 | 2/5 | 0 | 0.4000 | 0.2740 | 35.0000 |
| Sira | 6 | 4 | 0 | 4/6 | 0 | 0.6670 | 0.3170 | 37.5000 |
| Som | 3 | 0 | 0 | 0/3 | 0 | 0.0000 | 0.3330 |  |

## C. Mean Aug-Nov SVI of rainfed farmland per year (negative = worse than normal)

Compare with official drought declarations (data/official/drought_declarations.csv).

### Source: median of sampled fields

| site_code | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| Bal | 0.3600 | 0.4600 | -0.9200 | 0.5400 | -0.8500 | 0.1600 | 0.5500 | -0.8800 |
| Cho | 0.1100 | 1.0300 | 0.3400 | 0.3900 | -1.7400 | 0.8700 | 0.5900 | -1.4700 |
| Din | 0.2400 | 0.7100 | -0.9200 | 0.3900 | -1.4100 | 0.1200 | 0.2900 | -1.3900 |
| Lep | 0.2000 | 0.7200 | 0.3800 | -0.2500 | -1.2300 | 0.7300 | 0.6500 | -0.9800 |
| Ped | -0.2400 | 0.3700 | -0.1600 | 0.5400 | -0.4800 | 0.2500 | 0.3200 | 0.2400 |
| Pul | -0.1600 | 0.6300 | -0.2800 | 0.2300 | -0.3600 | -0.3000 | -0.1300 | -0.5100 |
| Sira | 0.7600 | 0.6900 | 0.2900 | -0.1400 | -1.5400 | 0.7500 | 0.0300 | -1.9800 |
| Som | -0.4800 | 0.0100 | 0.4100 | 1.1500 | -1.0900 | 1.0400 | 0.5200 | -1.4800 |

### Source: whole-area farmland

| site_code | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| Bal | 0.2900 | 0.6800 | -1.2400 | 1.3400 | -1.5900 | -0.2300 | 0.4900 | -1.5500 |
| Cho | 1.5900 |  |  | -0.2700 |  | 2.2800 | 0.9000 | -1.3300 |
| Din | 0.3800 | 0.6200 | -1.7200 | 0.5600 | -2.4900 | 0.4800 | 0.9900 | -2.3200 |
| Lep |  | 0.4400 |  | -1.1000 | -0.8200 | 1.4300 | 0.5900 |  |
| Ped | 1.2500 | 0.6100 | -0.8300 | 0.3300 | -1.2400 | 0.5300 | 0.1400 | -0.9500 |
| Pul | 0.5700 | 0.9400 | -1.3100 | 1.0300 | -0.2000 | 0.1000 | 1.1900 | -1.5700 |
| Sira | 0.8900 | 0.6700 | 0.4000 | -0.3000 | -3.1000 | 0.7800 | 0.0500 | -1.5900 |
| Som |  | 0.6100 | 0.8500 | 0.2200 | -0.9300 | 3.1200 | 1.8900 | -3.9100 |
