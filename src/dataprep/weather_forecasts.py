"""
Link step 2: real forecasts from the WEATHER MODULE for every satellite date (2019 onwards).

    python src/dataprep/weather_forecasts.py [--quick]

Uses the weather module's best configuration by validation (feature set weather_spei_doy,
XGBoost) and its own code and split: trained on 1979-2011, early stopping on 2012-2018,
so every forecast for 2019+ is out-of-sample. For each weather site and each day t it gives
P(Healthy / Moderate / Severe SPEI class) for t+7, t+15 and t+30, made with data up to day t.

Runs in a separate Python process inside the weather module, because both repos have a
module called `config`.
Output: data/clean/weather_forecasts.csv  (weather, date, h, p_healthy, p_moderate, p_severe)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def worker(weather_dir: Path, out: Path, horizons: list[int], feature_set: str, start: str, quick: bool):
    sys.path.insert(0, str(weather_dir / "src"))
    import time

    import numpy as np
    import pandas as pd
    from xgboost import XGBClassifier

    import config as WC                     # the WEATHER module's config
    from features.sequence_builder import add_doy_features, build_sequences_all_fields, load_prepared
    from features.splits import purged_periods

    def train_xgb(X_tr, y_tr, X_val, y_val, X_new):
        """Same model and settings as the weather module's trainers.train_xgb (seed 0), without
        importing its PyTorch code (not needed for XGBoost and blocked on some computers)."""
        t0 = time.time()
        params = dict(WC.XGB_PARAMS)
        if quick:
            params.update(n_estimators=20, early_stopping_rounds=5)
        w = len(y_tr) / (3 * np.maximum(np.bincount(y_tr, minlength=3), 1))
        flat = lambda a: a.reshape(len(a), -1)                    # noqa: E731
        clf = XGBClassifier(random_state=0, **params)
        clf.fit(flat(X_tr), y_tr, sample_weight=w[y_tr], eval_set=[(flat(X_val), y_val)], verbose=False)
        p = np.zeros((len(X_new), 3))
        p[:, clf.classes_] = clf.predict_proba(flat(X_new))
        return p, round(time.time() - t0, 1)

    frames = {k: add_doy_features(v) for k, v in load_prepared().items()}
    parts = []
    for h in horizons:
        X, y, meta = build_sequences_all_fields(frames, feature_set, h)
        per = purged_periods(meta)
        t = pd.to_datetime(meta["last_input_date"])
        use = (t >= pd.Timestamp(start)).to_numpy()
        p, secs = train_xgb(X[per == "train"], y[per == "train"], X[per == "val"], y[per == "val"], X[use])
        info = {"train_time_s": secs}
        m = pd.DataFrame({"weather": meta.loc[use, "field"].to_numpy(), "date": t[use].dt.date.to_numpy(),
                          "h": h, "p_healthy": p[:, 0], "p_moderate": p[:, 1], "p_severe": p[:, 2]})
        parts.append(m)
        print(f"  weather forecast h={h:2d}: trained on {int((per == 'train').sum())} samples, "
              f"{len(m)} forecasts from {start} ({info['train_time_s']} s)", flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(parts, ignore_index=True).to_csv(out, index=False)
    print(f"Wrote {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--worker", nargs=3, metavar=("WEATHER_DIR", "OUT", "SETTINGS"), help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.worker:
        wdir, out, settings = a.worker
        hs, fs, start = settings.split("|")
        worker(Path(wdir), Path(out), [int(x) for x in hs.split(",")], fs, start, a.quick)
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import config as C
    settings = "|".join([",".join(map(str, C.WEATHER_FC_HORIZONS)), C.WEATHER_FC_FEATURE_SET, C.WEATHER_FC_START])
    cmd = [sys.executable, str(Path(__file__).resolve()), "--worker", str(C.WEATHER_DIR),
           str(C.CLEAN_DIR / "weather_forecasts.csv"), settings] + (["--quick"] if a.quick else [])
    subprocess.run(cmd, check=True, cwd=str(C.WEATHER_DIR))


if __name__ == "__main__":
    main()
