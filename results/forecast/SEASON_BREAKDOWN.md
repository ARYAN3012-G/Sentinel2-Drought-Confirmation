# Forecast scores by season (macro-F1)

The headline tables pool all months. Here the same test predictions are split by the season of the target date: kharif = Jun-Nov, rabi = Dec-Mar, other = Apr-May. Weather class: the saved final weather models (one seed of the XGBoost hybrid, trained 1979-2011) on target dates from 2019 - a check of the season pattern, not a replacement for the weather module's 5-seed tables. The crop-condition forecast split comes from run_forecast.py (subgroups in REPORT_temporal.md, next full run).

| stage | model | all months | kharif (Jun-Nov) | other (Apr-May) | rabi (Dec-Mar) |
|---|---|---|---|---|---|
| weather class +7 d | persistence | 0.6580 | 0.7120 | 0.6830 | 0.5210 |
| weather class +7 d | hybrid XGBoost (seed 0) | 0.8100 | 0.8230 | 0.7730 | 0.8100 |
| weather class +15 d | persistence | 0.5120 | 0.5440 | 0.5520 | 0.3630 |
| weather class +15 d | hybrid XGBoost (seed 0) | 0.6310 | 0.6060 | 0.6220 | 0.6510 |
| weather class +30 d | persistence | 0.4220 | 0.4250 | 0.3550 | 0.4310 |
| weather class +30 d | hybrid XGBoost (seed 0) | 0.4170 | 0.4100 | 0.3400 | 0.4480 |

Number of test samples:

| stage | all months | kharif (Jun-Nov) | other (Apr-May) | rabi (Dec-Mar) |
|---|---|---|---|---|
| weather class +7 d | 17178 | 8616 | 2928 | 5634 |
| weather class +15 d | 17178 | 8616 | 2928 | 5634 |
| weather class +30 d | 17178 | 8616 | 2928 | 5634 |

Balanced accuracy and sample counts per row: season_breakdown.csv.
