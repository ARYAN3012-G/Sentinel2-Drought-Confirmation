"""
The integrated system for one date: weather alarm -> satellite confirmation -> fields for the drone.

    python src/system/run_system.py --train                 # once: train + save the crop model
    python src/system/run_system.py --date 2026-09-15       # any date with data
    python src/system/run_system.py                         # latest date with data

Monthly use (no retraining): add the new weather days (weather module: tools/update_agera5.py),
export the new Sentinel-2 dates (Earth Engine script B), then run build_dataset, weather_link,
weather_forecasts and this script. Models, SPEI calibration and SVI normals stay frozen; retrain
once a year, after the season, if wanted.

Stage 1 (weather module, trained 1979-2011): SPEI-30/90 on the date and the forecast SPEI class
          for +7/+15/+30 days. ALARM if SPEI-30 < -1 now or the +15-day forecast is Severe.
Stage 2 (satellite): latest SVI of the 20 sampled rainfed fields per site (images at most
          30 days old). CONFIRMED if the median rainfed SVI < -1 (same rule as the lag analysis).
Status: DROUGHT (alarm + confirmed) · DROUGHT continuing (confirmed, SPEI-30 recovered but
          SPEI-90 < -1) · WATCH (alarm, crops not yet stressed) · CROP STRESS without alarm · normal.
Stage 3 (targeting): candidate RAINFED fields for a visit, two lists per site:
          - stressed now: SVI < -1, lowest first (below the field's normal - not measured damage);
          - at risk: normal now, ranked by the crop model's 15-day risk score (>= MIN_RISK_SCORE;
            a ranking score, not a calibrated probability). Only for dates the model did not
            train on (2025 onwards); earlier dates show the stressed-now list only.
Missing or stale data never reads as "no stress": too few satellite fields -> INSUFFICIENT
satellite data; weather or forecast older than MAX_DATA_AGE_DAYS -> not used.
Outputs: results/system/<date>/{SYSTEM_REPORT.md, fields_to_fly.csv, fields_to_fly.kml}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "experiments"))
import run_forecast as RF  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
MODEL_DIR = C.ROOT / "models"
OUT = C.RESULTS_DIR / "system"
H = 15
FEATURE_SET = "sat_weatherforecast"          # version 3: the integrated weather -> satellite model
MIN_SAT_FIELDS = 5            # rainfed fields with a recent image needed to confirm / rule out stress
MAX_DATA_AGE_DAYS = 5         # weather observation and forecast must be at most this old
MIN_RISK_SCORE = 0.5          # at-risk list: only fields with a risk score of at least this
FIRST_UNSEEN_YEAR = C.TEST_YEARS[0]          # crop model trained on 2019-2023, early stopping on 2024
CLASS = ["Healthy", "Moderate", "Severe"]


def model_path() -> Path:
    return MODEL_DIR / f"crop_xgb_{FEATURE_SET}_h{H}.json"


def train():
    """Same model and split as the evaluation (TRAIN 2019-23, early stopping on VAL 2024, seed 0)."""
    from xgboost import XGBClassifier
    blocks, meta = RF.build_samples(H)
    X, y = RF.features(blocks, FEATURE_SET), meta["y"].to_numpy()
    mk = RF.masks(meta, "temporal", None)
    params = dict(C.XGB_PARAMS, random_state=0, num_class=RF.K, objective="multi:softprob")
    m = XGBClassifier(**params)
    m.fit(X[mk["train"]], y[mk["train"]], sample_weight=RF.class_weights(y[mk["train"]]),
          eval_set=[(X[mk["val"]], y[mk["val"]])], verbose=False)
    MODEL_DIR.mkdir(exist_ok=True)
    m.save_model(model_path())
    info = {"feature_set": FEATURE_SET, "horizon_days": H, "n_features": int(X.shape[1]),
            "train_samples": int(mk["train"].sum()), "val_samples": int(mk["val"].sum()),
            "trained_on_target_years": "2019-2023 (early stopping on 2024)"}
    model_path().with_suffix(".info.json").write_text(json.dumps(info, indent=1))
    print(f"Saved {model_path()}  ({info['train_samples']} training samples)")


def _ring_area_centroid(ring):
    """Shoelace area (degree units, for weighting only) and area centroid of one ring."""
    x = np.array([q[0] for q in ring]); y = np.array([q[1] for q in ring])
    cr = x[:-1] * y[1:] - x[1:] * y[:-1]
    a = cr.sum() / 2
    if abs(a) < 1e-15:
        return 0.0, x.mean(), y.mean()
    return abs(a), ((x[:-1] + x[1:]) * cr).sum() / (6 * a), ((y[:-1] + y[1:]) * cr).sum() / (6 * a)


def field_geometry() -> pd.DataFrame:
    g = json.loads(C.SEGMENTS_FILE.read_text())
    rows = []
    for f in g["features"]:
        geom = f["geometry"]                     # Polygon, or MultiPolygon for a split segment
        parts = [geom["coordinates"][0]] if geom["type"] == "Polygon" else [p[0] for p in geom["coordinates"]]
        areas = [_ring_area_centroid(r) for r in parts]
        a_tot = sum(a for a, _, _ in areas)
        lon = sum(a * x for a, x, _ in areas) / a_tot if a_tot else np.mean([q[0] for q in parts[0]])
        lat = sum(a * y for a, _, y in areas) / a_tot if a_tot else np.mean([q[1] for q in parts[0]])
        rows.append({"field_id": f["properties"]["field_id"], "lat": round(lat, 6), "lon": round(lon, 6),
                     "rings": parts})
    return pd.DataFrame(rows).set_index("field_id")


def weather_status(date: pd.Timestamp) -> pd.DataFrame:
    w = pd.read_csv(C.CLEAN_DIR / "weather_5day.csv", parse_dates=["date"])
    fc = pd.read_csv(C.CLEAN_DIR / "weather_forecasts.csv", parse_dates=["date"])
    rows = []
    for code in C.SITE_ORDER:
        wx = C.SITES[code]["weather"]
        ww = w[(w.weather == wx) & (w.date <= date)].tail(1)
        fresh = len(ww) and (date - ww.date.iloc[0]).days <= MAX_DATA_AGE_DAYS
        rec = {"site": code, "weather_date": ww.date.iloc[0].date() if len(ww) else None,
               "SPEI30": round(float(ww.SPEI30.iloc[0]), 2) if fresh else np.nan,
               "SPEI90": round(float(ww.SPEI90.iloc[0]), 2) if fresh else np.nan}
        for h in C.WEATHER_FC_HORIZONS:
            # only a forecast ISSUED within MAX_DATA_AGE_DAYS before the date; never an old one
            ff = fc[(fc.weather == wx) & (fc.h == h) & (fc.date <= date)
                    & (fc.date > date - pd.Timedelta(days=MAX_DATA_AGE_DAYS))].tail(1)
            if len(ff):
                p = ff[["p_healthy", "p_moderate", "p_severe"]].to_numpy()[0]
                rec[f"forecast_+{h}d"] = f"{CLASS[int(p.argmax())]} ({p.max():.0%}), issued {ff.date.iloc[0].date()}"
                rec[f"_cls{h}"] = int(p.argmax())
            else:
                rec[f"forecast_+{h}d"] = "missing"
        rec["weather_ok"] = bool(fresh)
        rec["ALARM"] = bool(fresh and ((rec["SPEI30"] < C.ALARM_SPEI) or rec.get(f"_cls{H}") == 2))
        rows.append(rec)
    return pd.DataFrame(rows)


def satellite_status(f: pd.DataFrame, date: pd.Timestamp) -> tuple[pd.DataFrame, pd.DataFrame]:
    now = f[(f.date <= date) & (f.date > date - pd.Timedelta(days=C.STEP_DAYS))]
    now = now[now.age_c <= C.MAX_INPUT_AGE]
    rows = []
    for code in C.SITE_ORDER:
        r = now[(now.site_code == code) & (now.irrigated == 0) & now.SVI_c.notna()]
        enough = len(r) >= MIN_SAT_FIELDS
        med = float(r.SVI_c.median()) if len(r) else np.nan
        rows.append({"site": code, "rainfed_fields_with_data": len(r),
                     "median_image_age_days": float(r.age_c.median()) if len(r) else np.nan,
                     "median_SVI": round(med, 2) if len(r) else np.nan,
                     "fields_below_normal": f"{(r.SVI_c < C.STRESS_Z).mean():.0%}" if len(r) else "",
                     "fields_strongly_below": f"{(r.SVI_c < -1.5).mean():.0%}" if len(r) else "",
                     "satellite_ok": bool(enough),
                     "CONFIRMED": bool(enough and med < C.STRESS_Z)})
    return pd.DataFrame(rows), now


def at_risk(date: pd.Timestamp) -> pd.DataFrame | None:
    if date.year < FIRST_UNSEEN_YEAR:
        return None
    from xgboost import XGBClassifier
    if not model_path().exists():
        sys.exit("No saved model - run: python src/system/run_system.py --train")
    blocks, meta = RF.build_samples(H, live=True)
    sel = (meta["t"] == date).to_numpy()
    if not sel.any():
        return pd.DataFrame()
    m = XGBClassifier()
    m.load_model(model_path())
    p = RF.full_proba(m, RF.features(blocks, FEATURE_SET)[sel])
    out = meta.loc[sel, ["field_id", "site_code", "irrigated", "label_t", "svi_t"]].copy()
    out["onset_risk"] = p[:, 1] + p[:, 2]          # a ranking score, not a calibrated probability
    out["p_severe"] = p[:, 2]
    return out


def write_kml(rows: pd.DataFrame, geo: pd.DataFrame, path: Path, title: str):
    pm = []
    for r in rows.itertuples():
        if r.field_id not in geo.index:
            continue
        polys = "".join("<Polygon><outerBoundaryIs><LinearRing><coordinates>"
                        + " ".join(f"{q[0]},{q[1]},0" for q in ring)
                        + "</coordinates></LinearRing></outerBoundaryIs></Polygon>"
                        for ring in geo.loc[r.field_id, "rings"])
        colour = "ff0000ff" if r.reason.startswith("stressed") else "ff00a5ff"
        pm.append(f"<Placemark><name>{r.site} {r.rank}: {r.reason}</name><description>{r.field_id}; "
                  f"{r.area_ha} ha; SVI {r.SVI_now}; risk score {r.risk_score_15d}</description>"
                  f"<Style><LineStyle><color>{colour}</color><width>3</width></LineStyle>"
                  f"<PolyStyle><fill>0</fill></PolyStyle></Style><MultiGeometry>{polys}</MultiGeometry></Placemark>")
    path.write_text('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2">'
                    f"<Document><name>{title}</name>{''.join(pm)}</Document></kml>", encoding="utf-8")


def run(date: pd.Timestamp | None, n_per_list: int):
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    if date is None:
        date = f.loc[f.SVI_c.notna(), "date"].max()
    date = f.loc[f.date <= date, "date"].max()                        # snap to the 5-day grid
    wx = weather_status(date)
    sat, now = satellite_status(f, date)
    risk = at_risk(date)
    geo = field_geometry()
    static = f.groupby("field_id")[["site_code", "area_ha", "irrigated"]].first()

    # Population: RAINFED sampled fields (the population the confirmation rule and the drought
    # question are about). Two candidate lists, both shortlists for a field visit, not measured damage.
    lists = []
    for code in C.SITE_ORDER:
        dmg = now[(now.site_code == code) & (now.irrigated == 0) & (now.SVI_c < C.STRESS_Z)]
        dmg = dmg.sort_values("SVI_c").head(n_per_list)
        lists.append(pd.DataFrame({"site": code, "field_id": dmg.field_id, "reason": "stressed now (satellite candidate)",
                                   "SVI_now": dmg.SVI_c.round(2), "image_age_days": dmg.age_c,
                                   "risk_score_15d": np.nan}))
        if risk is not None and len(risk):
            rk = risk[(risk.site_code == code) & (risk.irrigated == 0) & (risk.label_t == 0)
                      & (risk.onset_risk >= MIN_RISK_SCORE)].sort_values("onset_risk", ascending=False)
            rk = rk.head(n_per_list)
            lists.append(pd.DataFrame({"site": code, "field_id": rk.field_id, "reason": "at risk (normal now)",
                                       "SVI_now": rk.svi_t.round(2), "image_age_days": np.nan,
                                       "risk_score_15d": rk.onset_risk.round(2)}))
    fly = pd.concat(lists, ignore_index=True)
    fly["rank"] = fly.groupby(["site", "reason"]).cumcount() + 1
    fly = fly.join(static[["area_ha", "irrigated"]], on="field_id").join(geo[["lat", "lon"]], on="field_id")
    # hand-off record: what the selection was based on
    wmap = wx.set_index("site")
    fly["issue_date"] = str(date.date())
    fly["weather_obs_date"] = fly["site"].map(wmap["weather_date"]).astype(str)
    fly["weather_forecast_+15d"] = fly["site"].map(wmap[f"forecast_+{H}d"])
    fly["crop_model"] = model_path().name if risk is not None else ""
    fly["svi_reference"] = f"2019-{C.REF_CUTOFF[:4]}, own year excluded"

    od = OUT / str(date.date())
    od.mkdir(parents=True, exist_ok=True)
    cols = ["site", "reason", "rank", "field_id", "lat", "lon", "area_ha", "irrigated", "SVI_now", "image_age_days",
            "risk_score_15d", "issue_date", "weather_obs_date", "weather_forecast_+15d", "crop_model", "svi_reference"]
    fly[cols].to_csv(od / "fields_to_fly.csv", index=False)
    write_kml(fly, geo, od / "fields_to_fly.kml", f"Fields to fly, {date.date()}")

    summary = wx[["site", "SPEI30", "SPEI90", "weather_ok", "ALARM"]].merge(
        sat[["site", "rainfed_fields_with_data", "median_SVI", "fields_below_normal", "satellite_ok", "CONFIRMED"]],
        on="site")
    # Crops follow SPEI-90 best (lag analysis): after late rain SPEI-30 can recover while the
    # 90-day deficit and the crop stress persist -> "continuing", not "over".
    ok_w, ok_s = summary.weather_ok, summary.satellite_ok
    continuing = ~summary.ALARM & summary.CONFIRMED & (summary.SPEI90 < C.ALARM_SPEI)
    summary["status"] = np.select(
        [~ok_w, summary.ALARM & ~ok_s, ~ok_s,
         summary.ALARM & summary.CONFIRMED, continuing, summary.ALARM & ~summary.CONFIRMED,
         ~summary.ALARM & summary.CONFIRMED],
        ["INSUFFICIENT weather data", "WEATHER ALARM, satellite data insufficient (cannot confirm)",
         "INSUFFICIENT satellite data",
         "DROUGHT: alarm confirmed by crops", "DROUGHT continuing: crops stressed, 90-day deficit persists",
         "WATCH: weather alarm, rainfed crops observed not below normal", "CROP STRESS without weather alarm"],
        "normal (observed)")
    risk_note = ("" if risk is not None else
                 f"\n\nAt-risk ranking skipped: {date.year} is inside the crop model's training years "
                 f"(2019-{FIRST_UNSEEN_YEAR - 1}), so its predictions would be in-sample.")
    lines = [f"# Drought system report - {date.date()}", "",
             "Stage 1 = weather module (SPEI now, forecast SPEI class). Stage 2 = satellite (latest SVI of "
             "the sampled rainfed fields, images at most 30 days old). Stage 3 = fields for the drone.", "",
             "## Status per site", "", to_md(summary, index=False), "",
             "## Stage 1: weather", "", to_md(wx.drop(columns=[c for c in wx if c.startswith("_")]), index=False), "",
             f"ALARM = SPEI-30 < {C.ALARM_SPEI} on the date, or the +{H}-day forecast class is Severe. "
             f"DROUGHT continuing = no alarm any more (SPEI-30 recovered) but crops still stressed and "
             f"SPEI-90 < {C.ALARM_SPEI}.", "",
             "## Stage 2: satellite", "", to_md(sat, index=False), "",
             f"CONFIRMED = median rainfed SVI < {C.STRESS_Z:g}, from at least {MIN_SAT_FIELDS} rainfed fields "
             f"with an image at most {C.MAX_INPUT_AGE} days old; fewer = INSUFFICIENT satellite data (never read "
             f"as 'not stressed'). Weather older than {MAX_DATA_AGE_DAYS} days or a forecast issued more than "
             f"{MAX_DATA_AGE_DAYS} days before the date is not used.", "",
             "## Stage 3: fields to fly", "",
             f"Rainfed fields only; up to {n_per_list} per site and list. Map: `fields_to_fly.kml` (Google Earth; "
             "red = stressed now, orange = at risk). Both are SHORTLISTS for a visit: 'stressed now' = SVI < -1 "
             "(below the field's normal, not measured damage); 'at risk' = normal now with a 15-day risk score "
             f">= {MIN_RISK_SCORE} (a ranking score, not a calibrated probability). For an unbiased check, also "
             "visit randomly chosen low-risk fields. Table: `fields_to_fly.csv` (incl. the dates and versions the "
             "selection used)." + risk_note, "",
             to_md(fly[cols], index=False), ""]
    (od / "SYSTEM_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(summary[["site", "status"]].to_string(index=False))
    print(f"Wrote {od / 'SYSTEM_REPORT.md'} and fields_to_fly.csv / .kml")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", action="store_true", help="train and save the crop model (once)")
    ap.add_argument("--date", nargs="*", help="dates YYYY-MM-DD (default: latest date with data)")
    ap.add_argument("--n", type=int, default=5, help="fields per site and list")
    a = ap.parse_args()
    if a.train:
        train()
    if a.date is not None or not a.train:
        for d in (a.date or [None]):
            run(pd.Timestamp(d) if d else None, a.n)


if __name__ == "__main__":
    main()
