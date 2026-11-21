# Pre-registration: rabi 2026-27 prospective test

**Registered:** 21 November 2026, before rabi 2026-27 (1 Dec 2026 – 31 Mar 2027) and before the Andhra Pradesh rabi 2026-27 drought order. The git commit that adds this file dates the registration. The rules are implemented in `src/analysis/rabi_extra.py` (`registered()`), and none of the constants below will be changed before the test is scored.

## Why
In the corrected replay (results/replay/REPLAY_REPORT.md), the integrated system confirmed **0 of 4** severe rabi mandal-seasons (2023-24, 2024-25) using in-season satellite images. Its only rabi confirmation (Kurnool Rural, 6 Dec 2023) rested on November images, which is carry-over of kharif stress.

A retrospective look at **rainfed** vegetation activity, done *after* seeing those seasons, suggested a signal: in 2024-25, rainfed activity was 45 % of normal at Dinnedevarapadu (Kurnool Rural) and 62 % at Balaji Villas (Kurnool Urban). Because the rule was chosen after seeing the data, it is a hypothesis. Rabi 2026-27 is the first season it can be tested on.

## Rules (fixed)

| Item | Registered choice |
|---|---|
| Field population | The rainfed sampled fields (frozen irrigation flag, `irrigated == 0`), all 8 sites, segments `field_segments_v2.geojson` |
| Data | `data/clean/fields_5day.csv` built by the unchanged pipeline (`build_dataset.py`, REF_CUTOFF 2023-12-31) from Earth Engine script B v2 exports |
| Active field | NDVI 90th percentile > 0.35 **and** 90th − 10th percentile > 0.15 in the window |
| **R1** (end of season) | Window 1 Dec 2026 – 31 Mar 2027; 5-day interpolated NDVI (`NDVI`); field needs ≥ 12 values |
| **R2** (early warning, issued 15 Feb 2027) | Window 1 Dec 2026 – 13 Feb 2027 (issue date − 2-day Sentinel-2 delay); causal NDVI (`NDVI_c`, no look-ahead); field needs ≥ 8 values |
| Normal | Mean active share of the same site, same rule and same window over rabi 2019-20, 2020-21, 2021-22, 2022-23 |
| Flag | Site active share < 75 % of its normal |
| Missing data | Fields below the value minimum are left out; a site with < 10 remaining rainfed fields is "insufficient" (not a flag, not a non-flag) |
| Evaluation unit | Mandal × rabi season; a mandal is flagged if any of its sites flags (Lepakshi + Cholasamudram = Lepakshi; Balaji Villas + Pullaiah = Kurnool Urban) |
| Outcome | Official AP rabi 2026-27 drought order (Severe / Moderate / Not declared) per mandal. Sira (Karnataka) and Peddakadubur (Adoni border) are scored only if a matching declaration exists and is unambiguous |
| Reported | Severe flagged x/n, moderate flagged x/n, not-declared flagged x/n, separately for R1 and R2, plus the unchanged replay with in-season vs carry-over confirmations |

## What the result can and cannot show
- R1 tests **end-of-season detection**. Only R2 (fixed issue date 15 Feb, causal data) tests an **early-warning** claim.
- One season and about 6 mandals give case evidence, not a statistical test. A hit or a miss is reported as it is.
- Declarations are administrative decisions, not field-level ground truth. The site-to-mandal assignment uses the site centre, not a polygon overlay.
- Post-hoc behaviour on 2023-24 – 2025-26 (shown in RABI_EXTRA_REPORT.md: R1 2/4 severe, R2 3/4 severe, 0/10 undeclared flagged) describes the rule; it is **not** evidence that the rule works.
