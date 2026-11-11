"""
Link step 2: real forecasts from the WEATHER MODULE for every satellite date (2019 onwards).

    python src/dataprep/weather_forecasts.py [--quick]

Uses the weather module's best configuration by validation (feature set weather_spei_doy,
XGBoost) and its own code and split: trained on 1979-2011, early stopping on 2012-2018,
so every forecast for 2019+ is out-of-sample. For each weather site and each day t it gives
P(Healthy / Moderate / Severe SPEI class) for t+7, t+15 and t+30, made with data up to day t,
for every day t up to the last day of weather data (also when t+h is not observed yet).

Runs in a separate Python process inside the weather module, because both repos have a
module called `config`. The fitted models are saved in models/ and re-used on later runs
(monthly updates only predict); --retrain fits them again. Extra AgERA5 cells
(data/weather_extra/) get forecasts too but are never used for training.
Output: data/clean/weather_forecasts.csv  (weather, date, h, p_healthy, p_moderate, p_severe)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def worker(weather_dir: Path, out: Path, horizons: list[int], feature_set: str, start: str, quick: bool,
           extra_dir: Path, model_dir: Path, retrain: bool):
    sys.path.insert(0, str(weather_dir / "src"))
    import time

    import numpy as np
    import pandas as pd
    from xgboost import XGBClassifier

    import config as WC                     # the WEATHER module's config
    from features.sequence_builder import add_doy_features, build_sequences_all_fields, load_prepared
    from features.splits import purged_periods

    flat = lambda a: a.reshape(len(a), -1)                        # noqa: E731

    def get_model(h, X_tr, y_tr, X_val, y_val):
        """Same model and settings as the weather module's trainers.train_xgb (seed 0), without
        importing its PyTorch code. Saved after the first fit and re-used (monthly runs only
        predict); --retrain fits again. Training data: weather-module sites only, 1979-2011,
        early stopping on 2012-2018 - unchanged by data appended later."""
        path = model_dir / f"weather_xgb_{feature_set}_h{h}{'_quick' if quick else ''}.json"
        clf = XGBClassifier()
        if path.exists() and not retrain:
            clf.load_model(path)
            return clf, f"loaded {path.name}"
        t0 = time.time()
        params = dict(WC.XGB_PARAMS)
        if quick:
            params.update(n_estimators=20, early_stopping_rounds=5)
        w = len(y_tr) / (3 * np.maximum(np.bincount(y_tr, minlength=3), 1))
        clf = XGBClassifier(random_state=0, **params)
        clf.fit(flat(X_tr), y_tr, sample_weight=w[y_tr], eval_set=[(flat(X_val), y_val)], verbose=False)
        model_dir.mkdir(parents=True, exist_ok=True)
        clf.save_model(path)
        return clf, f"trained in {time.time() - t0:.0f} s on {len(y_tr)} samples, saved {path.name}"

    def pad(df: pd.DataFrame, n: int) -> pd.DataFrame:
        """Append n placeholder days (copies of the last day) so the sequence builder also returns
        forecasts MADE on the most recent days, whose target days are not observed yet. Placeholder
        days never enter the input window of a kept forecast (filtered below) and are never scored."""
        last = df.iloc[[-1]]
        extra = pd.concat([last] * n, ignore_index=True)
        extra[WC.DATE_COLUMN] = last[WC.DATE_COLUMN].iloc[0] + pd.to_timedelta(np.arange(1, n + 1), "D")
        return pd.concat([df, extra], ignore_index=True)

    raw = load_prepared()
    for f in sorted(extra_dir.glob("*.csv")) if extra_dir.exists() else []:   # extra cells: forecast only
        raw[f.stem] = pd.read_csv(f, parse_dates=[WC.DATE_COLUMN])
        WC.FIELD_TO_CLUSTER[f.stem] = "extra"
    real_end = {k: v[WC.DATE_COLUMN].max() for k, v in raw.items()}
    frames = {k: add_doy_features(pad(v, max(horizons))) for k, v in raw.items()}
    parts = []
    for h in horizons:
        X, y, meta = build_sequences_all_fields(frames, feature_set, h)
        per = purged_periods(meta)
        t = pd.to_datetime(meta["last_input_date"])
        made_on_real_data = (t <= meta["field"].map(real_end)).to_numpy()
        use = (t >= pd.Timestamp(start)).to_numpy() & made_on_real_data
        own = meta["field"].isin(WC.FIELDS).to_numpy()                    # never train on extra cells
        tr, va = own & (per == "train"), own & (per == "val")
        clf, how = get_model(h, X[tr], y[tr], X[va], y[va])
        p = np.zeros((int(use.sum()), 3))
        p[:, clf.classes_.astype(int)] = clf.predict_proba(flat(X[use]))
        m = pd.DataFrame({"weather": meta.loc[use, "field"].to_numpy(), "date": t[use].dt.date.to_numpy(),
                          "h": h, "p_healthy": p[:, 0], "p_moderate": p[:, 1], "p_severe": p[:, 2]})
        parts.append(m)
        print(f"  weather forecast h={h:2d}: model {how}; {len(m)} forecasts from {start} "
              f"({meta.loc[use, 'field'].nunique()} cells)", flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(parts, ignore_index=True).to_csv(out, index=False)
    print(f"Wrote {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--retrain", action="store_true", help="fit the weather models again instead of loading models/")
    ap.add_argument("--worker", nargs=5, metavar=("WEATHER_DIR", "OUT", "SETTINGS", "EXTRA_DIR", "MODEL_DIR"),
                    help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.worker:
        wdir, out, settings, extra, mdir = a.worker
        hs, fs, start = settings.split("|")
        worker(Path(wdir), Path(out), [int(x) for x in hs.split(",")], fs, start, a.quick,
               Path(extra), Path(mdir), a.retrain)
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import config as C
    settings = "|".join([",".join(map(str, C.WEATHER_FC_HORIZONS)), C.WEATHER_FC_FEATURE_SET, C.WEATHER_FC_START])
    cmd = [sys.executable, str(Path(__file__).resolve()), "--worker", str(C.WEATHER_DIR),
           str(C.CLEAN_DIR / "weather_forecasts.csv"), settings, str(C.WEATHER_EXTRA_DIR), str(C.ROOT / "models")]
    cmd += (["--quick"] if a.quick else []) + (["--retrain"] if a.retrain else [])
    subprocess.run(cmd, check=True, cwd=str(C.WEATHER_DIR))


if __name__ == "__main__":
    main()
