# Satellite forecast results — split `loco`

Target: crop-condition class from SVI (Healthy / Moderate / Severe) h days ahead, sampled farmland fields. Macro-F1 on the untouched TEST data: mean ± std over seeds [95% block-bootstrap CI, blocks = target month]. Δ columns: paired bootstrap CI of the difference; entirely above 0 = significantly better. Onset: among fields Healthy at t, ranking of a drop below normal at t+h (ROC-AUC 0.5 = no skill; PR-AUC vs base rate).

Versions: 1 `satellite` · 2 `sat_pastweather` · 3 `sat_weatherforecast` (integrated weather -> satellite system) · 4 `sat_futureweather_UPPERBOUND` (perfect weather forecast, not a usable model) · reference `weather_only`.

## test_kurnool — horizon 15 days

Samples: train 19308, val 3334, test 5531. Test class shares: Healthy 52% / Moderate 43% / Severe 5%.

| model | macro-F1 | Δ vs persistence | Δ vs satellite only | severe-F1 | onset ROC-AUC | onset PR-AUC | onset rate |
|---|---|---|---|---|---|---|---|
| baseline/persistence | 0.626 [0.579, 0.674] |  |  | 0.3940 | 0.5000 | 0.2130 | 0.2130 |
| baseline/climatology | 0.227 [0.208, 0.241] | [-0.456, -0.343] |  | 0.0000 | 0.5000 | 0.2130 | 0.2130 |
| baseline/majority | 0.227 [0.208, 0.241] | [-0.456, -0.343] |  | 0.0000 | 0.5000 | 0.2130 | 0.2130 |
| satellite/rf | 0.599 ± 0.004 [0.544, 0.655] | [-0.056, +0.013] |  | 0.2860 | 0.7230 | 0.3910 | 0.2130 |
| satellite/xgb | 0.603 ± 0.002 [0.555, 0.654] | [-0.049, +0.008] |  | 0.3040 | 0.7480 | 0.4390 | 0.2130 |
| sat_pastweather/rf | 0.598 ± 0.002 [0.547, 0.659] | [-0.052, +0.008] | [-0.031, +0.024] | 0.2940 | 0.7130 | 0.3940 | 0.2130 |
| sat_pastweather/xgb | 0.629 ± 0.003 [0.580, 0.683] | [-0.018, +0.027] | [+0.006, +0.042] | 0.3860 | 0.7520 | 0.4450 | 0.2130 |
| sat_weatherforecast/rf | 0.600 ± 0.003 [0.546, 0.659] | [-0.053, +0.010] | [-0.032, +0.025] | 0.3010 | 0.7150 | 0.3980 | 0.2130 |
| sat_weatherforecast/xgb | 0.628 ± 0.002 [0.580, 0.685] | [-0.015, +0.027] | [+0.009, +0.041] | 0.3810 | 0.7520 | 0.4470 | 0.2130 |
| sat_futureweather_UPPERBOUND/rf | 0.601 ± 0.004 [0.549, 0.667] | [-0.049, +0.017] | [-0.026, +0.031] | 0.2970 | 0.7220 | 0.4050 | 0.2130 |
| sat_futureweather_UPPERBOUND/xgb | 0.630 ± 0.004 [0.587, 0.682] | [-0.011, +0.029] | [+0.013, +0.044] | 0.3810 | 0.7570 | 0.4590 | 0.2130 |
| weather_only/rf | 0.357 ± 0.002 [0.293, 0.391] | [-0.363, -0.209] | [-0.330, -0.196] | 0.0070 | 0.5080 | 0.2120 | 0.2130 |
| weather_only/xgb | 0.357 ± 0.001 [0.277, 0.392] | [-0.375, -0.202] | [-0.344, -0.193] | 0.0160 | 0.5180 | 0.2170 | 0.2130 |

## test_south — horizon 15 days

Samples: train 20082, val 2767, test 5646. Test class shares: Healthy 57% / Moderate 40% / Severe 4%.

