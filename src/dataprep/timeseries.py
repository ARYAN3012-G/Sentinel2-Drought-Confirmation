"""
Cleaning helpers for irregular Sentinel-2 series.

Two regular 5-day versions of every series are produced:
  interp  : linear interpolation between the observations before and after a grid date
            (gap <= MAX_GAP_DAYS). Uses observations AFTER the date, so it is used only
            for LABELS (target) and descriptive analysis.
  causal  : last observation carried forward (age <= MAX_GAP_DAYS) — uses only
            observations on or before the grid date. Used for MODEL INPUTS.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def merge_same_day(df: pd.DataFrame, keys: list[str], value_cols: list[str],
                   weight_col: str) -> pd.DataFrame:
    """One field/zone seen on two overlapping image tiles on the same day -> one row.
    Values are averaged weighted by clear pixels; the clear-pixel count is the maximum
    (overlapping tiles see the same pixels, so a sum would double count)."""
    w = df[weight_col].astype(float).clip(lower=0)
    tmp = df[value_cols].astype(float).mul(w, axis=0)
    tmp["_w"] = w.where(df[value_cols].notna().all(axis=1), 0.0)
    tmp[keys] = df[keys]
    g = tmp.groupby(keys, sort=True)
    out = g[value_cols].sum().div(g["_w"].sum().replace(0, np.nan), axis=0)
    out[weight_col] = df.groupby(keys, sort=True)[weight_col].max()
    return out.reset_index()


def spike_mask(t_days: np.ndarray, x: np.ndarray, thr: float, max_gap: int) -> np.ndarray:
    """True = keep. An observation is a spike if it jumps by more than `thr` away from
    BOTH neighbours in the same direction, with both neighbours within `max_gap` days."""
    keep = np.ones(len(x), dtype=bool)
    for i in range(1, len(x) - 1):
        if t_days[i] - t_days[i - 1] > max_gap or t_days[i + 1] - t_days[i] > max_gap:
            continue
        d1, d2 = x[i] - x[i - 1], x[i] - x[i + 1]
        if d1 * d2 > 0 and min(abs(d1), abs(d2)) > thr:
            keep[i] = False
    return keep


def to_grid(obs_t: np.ndarray, obs_v: np.ndarray, grid_t: np.ndarray, max_gap: int):
    """obs_t / grid_t in integer days, obs_t sorted and unique.
    Returns (interp, causal, age): age = days since the last observation on/before the date."""
    n = len(grid_t)
    if len(obs_t) == 0:
        nan = np.full(n, np.nan)
        return nan, nan.copy(), nan.copy()
    idx = np.searchsorted(obs_t, grid_t, side="right")        # observations <= grid date
    has_prev = idx > 0
    has_next = idx < len(obs_t)
    prev_i = np.clip(idx - 1, 0, len(obs_t) - 1)
    next_i = np.clip(idx, 0, len(obs_t) - 1)
    prev_t = np.where(has_prev, obs_t[prev_i], np.nan)
    next_t = np.where(has_next, obs_t[next_i], np.nan)
    age = grid_t - prev_t

    causal = np.where(has_prev & (age <= max_gap), obs_v[prev_i], np.nan)

    interp = np.interp(grid_t, obs_t, obs_v)
    exact = has_prev & (age == 0)
    ok = exact | (has_prev & has_next & ((next_t - prev_t) <= max_gap))
    interp = np.where(ok, interp, np.nan)
    return interp, causal, age


def make_grid(start: str, end: pd.Timestamp, step: int) -> pd.DatetimeIndex:
    return pd.date_range(pd.Timestamp(start), end, freq=f"{step}D")


def days(d) -> np.ndarray:
    return (pd.to_datetime(d).values.astype("datetime64[D]").astype(np.int64))
