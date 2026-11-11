"""
Step 1 of the satellite pipeline: Earth Engine exports -> clean 5-day series + SVI labels.

    python src/dataprep/build_dataset.py

Inputs  (data/gee_exports/): B_field_timeseries.csv, B_zone_timeseries.csv, B_zone_pixels.csv
Outputs (data/clean/):       fields_5day.csv  (240 sampled fields)
                             zones_5day.csv   (whole farmland area per site, rainfed / irrigated)
         results/qc/:        QC_REPORT.md, qc_observations.csv, qc_labels.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402
from dataprep.labels import svi, svi_class, vci  # noqa: E402
from dataprep.timeseries import days, make_grid, merge_same_day, spike_mask, to_grid  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
INDICES = ["NDVI", "NDMI", "EVI"]


def flag_spikes(obs: pd.DataFrame, id_col: str) -> pd.Series:
    """True = isolated NDVI spike. Two-sided (looks at the NEXT observation too), so it is used
    only for retrospective series (labels) and, cut at REF_CUTOFF, for the reference - never
    for model inputs."""
    out = pd.Series(False, index=obs.index)
    for _, g in obs.groupby(id_col, sort=False):
        g = g.sort_values("date")
        out.loc[g.index] = ~spike_mask(days(g["date"]), g["NDVI"].to_numpy(), C.SPIKE_NDVI, C.SPIKE_MAX_GAP)
    return out


def clean_observations(df: pd.DataFrame, id_col: str, clear_col: str, total_col: str,
                       min_clear: float, cols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clear-fraction filter, valid range, same-day merge (all backward-safe: each observation is
    judged on its own). Spikes are only FLAGGED (column `spike`), see flag_spikes. Returns (obs, qc)."""
    qc = df.groupby(id_col).size().rename("raw").to_frame()
    df = df.copy()
    df["clear_frac"] = (df[clear_col] / df[total_col]).clip(upper=1.0)
    df = df[df["clear_frac"] >= min_clear]
    qc["after_clear_filter"] = df.groupby(id_col).size()
    lo, hi = C.NDVI_VALID
    df = df[df["NDVI"].between(lo, hi)]
    df = merge_same_day(df, [id_col, "date"], cols + ["clear_frac"], clear_col)
    qc["after_same_day_merge"] = df.groupby(id_col).size()
    df = df.reset_index(drop=True)
    df["spike"] = flag_spikes(df, id_col)
    qc["after_spike_removal"] = df[~df["spike"]].groupby(id_col).size()
    gaps = df.sort_values("date").groupby(id_col)["date"].apply(lambda s: s.diff().dt.days.median())
    qc["median_gap_days"] = gaps
    return df, qc.fillna(0)


