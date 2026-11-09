"""
Crop-condition labels per field, computed without leakage. Reference = TRAINING years only,
and never the year being scored.

SVI (Standardized Vegetation Index, Peters et al. 2002) — the LABEL:
    z = (NDVI - mu) / sigma
    mu    = mean reference NDVI within +-VCI_DOY_WINDOW days of the same day of year
    sigma = spread of out-of-sample reference deviations within +-SVI_SIGMA_WINDOW days
Classes use the weather module's SPEI thresholds, so both modules share one scale:
    Healthy z >= 0 · Moderate -1.5 <= z < 0 · Severe z < -1.5

VCI (Kogan 1995) is kept as an extra input/report variable only: with 4-5 reference years its
min/max envelope puts ~20 % of all dates at VCI ~ 0 by chance, so it is not used as the label.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import config as C


def _setup(dates: pd.DatetimeIndex, ref_ndvi: np.ndarray, ref_years):
    years = np.asarray(dates.year)
    doy = np.asarray(dates.dayofyear)
    d = np.abs(doy[:, None] - doy[None, :])
    dist = np.minimum(d, 365 - d)
    usable = np.isin(years, ref_years) & np.isfinite(ref_ndvi)
    other_year = years[:, None] != years[None, :]
    return years, dist, usable, other_year


def envelope(dates, ref_ndvi, ref_years=None):
    """Reference min / max / mean / number of years within +-VCI_DOY_WINDOW days, own year excluded."""
    ref_years = C.TRAIN_YEARS if ref_years is None else ref_years
    years, dist, usable, other = _setup(dates, ref_ndvi, ref_years)
    m = (dist <= C.VCI_DOY_WINDOW) & usable[None, :] & other
    r = np.where(m, ref_ndvi[None, :], np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        mn, mx, mu = np.nanmin(r, 1), np.nanmax(r, 1), np.nanmean(r, 1)
    n_years = sum((m & (years == y)[None, :]).any(axis=1).astype(int) for y in ref_years)
    crop = (n_years >= C.VCI_MIN_REF_YEARS) & (mx - mn >= C.VCI_MIN_RANGE) & (mx >= C.VCI_MIN_PEAK)
    return mn, mx, mu, crop


def vci(dates, ndvi, ref_ndvi, ref_years=None):
    """Returns (vci 0-100 or NaN, reference min, reference max)."""
    mn, mx, _, crop = envelope(dates, ref_ndvi, ref_years)
    ok = crop & np.isfinite(ndvi)
    with np.errstate(invalid="ignore", divide="ignore"):
        v = np.clip(100.0 * (ndvi - mn) / (mx - mn), 0.0, 100.0)
    return np.where(ok, v, np.nan), mn, mx


def svi(dates, ndvi, ref_ndvi, ref_years=None):
    """Returns (z or NaN, mu, sigma)."""
    ref_years = C.TRAIN_YEARS if ref_years is None else ref_years
    _, _, mu, crop = envelope(dates, ref_ndvi, ref_years)
    years, dist, usable, other = _setup(dates, ref_ndvi, ref_years)
    resid = ref_ndvi - mu                                  # out-of-sample: mu excludes own year
    use = usable & crop & np.isfinite(resid)
    m = (dist <= C.SVI_SIGMA_WINDOW) & use[None, :] & other
    r = np.where(m, resid[None, :], np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        sigma = np.sqrt(np.nanmean(r ** 2, axis=1))         # spread around the reference mean
    n = m.sum(axis=1)
    ok = crop & np.isfinite(ndvi) & (n >= C.SVI_MIN_POINTS) & (sigma > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        z = np.clip((ndvi - mu) / sigma, -C.SVI_CLIP, C.SVI_CLIP)
    return np.where(ok, z, np.nan), mu, sigma


def svi_class(z: np.ndarray) -> np.ndarray:
    """0 Healthy (z >= 0), 1 Moderate (-1.5 <= z < 0), 2 Severe (z < -1.5), NaN where no label."""
    out = np.full(len(z), np.nan)
    f = np.isfinite(z)
    out[f] = np.where(z[f] < C.SVI_SEVERE, 2, np.where(z[f] < C.SVI_MODERATE, 1, 0))
    return out
