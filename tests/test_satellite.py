"""Integrity / leakage tests for the satellite pipeline (small hand-made arrays, no real data needed)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import config as C  # noqa: E402
from dataprep.labels import svi, svi_class, vci  # noqa: E402
from dataprep.timeseries import days, merge_same_day, spike_mask, to_grid  # noqa: E402


def test_causal_grid_never_uses_future_observations():
    obs_t, obs_v = np.array([0, 20]), np.array([0.2, 0.8])
    interp, causal, age = to_grid(obs_t, obs_v, np.array([0, 10, 20, 55]), max_gap=30)
    assert causal[1] == pytest.approx(0.2)          # carried forward, not 0.5
    assert interp[1] == pytest.approx(0.5)          # labels may interpolate
    assert age[1] == 10
    assert np.isnan(causal[3])                      # last image 35 days old > 30
    assert np.isnan(interp[3])


def test_interp_not_across_long_gaps():
    interp, _, _ = to_grid(np.array([0, 60]), np.array([0.2, 0.8]), np.array([30]), max_gap=30)
    assert np.isnan(interp[0])


def test_spike_removed_but_real_change_kept():
    t = np.arange(0, 50, 5)
    x = np.array([0.3, 0.3, 0.3, 0.9, 0.3, 0.3, 0.6, 0.6, 0.6, 0.6])  # spike at 3, step at 6
    keep = spike_mask(t, x, thr=0.15, max_gap=30)
    assert not keep[3]
    assert keep[[5, 6, 7]].all()


def test_same_day_merge_weighted_and_max_count():
    df = pd.DataFrame({"id": ["a", "a"], "date": ["2020-01-01"] * 2, "NDVI": [0.2, 0.6], "n": [10, 30]})
    out = merge_same_day(df, ["id", "date"], ["NDVI"], "n")
    assert out["NDVI"].iloc[0] == pytest.approx(0.5)
    assert out["n"].iloc[0] == 30


def _season(dates, amp):
    doy = dates.dayofyear.to_numpy()
    return 0.2 + amp * np.clip(np.sin(2 * np.pi * (doy - 180) / 365), 0, None)


def test_vci_reference_uses_only_training_years_and_never_own_year():
    dates = pd.date_range("2019-01-01", "2026-10-31", freq="5D")
    ndvi = _season(dates, 0.5)
    v1, mn1, mx1 = vci(dates, ndvi, ndvi)
    # change a TEST year: no training-year reference may change
    ndvi2 = ndvi.copy()
    ndvi2[dates.year == 2025] += 0.3
    v2, mn2, mx2 = vci(dates, ndvi2, ndvi2)
    train = np.isin(dates.year, C.TRAIN_YEARS)
    assert np.allclose(np.nan_to_num(mx1[train]), np.nan_to_num(mx2[train]))
    # change a TRAINING year: its own reference must not change
    ndvi3 = ndvi.copy()
    ndvi3[dates.year == 2021] *= 0.5
    _, mn3, mx3 = vci(dates, ndvi3, ndvi3)
    y21 = dates.year == 2021
    assert np.allclose(np.nan_to_num(mx1[y21]), np.nan_to_num(mx3[y21]))
    assert np.allclose(np.nan_to_num(mn1[y21]), np.nan_to_num(mn3[y21]))


def test_vci_unlabelled_without_crop_signal():
    dates = pd.date_range("2019-01-01", "2026-10-31", freq="5D")
    flat = np.full(len(dates), 0.2)                 # bare land: no crop cycle
    v, _, _ = vci(dates, flat, flat)
    assert np.isnan(v).all()


def test_svi_classes_match_spei_thresholds():
    c = svi_class(np.array([0.5, 0.0, -0.1, -1.5, -1.51, np.nan]))
    assert list(c[:5]) == [0, 0, 1, 1, 2] and np.isnan(c[5])


def test_svi_reference_excludes_test_years_and_own_year():
    dates = pd.date_range("2019-01-01", "2026-10-31", freq="5D")
    rng = np.random.default_rng(1)
    ndvi = _season(dates, 0.5) + rng.normal(0, 0.03, len(dates))
    z1, mu1, s1 = svi(dates, ndvi, ndvi)
    ndvi2 = ndvi.copy()
    ndvi2[dates.year >= 2024] -= 0.2                # change val/test years only
    z2, mu2, s2 = svi(dates, ndvi2, ndvi2)
    train = np.isin(dates.year, C.TRAIN_YEARS)
    assert np.allclose(np.nan_to_num(z1[train]), np.nan_to_num(z2[train]))
    assert np.allclose(np.nan_to_num(mu1[~train]), np.nan_to_num(mu2[~train]))
    # a normal year scores near 0 on average, a uniformly worse test year clearly negative
    assert abs(np.nanmean(z1[train])) < 0.5
    assert np.nanmean(z2[dates.year == 2025]) < -1


def test_weather_5day_uses_no_day_after_t():
    from dataprep.weather_link import to_5day
    d = pd.DataFrame({"valid_time": pd.date_range("2019-01-01", periods=40)})
    for col, _ in __import__("dataprep.weather_link", fromlist=["RAW"]).RAW.values():
        d[col] = np.arange(40, dtype=float)
    for k in C.SPEI_SCALES:
        d[f"SPEI{k}"] = 0.0
    grid = pd.DatetimeIndex(["2019-01-20"])
    a = to_5day(d, grid)
    d.loc[d["valid_time"] > "2019-01-20", d.columns[1:]] = 999.0
    b = to_5day(d, grid)
    pd.testing.assert_frame_equal(a, b)
    assert a["P"].iloc[0] == sum(range(15, 20))     # days 16-20 Jan = values 15..19


def test_sample_inputs_end_at_t_and_target_is_h_ahead(tmp_path, monkeypatch):
    from experiments import run_forecast as R
    dates = pd.date_range("2019-01-01", "2026-10-31", freq="5D")
    n = len(dates)
    rng = np.random.default_rng(0)
    f = pd.DataFrame({"field_id": "F1", "site_code": "Som", "cluster": "south", "irrigated": 0,
                      "weather": "Somandepalle", "date": dates,
                      "label": rng.integers(0, 3, n).astype(float),
                      "label_c": rng.integers(0, 3, n).astype(float), "age_c": 0.0})
    for c in C.SAT_FEATURES:
        if c != "age_c":
            f[c] = rng.random(n)
    w = pd.DataFrame({"weather": "Somandepalle", "date": dates})
    for c in C.WEATHER_FEATURES:
        w[c] = rng.random(n)
    fc = pd.concat([pd.DataFrame({"weather": "Somandepalle", "date": dates, "h": h,
                                  "p_healthy": rng.random(n), "p_moderate": rng.random(n),
                                  "p_severe": rng.random(n)}) for h in C.WEATHER_FC_HORIZONS])
    monkeypatch.setattr(C, "CLEAN_DIR", tmp_path)
    fc.to_csv(tmp_path / "weather_forecasts.csv", index=False)
    f.to_csv(tmp_path / "fields_5day.csv", index=False)
    w.to_csv(tmp_path / "weather_5day.csv", index=False)
    blocks, meta = R.build_samples(15)
    assert ((meta["target_date"] - meta["t"]).dt.days == 15).all()
    assert ((meta["t"] - meta["input_start"]).dt.days == (C.INPUT_STEPS - 1) * C.STEP_DAYS).all()
    # change everything after one sample's t: that sample's inputs must not change
    i = len(meta) // 2
    t = meta["t"].iloc[i]
    f2, w2 = f.copy(), w.copy()
    f2.loc[f2["date"] > t, [c for c in C.SAT_FEATURES if c != "age_c"]] = 5.0
    w2.loc[w2["date"] > t, C.WEATHER_FEATURES] = 5.0
    fc2 = fc.copy()
    fc2.loc[fc2["date"] > t, ["p_healthy", "p_moderate", "p_severe"]] = 5.0
    f2.to_csv(tmp_path / "fields_5day.csv", index=False)
    w2.to_csv(tmp_path / "weather_5day.csv", index=False)
    fc2.to_csv(tmp_path / "weather_forecasts.csv", index=False)
    blocks2, meta2 = R.build_samples(15)
    for b in ("sat", "weather", "wxfc", "static"):          # usable inputs: nothing after t
        assert np.allclose(blocks[b][i], blocks2[b][i])
    assert not np.allclose(blocks["future"][i], blocks2["future"][i])   # upper bound: uses (t, t+h]
    # the upper-bound block uses only days up to t+h: changing later weather leaves it unchanged
    w3 = w.copy()
    w3.loc[w3["date"] > meta["target_date"].iloc[i], C.WEATHER_FEATURES] = 7.0
    w3.to_csv(tmp_path / "weather_5day.csv", index=False)
    blocks3, _ = R.build_samples(15)
    assert np.allclose(blocks["future"][i], blocks3["future"][i])
    # target label equals the label on target_date
    lab = f.set_index("date")["label"]
    assert (meta["y"].to_numpy() == lab.reindex(meta["target_date"]).to_numpy()).all()


def test_purged_split_and_loco_masks():
    from experiments import run_forecast as R
    meta = pd.DataFrame({
        "cluster": ["south", "south", "kurnool", "kurnool", "south"],
        "period": ["train", "val", "test", "test", "test"],
        "input_period": ["train", "train", "test", "test", "test"],
        "support_period": ["train", "val", "test", "test", "test"]})
    mk = R.masks(meta, "temporal", None)
    assert list(mk["val"]) == [False, False, False, False, False]   # crosses periods -> dropped
    mk = R.masks(meta, "loco", "kurnool")
    assert list(mk["test"]) == [False, False, True, True, False]
    assert not (mk["train"] & (meta["cluster"] == "kurnool").to_numpy()).any()


def test_site_order_matches_earth_engine_zones():
    assert C.SITE_ORDER == ["Som", "Lep", "Cho", "Sira", "Ped", "Din", "Bal", "Pul"]
    assert C.SITES["Lep"]["weather"] == C.SITES["Cho"]["weather"]
    assert {C.SITES[s]["cluster"] for s in ("Din", "Bal", "Pul", "Ped")} == {"kurnool"}


def test_label_support_crossing_a_boundary_is_purged():
    from experiments import run_forecast as R
    meta = pd.DataFrame({"cluster": ["south"] * 2, "period": ["train", "train"],
                         "input_period": ["train", "train"], "support_period": ["train", "val"]})
    assert list(R.masks(meta, "temporal", None)["train"]) == [True, False]


def _synthetic_field(seed=0, extra=None):
    """Seasonal NDVI every ~6 days 2019-2026 with noise; extra = list of (date, ndvi) to append."""
    rng = np.random.default_rng(seed)
    d = pd.date_range("2019-01-03", "2026-10-30", freq="6D")
    doy = d.dayofyear.to_numpy()
    ndvi = 0.25 + 0.35 * np.exp(-((doy - 270) / 40.0) ** 2) + rng.normal(0, 0.02, len(d))
    obs = pd.DataFrame({"field_id": "F1", "date": d, "NDVI": ndvi, "NDMI": ndvi - 0.3, "EVI": ndvi * 0.8})
    if extra:
        obs = pd.concat([obs, pd.DataFrame([{"field_id": "F1", "date": pd.Timestamp(t), "NDVI": v,
                                             "NDMI": v - 0.3, "EVI": v * 0.8} for t, v in extra])])
    obs = obs.sort_values("date").reset_index(drop=True)
    return obs


def _grid(obs):
    from dataprep.build_dataset import flag_spikes, to_5day
    obs = obs.copy()
    obs["spike"] = flag_spikes(obs, "field_id")
    static = pd.DataFrame({"field_id": ["F1"], "irrigated": [0]})
    return to_5day(obs, "field_id", static, ["NDVI", "NDMI", "EVI"]).set_index("date")


def test_model_inputs_unchanged_by_later_images():
    """The last image before T jumps up (0.9). With data only up to T it cannot be judged a
    spike; once later images arrive, the two-sided spike rule removes it. Model inputs up to T
    must be identical in both cases (the old pipeline changed them: look-ahead)."""
    T = pd.Timestamp("2025-08-01")
    full = _synthetic_field()
    up_to_T = full[full["date"] <= T].copy()
    last = up_to_T.index[-1]
    up_to_T.loc[last, "NDVI"] = 0.9
    full.loc[last, "NDVI"] = 0.9
    g1, g2 = _grid(up_to_T), _grid(full)
    cols = ["NDVI_c", "SVI_c", "VCI_c", "age_c"]
    a, b = g1.loc[:T, cols], g2.loc[:T, cols]
    assert np.allclose(a.fillna(-99).to_numpy(), b.fillna(-99).to_numpy())
    d = g2.index[g2.index >= full.loc[last, "date"]][0]               # first grid date after that image
    assert g2.loc[d, "NDVI_c"] == pytest.approx(0.9)                  # the image is still a model input
    assert not np.isclose(g2.loc[d, "NDVI"], 0.9)                     # but not part of the label series


def test_reference_ignores_images_after_cutoff():
    base = _synthetic_field()
    changed = base.copy()
    m = changed["date"] > pd.Timestamp(C.REF_CUTOFF)
    changed.loc[m, "NDVI"] = changed.loc[m, "NDVI"] * 0.5            # only post-2023 images differ
    g1, g2 = _grid(base), _grid(changed)
    for c in ("ref_mean", "ref_sigma"):
        assert np.allclose(g1[c].fillna(-99).to_numpy(), g2[c].fillna(-99).to_numpy())


def test_svi_mean_and_spread_fully_exclude_the_scored_year():
    dates = pd.date_range("2019-01-01", "2023-12-31", freq="5D")
    doy = dates.dayofyear.to_numpy()
    rng = np.random.default_rng(1)
    ref = 0.3 + 0.3 * np.exp(-((doy - 270) / 40.0) ** 2) + rng.normal(0, 0.03, len(dates))
    _, mu1, s1 = svi(dates, ref, ref)
    ref2 = ref.copy()
    y21 = dates.year == 2021
    ref2[y21] = ref2[y21] + rng.normal(0, 0.2, y21.sum())             # change only year 2021
    _, mu2, s2 = svi(dates, ref2, ref2)
    assert np.allclose(np.nan_to_num(mu1[y21], nan=-9), np.nan_to_num(mu2[y21], nan=-9))
    assert np.allclose(np.nan_to_num(s1[y21], nan=-9), np.nan_to_num(s2[y21], nan=-9))


def test_weather_cells_contain_the_site_centres():
    """Each site uses the AgERA5 cell its centre lies in (Pullaiah -> Balaji Villas' cell)."""
    assert C.SITES["Pul"]["weather"] == C.SITES["Bal"]["weather"]
    assert C.SITES["Ped"]["weather"] == "Peddakadubur" and not C.WEATHER_EXTRA


def test_labels_exist_after_the_reference_cutoff():
    g = _grid(_synthetic_field())
    after = g.index > pd.Timestamp(C.REF_CUTOFF)
    assert g.loc[after, "SVI"].notna().sum() > 0 and g.loc[after, "label"].notna().sum() > 0