| model | macro-F1 | Δ vs persistence | Δ vs satellite only | severe-F1 | onset ROC-AUC | onset PR-AUC | onset rate |
|---|---|---|---|---|---|---|---|
| baseline/persistence | 0.657 [0.597, 0.735] |  |  | 0.4990 | 0.5000 | 0.2020 | 0.2020 |
| baseline/climatology | 0.242 [0.214, 0.266] | [-0.483, -0.361] |  | 0.0000 | 0.5000 | 0.2020 | 0.2020 |
| baseline/majority | 0.242 [0.214, 0.266] | [-0.483, -0.361] |  | 0.0000 | 0.5000 | 0.2020 | 0.2020 |
| satellite/rf | 0.645 ± 0.002 [0.590, 0.711] | [-0.045, +0.022] |  | 0.4280 | 0.7470 | 0.4430 | 0.2020 |
| satellite/xgb | 0.629 ± 0.005 [0.589, 0.673] | [-0.083, +0.009] |  | 0.3850 | 0.7600 | 0.4440 | 0.2020 |
| sat_pastweather/rf | 0.555 ± 0.004 [0.475, 0.664] | [-0.152, -0.041] | [-0.137, -0.023] | 0.1710 | 0.7600 | 0.4320 | 0.2020 |
| sat_pastweather/xgb | 0.595 ± 0.005 [0.512, 0.700] | [-0.108, -0.007] | [-0.094, +0.055] | 0.2870 | 0.7670 | 0.4380 | 0.2020 |
| sat_weatherforecast/rf | 0.559 ± 0.005 [0.480, 0.683] | [-0.145, -0.024] | [-0.131, -0.005] | 0.1780 | 0.7600 | 0.4370 | 0.2020 |
| sat_weatherforecast/xgb | 0.599 ± 0.007 [0.524, 0.706] | [-0.093, +0.001] | [-0.080, +0.062] | 0.2890 | 0.7730 | 0.4480 | 0.2020 |
| sat_futureweather_UPPERBOUND/rf | 0.556 ± 0.006 [0.477, 0.664] | [-0.156, -0.038] | [-0.139, -0.024] | 0.1700 | 0.7630 | 0.4360 | 0.2020 |
| sat_futureweather_UPPERBOUND/xgb | 0.599 ± 0.008 [0.517, 0.704] | [-0.105, -0.003] | [-0.089, +0.062] | 0.2800 | 0.7900 | 0.4630 | 0.2020 |
| weather_only/rf | 0.323 ± 0.004 [0.275, 0.354] | [-0.409, -0.294] | [-0.392, -0.278] | 0.0000 | 0.5470 | 0.2120 | 0.2020 |
| weather_only/xgb | 0.318 ± 0.004 [0.280, 0.347] | [-0.422, -0.286] | [-0.361, -0.272] | 0.0010 | 0.5280 | 0.1970 | 0.2020 |

## test_kurnool — horizon 30 days

Samples: train 18567, val 3080, test 5161. Test class shares: Healthy 52% / Moderate 43% / Severe 5%.

| model | macro-F1 | Δ vs persistence | Δ vs satellite only | severe-F1 | onset ROC-AUC | onset PR-AUC | onset rate |
|---|---|---|---|---|---|---|---|
| baseline/persistence | 0.506 [0.464, 0.551] |  |  | 0.2090 | 0.5000 | 0.3000 | 0.3000 |
| baseline/climatology | 0.228 [0.212, 0.242] | [-0.333, -0.232] |  | 0.0000 | 0.5000 | 0.3000 | 0.3000 |
| baseline/majority | 0.228 [0.212, 0.242] | [-0.333, -0.232] |  | 0.0000 | 0.5000 | 0.3000 | 0.3000 |
| satellite/rf | 0.467 ± 0.003 [0.431, 0.511] | [-0.063, -0.012] |  | 0.0620 | 0.6310 | 0.4290 | 0.3000 |
| satellite/xgb | 0.487 ± 0.004 [0.458, 0.515] | [-0.048, +0.004] |  | 0.0900 | 0.6650 | 0.4600 | 0.3000 |
| sat_pastweather/rf | 0.451 ± 0.002 [0.412, 0.493] | [-0.079, -0.026] | [-0.028, -0.006] | 0.0390 | 0.6200 | 0.4140 | 0.3000 |
| sat_pastweather/xgb | 0.504 ± 0.003 [0.456, 0.547] | [-0.023, +0.017] | [-0.005, +0.041] | 0.1610 | 0.6820 | 0.4830 | 0.3000 |
| sat_weatherforecast/rf | 0.452 ± 0.003 [0.410, 0.495] | [-0.080, -0.026] | [-0.028, -0.008] | 0.0410 | 0.6190 | 0.4100 | 0.3000 |
| sat_weatherforecast/xgb | 0.498 ± 0.004 [0.457, 0.542] | [-0.028, +0.017] | [-0.005, +0.032] | 0.1450 | 0.6800 | 0.4720 | 0.3000 |
| sat_futureweather_UPPERBOUND/rf | 0.453 ± 0.001 [0.416, 0.498] | [-0.078, -0.022] | [-0.024, -0.003] | 0.0350 | 0.6380 | 0.4250 | 0.3000 |
| sat_futureweather_UPPERBOUND/xgb | 0.506 ± 0.004 [0.460, 0.552] | [-0.025, +0.028] | [-0.008, +0.050] | 0.1490 | 0.6960 | 0.4910 | 0.3000 |
| weather_only/rf | 0.354 ± 0.003 [0.293, 0.387] | [-0.236, -0.101] | [-0.188, -0.080] | 0.0070 | 0.5110 | 0.3030 | 0.3000 |
| weather_only/xgb | 0.350 ± 0.007 [0.278, 0.387] | [-0.255, -0.099] | [-0.216, -0.098] | 0.0400 | 0.5220 | 0.3110 | 0.3000 |

