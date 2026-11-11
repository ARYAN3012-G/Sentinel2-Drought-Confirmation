"""
Step 5: forecast crop condition (SVI class) 15 / 30 days ahead — does the weather module help?

    python src/experiments/run_forecast.py                     # temporal + loco, all settings
    python src/experiments/run_forecast.py --split temporal --horizons 15 --seeds 0 --quick

Sample = one field at grid date t. Inputs (all from data available at t unless stated):
  sat     last 60 days of satellite: causal NDVI/NDMI/EVI/SVI/VCI + age of last image
  weather last 60 days of observed weather: P, ET0, water balance, T, RH, solar, wind, SPEI-30/60/90
  wxfc    weather-module forecast made at t: P(Healthy/Moderate/Severe SPEI) at t+7, t+15, t+30
  future  observed weather over (t, t+h] — UPPER BOUND ONLY (= a perfect weather forecast)
  static  day-of-year (sin/cos) and irrigated flag, in every version
Versions compared on IDENTICAL samples (config.FEATURE_SETS):
  1 satellite · 2 + past weather · 3 + weather-module forecast (integrated system)
  4 + future weather (upper bound) · reference: weather only
Target: SVI class at t+h. Split: temporal = TRAIN 2019-23 / VAL 2024 / TEST 2025-26, purged;
loco = train+val on one cluster, test on the other cluster's TEST years.
Scores: macro-F1 (3 classes) with CIs and paired differences vs persistence and vs version 1;
ONSET scores: among fields healthy at t, how well is a drop below normal at t+h predicted
(ROC-AUC, PR-AUC vs base rate) — persistence cannot predict onsets by definition.
Outputs: results/forecast/{REPORT_<split>.md, summary_<split>.csv, preds_*.npz}
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from sklearn.metrics import average_precision_score, roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

M = C.weather_module("evaluation/metrics.py")
to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "forecast"
K = 3
WXFC_COLS = [f"{c}_h{h}" for h in C.WEATHER_FC_HORIZONS for c in ("p_healthy", "p_moderate", "p_severe")]


# --------------------------------------------------------------------------- samples
def load_weather_forecasts() -> pd.DataFrame:
    fc = pd.read_csv(C.CLEAN_DIR / "weather_forecasts.csv", parse_dates=["date"])
    wide = fc.pivot_table(index=["weather", "date"], columns="h",
                          values=["p_healthy", "p_moderate", "p_severe"])
    wide.columns = [f"{c}_h{h}" for c, h in wide.columns]
    return wide[WXFC_COLS]


def future_block(wx: np.ndarray, t_idx: np.ndarray, H: int) -> np.ndarray:
    """Observed weather over steps t+1 ... t+H (days t+1 ... t+h): sums, means, SPEI at t+h."""
    col = {c: i for i, c in enumerate(C.WEATHER_FEATURES)}
    out = []
    for c in C.FUTURE_SUM + C.FUTURE_MEAN:
        v = np.stack([wx[t_idx + k, col[c]] for k in range(1, H + 1)], axis=1)
        out.append(v.sum(1) if c in C.FUTURE_SUM else v.mean(1))
    for c in C.FUTURE_AT_TARGET:
        out.append(wx[t_idx + H, col[c]])
    return np.column_stack(out)


def build_samples(h_days: int, live: bool = False):
    """live=True: also the most recent dates whose target (t+h) is not observed yet (for run_system);
    y = -1 there and the 'future' block is empty. Inputs are built exactly as in the evaluation."""
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    w = pd.read_csv(C.CLEAN_DIR / "weather_5day.csv", parse_dates=["date"]).set_index(["weather", "date"])
    fc = load_weather_forecasts()
    H, L = h_days // C.STEP_DAYS, C.INPUT_STEPS
    parts = {b: [] for b in ("sat", "weather", "wxfc", "future", "static")}
    metas = []
    for fid, g in f.sort_values("date").groupby("field_id", sort=True):
        n = len(g)
        if n < L + (0 if live else H):
            continue
        idx = pd.MultiIndex.from_arrays([g["weather"], g["date"]])
        dates = g["date"].to_numpy()
        wx = w.reindex(idx)[C.WEATHER_FEATURES].to_numpy(float)
        wf = fc.reindex(idx).to_numpy(float)
        sat = g[C.SAT_FEATURES].to_numpy(float)
        lab, lab_c, age = (g[c].to_numpy(float) for c in ("label", "label_c", "age_c"))
        t_idx = np.arange(L - 1, n if live else n - H)                    # window ends at t
        ws = sliding_window_view(sat, (L, sat.shape[1]))[:, 0][: len(t_idx)]
        ww = sliding_window_view(wx, (L, wx.shape[1]))[:, 0][: len(t_idx)]
        wft = wf[t_idx]
        if live:
            fut = np.zeros((len(t_idx), 0))
            tgt = np.array([lab[i + H] if i + H < n else np.nan for i in t_idx])
            keep = (age[t_idx] <= C.MAX_INPUT_AGE) & np.isfinite(ww).all(axis=(1, 2)) & np.isfinite(wft).all(1)
        else:
            fut = future_block(wx, t_idx, H)
            tgt = lab[t_idx + H]
            keep = (np.isfinite(tgt) & (age[t_idx] <= C.MAX_INPUT_AGE) & np.isfinite(ww).all(axis=(1, 2))
                    & np.isfinite(wft).all(1) & np.isfinite(fut).all(1))
        if not keep.any():
            continue
        t_idx = t_idx[keep]
        t_dates = pd.to_datetime(dates[t_idx])
        doy = t_dates.dayofyear.to_numpy()
        parts["sat"].append(ws[keep].reshape(len(t_idx), -1))
        parts["weather"].append(ww[keep].reshape(len(t_idx), -1))
        parts["wxfc"].append(wft[keep])
        parts["future"].append(fut[keep])
        parts["static"].append(np.column_stack([np.sin(2 * np.pi * doy / 365.25), np.cos(2 * np.pi * doy / 365.25),
                                                np.full(len(t_idx), g["irrigated"].iloc[0])]))
        metas.append(pd.DataFrame({
            "field_id": fid, "site_code": g["site_code"].iloc[0], "cluster": g["cluster"].iloc[0],
            "irrigated": g["irrigated"].iloc[0], "input_start": pd.to_datetime(dates[t_idx - L + 1]),
            "t": t_dates, "target_date": t_dates + pd.Timedelta(days=h_days),
            "y": np.nan_to_num(tgt[keep], nan=-1).astype(int), "label_t": lab_c[t_idx],
            "svi_t": g["SVI_c"].to_numpy(float)[t_idx],
            "svi_prev": g["SVI_c"].to_numpy(float)[t_idx - 3],              # 15 days earlier
            "age_t": age[t_idx]}))
    meta = pd.concat(metas, ignore_index=True)
    meta["period"] = meta["target_date"].dt.year.map(C.period_of_year)
    meta["input_period"] = meta["input_start"].dt.year.map(C.period_of_year)
    # a target label is interpolated from images up to MAX_GAP_DAYS after the target date
    meta["support_period"] = (meta["target_date"] + pd.Timedelta(days=C.MAX_GAP_DAYS)).dt.year.map(C.period_of_year)
    return {b: np.vstack(v) for b, v in parts.items()}, meta


def features(blocks, fs: str) -> np.ndarray:
    return np.hstack([blocks[b] for b in C.FEATURE_SETS[fs]] + [blocks["static"]])


def masks(meta: pd.DataFrame, split: str, fold: str | None):
    # purged: inputs, target AND the images the target label is interpolated from lie in one period
    purged = ((meta["period"] == meta["input_period"]) & (meta["period"] == meta["support_period"])).to_numpy()
    per = meta["period"].to_numpy()
    if split == "temporal":
        return {p: purged & (per == p) for p in ("train", "val", "test")}
    other = [c for c in meta["cluster"].unique() if c != fold][0]
    tr_cl = (meta["cluster"] == other).to_numpy()
    te_cl = (meta["cluster"] == fold).to_numpy()
    return {"train": purged & tr_cl & (per == "train"), "val": purged & tr_cl & (per == "val"),
            "test": purged & te_cl & (per == "test")}


# --------------------------------------------------------------------------- baselines
def onehot(c):
    p = np.zeros((len(c), K))
    p[np.arange(len(c)), c.astype(int)] = 1.0
    return p


def baselines(meta, mk):
    tr, te = meta[mk["train"]], meta[mk["test"]]
    bins = lambda d: (d.dt.dayofyear - 1) // 10                         # noqa: E731
    counts = (tr.assign(b=bins(tr["target_date"])).groupby(["site_code", "b"])["y"]
              .value_counts().unstack(fill_value=0).reindex(columns=range(K), fill_value=0))
    glob = np.bincount(tr["y"], minlength=K) + 1.0
    keys = list(zip(te["site_code"], bins(te["target_date"])))
    clim = np.array([(counts.loc[k].to_numpy() + 1.0) if k in counts.index else glob for k in keys])
    clim = clim / clim.sum(1, keepdims=True)
    lt = te["label_t"].to_numpy()
    pers = np.where(np.isfinite(lt)[:, None], onehot(np.nan_to_num(lt)), clim)
    maj = np.tile(onehot(np.array([glob.argmax()]))[0], (len(te), 1))
    return {"persistence": pers, "climatology": clim, "majority": maj}


# --------------------------------------------------------------------------- models
def class_weights(y):
    w = len(y) / (K * np.maximum(np.bincount(y, minlength=K), 1))
    return w[y]


def full_proba(model, X):
    p = np.zeros((len(X), K))
    p[:, model.classes_.astype(int)] = model.predict_proba(X)
    return p


def train_predict(name, X, y, mk, seed, quick):
    if name == "rf":
        from sklearn.ensemble import RandomForestClassifier
        params = dict(C.RF_PARAMS, random_state=seed)
        if quick:
            params["n_estimators"] = 30
        m = RandomForestClassifier(**params).fit(X[mk["train"]], y[mk["train"]])
        return full_proba(m, X[mk["test"]])
    if name == "xgb":
        from xgboost import XGBClassifier
        params = dict(C.XGB_PARAMS, random_state=seed, num_class=K, objective="multi:softprob")
        if quick:
            params.update(n_estimators=30, early_stopping_rounds=5)
        m = XGBClassifier(**params)
        m.fit(X[mk["train"]], y[mk["train"]], sample_weight=class_weights(y[mk["train"]]),
              eval_set=[(X[mk["val"]], y[mk["val"]])], verbose=False)
        return m.predict_proba(X[mk["test"]])
    raise ValueError(name)


# --------------------------------------------------------------------------- evaluation
def onset_scores(y, label_t, score_below, score_strong):
    """Among samples normal-or-above at t: ranking of a drop below normal (class >= 1) and of a
    drop to strongly below normal (class 2) at t+h. Scores: higher = more likely."""
    sel = label_t == 0
    out = {"onset_n": int(sel.sum())}
    for name, ev, sc in (("onset", y[sel] >= 1, score_below[sel]), ("onset_strong", y[sel] == 2, score_strong[sel])):
        ev = ev.astype(int)
        ok = sel.sum() >= 20 and 0 < ev.sum() < len(ev)
        out[f"{name}_rate"] = round(float(ev.mean()), 3) if ok else np.nan
        out[f"{name}_roc_auc"] = round(float(roc_auc_score(ev, sc)), 3) if ok else np.nan
        out[f"{name}_pr_auc"] = round(float(average_precision_score(ev, sc)), 3) if ok else np.nan
    return out


def onset_auc_diff_ci(y, label_t, s1, s2, blocks, n_boot):
    """Paired block bootstrap (blocks = target month) of onset ROC-AUC(s1) - ROC-AUC(s2)."""
    sel = label_t == 0
    ev, a, b, bl = (y[sel] >= 1).astype(int), s1[sel], s2[sel], blocks[sel]
    ub = np.unique(bl)
    idx = {k: np.where(bl == k)[0] for k in ub}
    rng = np.random.default_rng(C.BOOTSTRAP_SEED)
    d = []
    for _ in range(n_boot):
        ii = np.concatenate([idx[k] for k in rng.choice(ub, len(ub))])
        if 0 < ev[ii].sum() < len(ii):
            d.append(roc_auc_score(ev[ii], a[ii]) - roc_auc_score(ev[ii], b[ii]))
    return (float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))) if len(d) > 20 else (np.nan, np.nan)


def onset_reference_scores(meta, mk):
    """Simple onset baselines that need no forecast model (persistence gives every
    currently-normal field the same score, so its onset ROC-AUC is 0.5 by construction):
      svi_level  lower current SVI = more likely to drop;
      svi_trend  falling SVI over the last 15 days;
      svi_logit  logistic regression on SVI, its 15-day change, season (sin/cos) and image age,
                 fitted on TRAIN samples that were normal-or-above at t."""
    from sklearn.linear_model import LogisticRegression
    doy = meta["t"].dt.dayofyear.to_numpy()
    Z = np.column_stack([meta["svi_t"], meta["svi_t"] - meta["svi_prev"], np.sin(2 * np.pi * doy / 365.25),
                         np.cos(2 * np.pi * doy / 365.25), meta["age_t"]]).astype(float)
    Z = np.nan_to_num(Z, nan=0.0)
    y, lt = meta["y"].to_numpy(), meta["label_t"].to_numpy()
    tr = mk["train"] & (lt == 0)
    lr = LogisticRegression(max_iter=1000).fit(Z[tr], (y[tr] >= 1).astype(int))
    lr2 = LogisticRegression(max_iter=1000).fit(Z[tr], (y[tr] == 2).astype(int))
    te = mk["test"]
    lvl, trend = -Z[te, 0], -Z[te, 1]
    return {"svi_level": (lvl, lvl), "svi_trend": (trend, trend),
            "svi_logit": (lr.predict_proba(Z[te])[:, 1], lr2.predict_proba(Z[te])[:, 1])}


# Breakdowns of the same TEST predictions (models are not retrained): rainfed / irrigated fields,
# and the 2026 kharif drought (targets Jul-Nov 2026; confirmed by AgERA5 rain 31-57 % below normal).
SUBGROUPS = {
    "rainfed fields": lambda te: (te["irrigated"] == 0).to_numpy(),
    "irrigated fields": lambda te: (te["irrigated"] == 1).to_numpy(),
    "2026 drought season (targets Jul-Nov 2026)": lambda te: te["target_date"].between("2026-07-01", "2026-11-30").to_numpy(),
}


def evaluate(te, results, n_boot, onset_refs=None):
    """te: TEST rows of meta; results: {model: [probs per seed]} for exactly those rows;
    onset_refs: {name: (score below normal, score strongly below)} onset-only baselines."""
    y = te["y"].to_numpy()
    lt = te["label_t"].to_numpy()
    blocks = te["target_date"].dt.strftime("%Y-%m").to_numpy()
    # sensitivity: 90-day blocks (inputs span 60 days, SPEI up to 90 days)
    blocks90 = ((te["target_date"] - pd.Timestamp(C.GRID_START)).dt.days // 90).to_numpy()
    pers = results["baseline/persistence"][0].argmax(1)
    best_ref = onset_refs["svi_logit"][0] if onset_refs else None
    rows = []
    for key, probs in results.items():
        per_seed = [M.compute_metrics(y, p) for p in probs]
        row = {"model": key, "seeds": len(probs)}
        for m_ in ("macro_f1", "severe_f1", "balanced_accuracy", "roc_auc_macro_ovr"):
            v = [d.get(m_, np.nan) for d in per_seed]
            row[m_], row[m_ + "_std"] = np.nanmean(v), np.nanstd(v)
        pm = np.mean(probs, axis=0)
        row.update(onset_scores(y, lt, pm[:, 1] + pm[:, 2], pm[:, 2]))
        row.update(M.block_bootstrap(y, pm.argmax(1), blocks, n_boot=n_boot, seed=C.BOOTSTRAP_SEED,
                                     pred_ref=None if key == "baseline/persistence" else pers))
        if key != "baseline/persistence":
            b = M.block_bootstrap(y, pm.argmax(1), blocks90, n_boot=n_boot, seed=C.BOOTSTRAP_SEED, pred_ref=pers)
            row["vs_pers90_low"], row["vs_pers90_high"] = b.get("d_macro_f1_ci_low"), b.get("d_macro_f1_ci_high")
        if best_ref is not None and not key.startswith("baseline/"):
            row["onset_vs_logit_low"], row["onset_vs_logit_high"] = onset_auc_diff_ci(
                y, lt, pm[:, 1] + pm[:, 2], best_ref, blocks, min(n_boot, 500))
        fs, _, model = key.partition("/")
        ref1 = f"satellite/{model}"
        if fs not in ("baseline", "satellite") and ref1 in results:
            b = M.block_bootstrap(y, pm.argmax(1), blocks, n_boot=n_boot, seed=C.BOOTSTRAP_SEED,
                                  pred_ref=np.mean(results[ref1], axis=0).argmax(1))
            row["vs_sat_low"], row["vs_sat_high"] = b.get("d_macro_f1_ci_low"), b.get("d_macro_f1_ci_high")
        # does the weather MODULE's forecast add anything beyond past weather?
        ref2 = f"sat_pastweather/{model}"
        if fs == "sat_weatherforecast" and ref2 in results:
            b = M.block_bootstrap(y, pm.argmax(1), blocks, n_boot=n_boot, seed=C.BOOTSTRAP_SEED,
                                  pred_ref=np.mean(results[ref2], axis=0).argmax(1))
            row["vs_past_low"], row["vs_past_high"] = b.get("d_macro_f1_ci_low"), b.get("d_macro_f1_ci_high")
        rows.append(row)
    for name, (s1, s2) in (onset_refs or {}).items():
        rows.append({"model": f"onset-baseline/{name}", "seeds": 1, **onset_scores(y, lt, s1, s2)})
    return pd.DataFrame(rows)


def ci(a, b):
    return "" if a is None or pd.isna(a) else f"[{a:+.3f}, {b:+.3f}]"


def write_report(split, tables, info):
    lines = [f"# Satellite forecast results — split `{split}`", "",
             "Target: SVI class h days ahead (normal or above / below normal / strongly below normal; index "
             "categories, not validated crop-damage classes), sampled farmland fields. Macro-F1 on the "
             "untouched TEST data: mean ± std over seeds [95% block-bootstrap CI, blocks = target month]. "
             "Δ columns: paired bootstrap CI of the difference; entirely above 0 = better than the reference. "
             "Δ vs persistence (90-d blocks) = the same comparison with 90-day blocks (sensitivity; inputs "
             "span 60 days, SPEI up to 90). Onset: among fields normal-or-above at t, ranking of a drop below "
             "normal (onset) or to strongly below normal (onset strong) at t+h. Persistence scores 0.5 there "
             "by construction, so the fair references are the onset baselines (current SVI level, its 15-day "
             "trend, and a logistic model on both + season + image age); onset Δ vs logit = paired CI of the "
             "ROC-AUC difference to that logistic baseline. Samples are purged when inputs, target or the "
             "images the target label is interpolated from cross a period boundary.", "",
             "Leave-one-cluster-out = transfer of the CROP model to the other cluster. Its inputs still come "
             "from the weather module trained on all 7 weather sites and from each field's own SVI normal, "
             "so it is not a fully unseen-region test.", "",
             "Versions: 1 `satellite` · 2 `sat_pastweather` · 3 `sat_weatherforecast` (integrated "
             "weather -> satellite system) · 4 `sat_futureweather_UPPERBOUND` (perfect weather "
             "forecast, not a usable model) · reference `weather_only`. Δ vs past weather (version 3 "
             "only): does the weather module's forecast add skill beyond the past weather of version 2?", ""]
    for (fold, h), df in tables.items():
        i = info[(fold, h)]
        lines += [f"## {fold} — horizon {h} days", "",
                  f"Samples: train {i['train']}, val {i['val']}, test {i['test']}. "
                  f"Test class shares: {i['test_classes']}.", ""]
        none = pd.Series([None] * len(df))
        t = pd.DataFrame({
            "model": df["model"],
            "macro-F1": ["" if pd.isna(r.macro_f1) else
                         f"{r.macro_f1:.3f}" + (f" ± {r.macro_f1_std:.3f}" if r.seeds > 1 else "")
                         + f" [{r.macro_f1_ci_low:.3f}, {r.macro_f1_ci_high:.3f}]" for r in df.itertuples()],
            "Δ vs persistence": [ci(a, b) for a, b in zip(df.get("d_macro_f1_ci_low", none),
                                                          df.get("d_macro_f1_ci_high", none))],
            "Δ vs satellite only": [ci(a, b) for a, b in zip(df.get("vs_sat_low", none),
                                                             df.get("vs_sat_high", none))],
            "Δ vs past weather": [ci(a, b) for a, b in zip(df.get("vs_past_low", none),
                                                           df.get("vs_past_high", none))],
            "Δ vs persistence (90-d blocks)": [ci(a, b) for a, b in zip(df.get("vs_pers90_low", none),
                                                                        df.get("vs_pers90_high", none))],
            "strongly-below F1": df["severe_f1"].round(3),
            "onset ROC-AUC": df["onset_roc_auc"], "onset PR-AUC": df["onset_pr_auc"],
            "onset Δ vs logit": [ci(a, b) for a, b in zip(df.get("onset_vs_logit_low", none),
                                                          df.get("onset_vs_logit_high", none))],
            "onset strong ROC-AUC": df["onset_strong_roc_auc"],
            "onset rate": df["onset_rate"]})
        lines += [to_md(t, index=False), ""]
    (OUT / f"REPORT_{split}.md").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", nargs="+", default=["temporal", "loco"], choices=["temporal", "loco"])
    ap.add_argument("--horizons", nargs="+", type=int, default=C.HORIZONS)
    ap.add_argument("--feature-sets", nargs="+", default=list(C.FEATURE_SETS))
    ap.add_argument("--models", nargs="+", default=C.MODELS)
    ap.add_argument("--seeds", nargs="+", type=int, default=C.SEEDS)
    ap.add_argument("--n-boot", type=int, default=C.BOOTSTRAP_N)
    ap.add_argument("--quick", action="store_true", help="tiny models, for a smoke test")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    for split in a.split:
        folds = [None] if split == "temporal" else ["kurnool", "south"]
        tables, info, summary = {}, {}, []
        for h in a.horizons:
            blocks, meta = build_samples(h)
            y = meta["y"].to_numpy()
            for fold in folds:
                mk = masks(meta, split, fold)
                name = "all_sites" if fold is None else f"test_{fold}"
                te_y = y[mk["test"]]
                info[(name, h)] = {p: int(mk[p].sum()) for p in mk} | {
                    "test_classes": " / ".join(f"{C.CLASS_NAMES[c]} {np.mean(te_y == c):.0%}" for c in range(K))}
                results = {f"baseline/{k}": [v] for k, v in baselines(meta, mk).items()}
                for fs in a.feature_sets:
                    X = features(blocks, fs)
                    for model in a.models:
                        probs = []
                        for s in a.seeds:
                            t0 = time.time()
                            probs.append(train_predict(model, X, y, mk, s, a.quick))
                            print(f"{split} {name} h{h} {fs:30s} {model} seed{s}  {time.time() - t0:.0f}s",
                                  flush=True)
                        results[f"{fs}/{model}"] = probs
                nb = 100 if a.quick else a.n_boot
                te = meta[mk["test"]]
                orefs = onset_reference_scores(meta, mk)
                df = evaluate(te, results, nb, orefs)
                tables[(name, h)] = df
                summary.append(df.assign(split=split, fold=name, horizon=h))
                for sub, rule in SUBGROUPS.items():
                    sel = rule(te)
                    if sel.sum() < 200 or len(np.unique(te_y[sel])) < 2:
                        continue
                    sname = f"{name} · {sub}"
                    info[(sname, h)] = {"train": info[(name, h)]["train"], "val": info[(name, h)]["val"],
                                        "test": int(sel.sum()), "test_classes": " / ".join(
                                            f"{C.CLASS_NAMES[c]} {np.mean(te_y[sel] == c):.0%}" for c in range(K))}
                    sdf = evaluate(te[sel], {k: [p[sel] for p in v] for k, v in results.items()}, nb,
                                   {k: (v[0][sel], v[1][sel]) for k, v in orefs.items()})
                    tables[(sname, h)] = sdf
                    summary.append(sdf.assign(split=split, fold=sname, horizon=h))
                np.savez_compressed(OUT / f"preds_{split}_{name}_h{h}.npz", y=te_y,
                                    field_id=te["field_id"].to_numpy(str),
                                    t=te["t"].dt.strftime("%Y-%m-%d").to_numpy(str),
                                    target_date=te["target_date"].dt.strftime("%Y-%m-%d").to_numpy(str),
                                    **{k.replace("/", "__"): np.mean(v, 0) for k, v in results.items()})
        pd.concat(summary).to_csv(OUT / f"summary_{split}.csv", index=False)
        write_report(split, tables, info)
        (OUT / f"run_{split}.json").write_text(json.dumps(vars(a), indent=1))
        print(f"Wrote {OUT / f'REPORT_{split}.md'}")


if __name__ == "__main__":
    main()
