# Satellite forecast results — split `temporal`

Target: crop-condition class from SVI (Healthy / Moderate / Severe) h days ahead, sampled farmland fields. Macro-F1 on the untouched TEST data: mean ± std over seeds [95% block-bootstrap CI, blocks = target month]. Δ columns: paired bootstrap CI of the difference; entirely above 0 = significantly better. Onset: among fields Healthy at t, ranking of a drop below normal at t+h (ROC-AUC 0.5 = no skill; PR-AUC vs base rate).

Versions: 1 `satellite` · 2 `sat_pastweather` · 3 `sat_weatherforecast` (integrated weather -> satellite system) · 4 `sat_futureweather_UPPERBOUND` (perfect weather forecast, not a usable model) · reference `weather_only`.

## all_sites — horizon 15 days

Samples: train 39390, val 6101, test 11177. Test class shares: Healthy 54% / Moderate 41% / Severe 4%.

| model | macro-F1 | Δ vs persistence | Δ vs satellite only | severe-F1 | onset ROC-AUC | onset PR-AUC | onset rate |
|---|---|---|---|---|---|---|---|
| baseline/persistence | 0.637 [0.588, 0.691] |  |  | 0.4360 | 0.5000 | 0.2070 | 0.2070 |
| baseline/climatology | 0.335 [0.299, 0.362] | [-0.358, -0.262] |  | 0.0000 | 0.4520 | 0.1970 | 0.2070 |
| baseline/majority | 0.234 [0.217, 0.251] | [-0.458, -0.354] |  | 0.0000 | 0.5000 | 0.2070 | 0.2070 |
| satellite/rf | 0.634 ± 0.002 [0.588, 0.693] | [-0.015, +0.015] |  | 0.3790 | 0.7650 | 0.4480 | 0.2070 |
| satellite/xgb | 0.632 ± 0.002 [0.589, 0.688] | [-0.021, +0.012] |  | 0.3820 | 0.7730 | 0.4650 | 0.2070 |
| sat_pastweather/rf | 0.623 ± 0.003 [0.567, 0.693] | [-0.029, +0.013] | [-0.029, +0.006] | 0.3450 | 0.7740 | 0.4530 | 0.2070 |
| sat_pastweather/xgb | 0.656 ± 0.003 [0.616, 0.709] | [+0.004, +0.034] | [+0.009, +0.041] | 0.4320 | 0.7900 | 0.4780 | 0.2070 |
| sat_weatherforecast/rf | 0.628 ± 0.003 [0.576, 0.696] | [-0.025, +0.017] | [-0.024, +0.012] | 0.3590 | 0.7720 | 0.4540 | 0.2070 |
| sat_weatherforecast/xgb | 0.655 ± 0.003 [0.615, 0.710] | [+0.008, +0.032] | [+0.010, +0.039] | 0.4350 | 0.7910 | 0.4810 | 0.2070 |
| sat_futureweather_UPPERBOUND/rf | 0.628 ± 0.002 [0.573, 0.693] | [-0.025, +0.018] | [-0.025, +0.011] | 0.3560 | 0.7790 | 0.4600 | 0.2070 |
| sat_futureweather_UPPERBOUND/xgb | 0.659 ± 0.002 [0.620, 0.709] | [+0.008, +0.038] | [+0.013, +0.045] | 0.4350 | 0.8030 | 0.4950 | 0.2070 |
| weather_only/rf | 0.361 ± 0.002 [0.333, 0.386] | [-0.334, -0.232] | [-0.333, -0.235] | 0.0030 | 0.5560 | 0.2210 | 0.2070 |
| weather_only/xgb | 0.377 ± 0.002 [0.356, 0.391] | [-0.315, -0.219] | [-0.312, -0.214] | 0.0450 | 0.5580 | 0.2190 | 0.2070 |

## all_sites — horizon 30 days

Samples: train 37686, val 5594, test 10591. Test class shares: Healthy 55% / Moderate 41% / Severe 4%.

| model | macro-F1 | Δ vs persistence | Δ vs satellite only | severe-F1 | onset ROC-AUC | onset PR-AUC | onset rate |
|---|---|---|---|---|---|---|---|
| baseline/persistence | 0.519 [0.472, 0.569] |  |  | 0.2530 | 0.5000 | 0.2940 | 0.2940 |
| baseline/climatology | 0.334 [0.302, 0.360] | [-0.229, -0.153] |  | 0.0000 | 0.4560 | 0.2840 | 0.2940 |
| baseline/majority | 0.235 [0.217, 0.253] | [-0.333, -0.237] |  | 0.0000 | 0.5000 | 0.2940 | 0.2940 |
| satellite/rf | 0.493 ± 0.002 [0.435, 0.552] | [-0.047, -0.003] |  | 0.1230 | 0.6870 | 0.4610 | 0.2940 |
| satellite/xgb | 0.505 ± 0.001 [0.466, 0.558] | [-0.033, +0.009] |  | 0.1730 | 0.6960 | 0.4680 | 0.2940 |
| sat_pastweather/rf | 0.470 ± 0.002 [0.415, 0.528] | [-0.073, -0.021] | [-0.038, -0.002] | 0.0530 | 0.7080 | 0.4690 | 0.2940 |
| sat_pastweather/xgb | 0.523 ± 0.006 [0.467, 0.588] | [-0.014, +0.024] | [-0.004, +0.040] | 0.2090 | 0.7100 | 0.4720 | 0.2940 |
| sat_weatherforecast/rf | 0.472 ± 0.003 [0.420, 0.526] | [-0.073, -0.024] | [-0.039, -0.002] | 0.0570 | 0.7060 | 0.4670 | 0.2940 |
| sat_weatherforecast/xgb | 0.526 ± 0.002 [0.478, 0.586] | [-0.016, +0.028] | [+0.002, +0.038] | 0.2210 | 0.7110 | 0.4730 | 0.2940 |
| sat_futureweather_UPPERBOUND/rf | 0.475 ± 0.002 [0.421, 0.537] | [-0.069, -0.012] | [-0.033, +0.005] | 0.0590 | 0.7130 | 0.4710 | 0.2940 |
| sat_futureweather_UPPERBOUND/xgb | 0.528 ± 0.004 [0.482, 0.595] | [-0.010, +0.035] | [+0.010, +0.042] | 0.2140 | 0.7310 | 0.4920 | 0.2940 |
| weather_only/rf | 0.355 ± 0.005 [0.314, 0.384] | [-0.213, -0.127] | [-0.187, -0.096] | 0.0040 | 0.5400 | 0.3040 | 0.2940 |
| weather_only/xgb | 0.362 ± 0.004 [0.329, 0.391] | [-0.212, -0.112] | [-0.199, -0.104] | 0.0280 | 0.5270 | 0.2890 | 0.2940 |