## test_south — horizon 30 days

Samples: train 19119, val 2514, test 5430. Test class shares: Healthy 57% / Moderate 40% / Severe 3%.

| model | macro-F1 | Δ vs persistence | Δ vs satellite only | severe-F1 | onset ROC-AUC | onset PR-AUC | onset rate |
|---|---|---|---|---|---|---|---|
| baseline/persistence | 0.537 [0.468, 0.601] |  |  | 0.3190 | 0.5000 | 0.2890 | 0.2890 |
| baseline/climatology | 0.242 [0.213, 0.267] | [-0.356, -0.232] |  | 0.0000 | 0.5000 | 0.2890 | 0.2890 |
| baseline/majority | 0.242 [0.213, 0.267] | [-0.356, -0.232] |  | 0.0000 | 0.5000 | 0.2890 | 0.2890 |
| satellite/rf | 0.470 ± 0.003 [0.410, 0.522] | [-0.117, -0.034] |  | 0.0940 | 0.6650 | 0.4450 | 0.2890 |
| satellite/xgb | 0.464 ± 0.002 [0.418, 0.508] | [-0.130, -0.025] |  | 0.1120 | 0.6820 | 0.4430 | 0.2890 |
| sat_pastweather/rf | 0.444 ± 0.003 [0.400, 0.487] | [-0.140, -0.057] | [-0.041, -0.006] | 0.0060 | 0.7000 | 0.4720 | 0.2890 |
| sat_pastweather/xgb | 0.459 ± 0.005 [0.402, 0.528] | [-0.145, -0.025] | [-0.025, +0.033] | 0.0670 | 0.7200 | 0.4830 | 0.2890 |
| sat_weatherforecast/rf | 0.439 ± 0.001 [0.397, 0.477] | [-0.150, -0.058] | [-0.057, -0.008] | 0.0000 | 0.6960 | 0.4670 | 0.2890 |
| sat_weatherforecast/xgb | 0.461 ± 0.004 [0.407, 0.527] | [-0.142, -0.023] | [-0.021, +0.030] | 0.0700 | 0.7200 | 0.4860 | 0.2890 |
| sat_futureweather_UPPERBOUND/rf | 0.447 ± 0.004 [0.403, 0.483] | [-0.140, -0.055] | [-0.050, -0.000] | 0.0060 | 0.6980 | 0.4670 | 0.2890 |
| sat_futureweather_UPPERBOUND/xgb | 0.459 ± 0.003 [0.402, 0.526] | [-0.140, -0.029] | [-0.024, +0.027] | 0.0560 | 0.7080 | 0.4710 | 0.2890 |
| weather_only/rf | 0.321 ± 0.003 [0.266, 0.365] | [-0.264, -0.180] | [-0.194, -0.104] | 0.0000 | 0.5500 | 0.2900 | 0.2890 |
| weather_only/xgb | 0.330 ± 0.009 [0.303, 0.361] | [-0.262, -0.144] | [-0.166, -0.090] | 0.0000 | 0.5700 | 0.3010 | 0.2890 |