def to_5day(obs: pd.DataFrame, id_col: str, static: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    end = obs["date"].max()
    grid = make_grid(C.GRID_START, end, C.STEP_DAYS)
    gt = days(grid)
    rows = []
    cutoff = pd.Timestamp(C.REF_CUTOFF)
    for key, g in obs.groupby(id_col, sort=True):
        g = g.sort_values("date")
        clean = g[~g["spike"]]                                   # retrospective: labels only
        out = pd.DataFrame({id_col: key, "date": grid})
        for col in cols:
            # labels / targets: spike-free, interpolated (uses observations on both sides)
            v = clean[col].to_numpy(float)
            ok = np.isfinite(v)
            interp, _, _ = to_grid(days(clean["date"])[ok], v[ok], gt, C.MAX_GAP_DAYS)
            out[col] = interp
            # model inputs: every accepted observation up to the date (no look-ahead cleaning)
            v = g[col].to_numpy(float)
            ok = np.isfinite(v)
            _, causal, age = to_grid(days(g["date"])[ok], v[ok], gt, C.MAX_GAP_DAYS)
            out[col + "_c"] = causal
            if col == "NDVI":
                out["age_c"] = np.where(np.isfinite(causal), age, np.nan)
        # reference ("normal"): only observations up to REF_CUTOFF, spikes judged within that set
        r = g[g["date"] <= cutoff].copy()
        if len(r):
            r = r[~flag_spikes(r, id_col)]
        rv = r["NDVI"].to_numpy(float)
        ok = np.isfinite(rv)
        ref, _, _ = to_grid(days(r["date"])[ok], rv[ok], gt, C.MAX_GAP_DAYS) if ok.any()             else (np.full(len(gt), np.nan),) * 3
        ref = np.where(grid <= cutoff, ref, np.nan)
        out["SVI"], out["ref_mean"], out["ref_sigma"] = svi(grid, out["NDVI"].to_numpy(), ref)
        out["SVI_c"], _, _ = svi(grid, out["NDVI_c"].to_numpy(), ref)
        out["VCI"], _, _ = vci(grid, out["NDVI"].to_numpy(), ref)
        out["VCI_c"], _, _ = vci(grid, out["NDVI_c"].to_numpy(), ref)
        out["label"] = svi_class(out["SVI"].to_numpy())
        out["label_c"] = svi_class(out["SVI_c"].to_numpy())
        rows.append(out)
    res = pd.concat(rows, ignore_index=True).merge(static, on=id_col, how="left")
    res["year"] = res["date"].dt.year
    res["period"] = res["year"].map(C.period_of_year)
    return res


def label_table(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    lab = df.dropna(subset=["label"])
    t = lab.groupby(by)["label"].value_counts(normalize=True).unstack(fill_value=0) * 100
    t.columns = [C.CLASS_NAMES[int(c)] + " %" for c in t.columns]
    t["labelled steps"] = lab.groupby(by).size()
    return t.round(1)


def build_fields() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(C.FIELD_TS_FILE)
    raw = raw.rename(columns=lambda c: c[:-5] if c.endswith("_mean") else c)
    raw["date"] = pd.to_datetime(raw["date"])
    static = (raw.groupby("field_id")[["site", "site_code", "irrigated", "area_ha", "pixels"]]
              .first().reset_index().rename(columns={"irrigated": "irrigated_gee"}))
    static["weather"] = static["site_code"].map(lambda s: C.SITES[s]["weather"])   # config, not the export
    static["cluster"] = static["site_code"].map(lambda s: C.SITES[s]["cluster"])
    # Script B counts every pixel touching the polygon, script A only pixel centres, so a fully
    # clear image has ~1.14x 'pixels'. Use each field's clearest image as 100 % instead.
    raw["full_px"] = raw.groupby("field_id")["NDVI_count"].transform("max")
    obs, qc = clean_observations(raw, "field_id", "NDVI_count", "full_px", C.MIN_CLEAR_FRAC_FIELD, INDICES)
    static = static.merge(frozen_field_flags(obs), on="field_id", how="left")
    dropped = static[~static["crop_ok_ref"]]
    static = static[static["crop_ok_ref"]].drop(columns="crop_ok_ref")
    obs = obs[obs["field_id"].isin(static["field_id"])]
    grid = to_5day(obs, "field_id", static, INDICES)
    qc = qc.join(static.set_index("field_id")[["site_code", "irrigated", "irrigated_gee"]], how="inner")
    qc.attrs["dropped"] = dropped
    return grid, qc


def frozen_field_flags(obs: pd.DataFrame) -> pd.DataFrame:
    """Irrigation flag and crop check from TRAINING-period observations only (<= REF_CUTOFF),
    replacing Earth Engine's flags that used 2019-2025 imagery (same rules, field level):
      irrigated   = summer (Mar-May) NDVI p75 > 0.4 in >= 2 of the 5 training years
                    (Earth Engine: >= 3 of 7 years, pixel level)
      crop_ok_ref = a crop cycle (yearly NDVI p90 > 0.35 and p90 - p10 > 0.15) in >= 2 of 5 years"""
    o = obs[(obs["date"] <= pd.Timestamp(C.REF_CUTOFF)) & ~obs["spike"]].copy()
    o["y"] = o["date"].dt.year
    summer = o[o["date"].dt.month.isin([3, 4, 5])].groupby(["field_id", "y"])["NDVI"].quantile(0.75)
    yr = o.groupby(["field_id", "y"])["NDVI"].quantile([0.1, 0.9]).unstack()
    cyc = (yr[0.9] > 0.35) & (yr[0.9] - yr[0.1] > 0.15)
    out = pd.DataFrame({"irr_years": (summer > 0.4).groupby("field_id").sum(),
                        "crop_years": cyc.groupby("field_id").sum()}).fillna(0)
    out["irrigated"] = (out["irr_years"] >= 2).astype(int)
    out["crop_ok_ref"] = out["crop_years"] >= 2
    return out[["irrigated", "crop_ok_ref"]].reset_index()


def build_zones() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(C.ZONE_TS_FILE)
    raw["date"] = pd.to_datetime(raw["date"])
    raw[["NDVI", "NDMI"]] = raw[["NDVI", "NDMI"]].where(raw[["NDVI", "NDMI"]] > -9000)  # EE placeholder
    tot = pd.read_csv(C.ZONE_PIXELS_FILE)[["zone", "total_pixels"]]
    raw = raw.merge(tot, on="zone", how="left")
    raw["zone_id"] = [f"{C.SITE_ORDER[int(z) // 2]}_{'irrigated' if int(z) % 2 else 'rainfed'}"
                      for z in raw["zone"]]
    static = pd.DataFrame({"zone_id": sorted(raw["zone_id"].unique())})
    static["site_code"] = static["zone_id"].str.split("_").str[0]
    static["irrigated"] = static["zone_id"].str.endswith("irrigated").astype(int)
    static["weather"] = static["site_code"].map(lambda s: C.SITES[s]["weather"])
    static["cluster"] = static["site_code"].map(lambda s: C.SITES[s]["cluster"])
    obs, qc = clean_observations(raw, "zone_id", "clear_pixels", "total_pixels", C.MIN_CLEAR_FRAC_ZONE,
                                 ["NDVI", "NDMI"])
    grid = to_5day(obs, "zone_id", static, ["NDVI", "NDMI"])
    return grid, qc


def main():
    C.CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    qc_dir = C.RESULTS_DIR / "qc"
    qc_dir.mkdir(parents=True, exist_ok=True)

    fields, qc_f = build_fields()
    fields.to_csv(C.CLEAN_DIR / "fields_5day.csv", index=False)
    print(f"fields: {fields['field_id'].nunique()} fields, {len(fields)} rows")
    zones = pd.DataFrame()
    qc_z = pd.DataFrame()
    if C.ZONE_TS_FILE.exists():
        zones, qc_z = build_zones()
        zones.to_csv(C.CLEAN_DIR / "zones_5day.csv", index=False)
        print(f"zones: {zones['zone_id'].nunique()} zones, {len(zones)} rows")

    qc_site = qc_f.groupby(["site_code", "irrigated"]).agg(
        fields=("raw", "size"), raw_obs=("raw", "sum"), clear=("after_clear_filter", "sum"),
        merged=("after_same_day_merge", "sum"), final=("after_spike_removal", "sum"),
        median_gap_days=("median_gap_days", "median"))
    qc_site.to_csv(qc_dir / "qc_observations.csv")
    lab_site = label_table(fields, ["site_code", "irrigated"])
    lab_period = label_table(fields, ["period"])
    lab_year = label_table(fields[fields["irrigated"] == 0], ["year"])
    pd.concat({"by site": lab_site}).to_csv(qc_dir / "qc_labels.csv")

    lines = ["# Satellite data quality report", "",
             "Real Sentinel-2 SR (Cloud Score+ and SCL masked), 240 sampled farmland segments.",
             f"Observation kept if >= {C.MIN_CLEAR_FRAC_FIELD:.0%} of the field's pixels are clear; "
             f"same-day duplicates merged. Isolated NDVI spikes > {C.SPIKE_NDVI} are removed from the "
             "label series only (that check looks at the next image); model inputs use every accepted "
             f"image up to the date. Reference (normal) = observations up to {C.REF_CUTOFF} only.", "",
             "## Observations per site (irrigated 0 = rainfed)", "", to_md(qc_site), "",
             "## Crop-condition labels (SVI) by period", "",
             f"SVI = standardized NDVI anomaly; reference = training years {C.TRAIN_YEARS[0]}-"
             f"{C.TRAIN_YEARS[-1]} only, +-{C.VCI_DOY_WINDOW} days of the same day of year, "
             f"labelled year fully excluded. Classes (SPEI thresholds of the weather module): normal or above z >= "
             f"{C.SVI_MODERATE:g}, below normal {C.SVI_SEVERE:g} to {C.SVI_MODERATE:g}, strongly below normal < {C.SVI_SEVERE:g}. "
             "Steps without a normal crop signal are unlabelled.", "",
             to_md(lab_period), "",
             "## Labels by year (rainfed fields) — drought years should show more stress", "",
             to_md(lab_year), "",
             "## Labels by site", "", to_md(lab_site), ""]
    dropped = qc_f.attrs.get("dropped", pd.DataFrame())
    agree = pd.crosstab(qc_f["irrigated_gee"], qc_f["irrigated"], rownames=["Earth Engine flag (2019-25)"],
                        colnames=["frozen flag (2019-23)"])
    lines += ["## Frozen field flags (training years only)", "",
              "The Earth Engine irrigation flag and crop check used 2019-2025 imagery (incl. validation and "
              "test years). Both are recomputed per field from 2019-2023 observations only; the frozen "
              "irrigation flag is the one used everywhere (models, rainfed/irrigated results).", "",
              to_md(agree), "",
              f"Fields without a crop cycle in >= 2 of the 5 training years, dropped: {len(dropped)}"
              + (f" ({', '.join(dropped['field_id'])})" if len(dropped) else "") + ".", ""]
    if len(qc_z):
        lines += ["## Whole-area farmland zones", "", to_md(qc_z[["raw", "after_spike_removal",
                                                                 "median_gap_days"]]), ""]
    (qc_dir / "QC_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {qc_dir / 'QC_REPORT.md'}")


if __name__ == "__main__":
    main()
