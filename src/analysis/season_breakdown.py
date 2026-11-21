"""
Season breakdown of the forecast scores (the headline tables pool every month of the year).

Splits test scores by the season of the TARGET date: kharif = Jun-Nov, rabi = Dec-Mar, other = Apr-May.
No model is retrained.

 Weather drought class (stage 1): the saved final weather models (XGBoost, feature set
    WEATHER_FC_FEATURE_SET, seed 0, trained 1979-2011) used by the satellite module; forecasts for
    target dates in the weather module's TEST period (2019 onwards) are out of sample. This is ONE seed
    of ONE model, a check of the season pattern - not a replacement for the weather module's tables
    (5 seeds, purged split), whose per-day predictions were not saved.
Persistence = the class on the issue date carried forward.
The crop-condition forecast (stage 2) gets the same split from run_forecast.py itself (subgroups
"kharif targets (Jun-Nov)" / "rabi targets (Dec-Mar)" in REPORT_<split>.md, next full run).

    python src/analysis/season_breakdown.py
Output: results/forecast/{season_breakdown.csv, SEASON_BREAKDOWN.md}
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "forecast"
WEATHER_PREPARED = C.WEATHER_DIR / "data" / "prepared"
TEST_START = "2019-01-01"


def season(dates: pd.Series) -> pd.Series:
    m = pd.to_datetime(dates).dt.month
    return pd.Series(np.select([m.between(6, 11), m.isin([12, 1, 2, 3])], ["kharif (Jun-Nov)", "rabi (Dec-Mar)"],
                               "other (Apr-May)"), index=dates.index)


def scores(y, p) -> dict:
    return dict(n=len(y), macro_f1=round(f1_score(y, p, average="macro", labels=[0, 1, 2]), 3),
                balanced_accuracy=round(balanced_accuracy_score(y, p), 3))


def weather_stage() -> pd.DataFrame:
    fc = pd.read_csv(C.CLEAN_DIR / "weather_forecasts.csv", parse_dates=["date"])
    lab = []
    for p in WEATHER_PREPARED.glob("*.csv"):
        d = pd.read_csv(p, usecols=["valid_time", "field", "label"], parse_dates=["valid_time"])
        lab.append(d.rename(columns={"valid_time": "date", "field": "weather"}))
    lab = pd.concat(lab).dropna(subset=["label"])
    lab["label"] = lab["label"].astype(int)
    rows = []
    for h in sorted(fc.h.unique()):
        f = fc[fc.h == h].copy()
        f["target"] = f.date + pd.Timedelta(days=int(h))
        f = f.merge(lab.rename(columns={"date": "target", "label": "y"}), on=["weather", "target"])
        f = f.merge(lab.rename(columns={"label": "y_now"}), on=["weather", "date"])
        f = f[f.target >= TEST_START]
        pred = f[["p_healthy", "p_moderate", "p_severe"]].to_numpy().argmax(1)
        s = season(f.target)
        for sn in ["all months"] + sorted(s.unique()):
            k = np.ones(len(f), bool) if sn == "all months" else (s == sn).to_numpy()
            for name, pr in (("persistence", f.y_now.to_numpy()), ("hybrid XGBoost (seed 0)", pred)):
                rows.append(dict(stage=f"weather class +{h} d", model=name, season=sn,
                                 **scores(f.y.to_numpy()[k], pr[k])))
    return pd.DataFrame(rows)


def main():
    t = weather_stage()
    t.to_csv(OUT / "season_breakdown.csv", index=False)
    wide = t.pivot_table(index=["stage", "model"], columns="season", values="macro_f1", sort=False)
    n = t.drop_duplicates(["stage", "season"]).pivot_table(index="stage", columns="season", values="n", sort=False)
    lines = ["# Forecast scores by season (macro-F1)", "",
             "The headline tables pool all months. Here the same test predictions are split by the season of the "
             "target date: kharif = Jun-Nov, rabi = Dec-Mar, other = Apr-May. Weather class: the saved final "
             "weather models (one seed of the XGBoost hybrid, trained 1979-2011) on target dates from 2019 - a check "
             "of the season pattern, not a replacement for the weather module's 5-seed tables. The crop-condition "
             "forecast split comes from run_forecast.py (subgroups in REPORT_temporal.md, next full run).", "",
             to_md(wide.round(3)), "", "Number of test samples:", "", to_md(n.astype(int)), "",
             "Balanced accuracy and sample counts per row: season_breakdown.csv.", ""]
    (OUT / "SEASON_BREAKDOWN.md").write_text("\n".join(lines), encoding="utf-8")
    print(wide.round(3).to_string())
    print(n.astype(int).to_string())


if __name__ == "__main__":
    main()
