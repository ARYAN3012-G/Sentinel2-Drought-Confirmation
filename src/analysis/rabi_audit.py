"""
Rabi field audit (descriptive, no comparison with declarations): do the existing sampled fields
contain rabi farming, and when does their greenness peak?

For every field and season (Oct y - Apr y+1) on the 5-day interpolated NDVI:
  peak month   = month of the highest NDVI in Oct-Apr
  rabi peak    = the highest NDVI falls in January-March and exceeds 0.35
                 (a crop green after the kharif harvest; it may have been sown in Oct-Nov)
  late kharif  = the highest NDVI falls in October-November and exceeds 0.35, then declines
Historically rabi-active field = rabi peak in >= 2 of the 4 reference seasons 2019-20 .. 2022-23.

    python src/analysis/rabi_audit.py
Output: results/rabi/{rabi_audit_fields.csv, rabi_audit_monthly.csv, RABI_AUDIT.md}
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "rabi"
REF = [2019, 2020, 2021, 2022]
SEASONS = REF + [2023, 2024, 2025]
GREEN = 0.35
MONTHS = [10, 11, 12, 1, 2, 3, 4]
NAMES = {10: "Oct", 11: "Nov", 12: "Dec", 1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"],
                    usecols=["field_id", "site_code", "irrigated", "date", "NDVI"])
    rows, monthly = [], []
    for y in SEASONS:
        s = f[f.date.between(pd.Timestamp(f"{y}-10-01"), pd.Timestamp(f"{y + 1}-04-30")) & f.NDVI.notna()].copy()
        s["month"] = s.date.dt.month
        top = s.loc[s.groupby("field_id").NDVI.idxmax()]
        for r in top.itertuples():
            kind = ("rabi peak" if r.month in (1, 2, 3) and r.NDVI > GREEN else
                    "late kharif" if r.month in (10, 11) and r.NDVI > GREEN else
                    "December peak" if r.month == 12 and r.NDVI > GREEN else "never green")
            rows.append(dict(season=y, field_id=r.field_id, site=r.site_code, irrigated=r.irrigated,
                             peak_month=NAMES[r.month], peak_ndvi=round(r.NDVI, 3), pattern=kind))
        m = s.groupby(["site_code", "irrigated", "month"]).NDVI.median().reset_index()
        monthly.append(m.assign(season=f"{y}-{str(y + 1)[2:]}"))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "rabi_audit_fields.csv", index=False)
    mm = pd.concat(monthly)
    mm.to_csv(OUT / "rabi_audit_monthly.csv", index=False)

    ref = t[t.season.isin(REF)]
    hist = (ref.assign(rp=ref.pattern == "rabi peak").groupby(["field_id", "site", "irrigated"]).rp.sum()
            .reset_index())
    hist["rabi_active"] = hist.rp >= 2
    cls = {0: "rainfed", 1: "irrigated"}
    tab = (hist.assign(cls=hist.irrigated.map(cls)).groupby(["site", "cls"])
           .agg(fields=("field_id", "size"), historically_rabi_active=("rabi_active", "sum")).unstack("cls"))
    tab.columns = [f"{b} {a.replace('_', ' ')}" for a, b in tab.columns]
    pat = (ref.assign(cls=ref.irrigated.map(cls)).groupby(["cls", "pattern"]).size()
           .unstack("pattern").fillna(0).astype(int))
    pat = (100 * pat.div(pat.sum(axis=1), axis=0)).round().astype(int).astype(str) + " %"
    prof = (mm[mm.season.isin([f"{y}-{str(y + 1)[2:]}" for y in REF])]
            .groupby(["irrigated", "month"]).NDVI.median().unstack("month")[MONTHS].round(2))
    prof.index = prof.index.map(cls)
    prof.columns = [NAMES[c] for c in prof.columns]
    lines = ["# Rabi field audit (descriptive)", "",
             "Do the existing 240 sampled fields contain rabi farming? Script A selected fields with a crop cycle in "
             "the CALENDAR year (not kharif crops specifically), so they may include rabi fields. Per field and season "
             f"(Oct - Apr), the month of highest NDVI: **rabi peak** = highest in Jan-Mar and > {GREEN} (a crop green "
             "after the kharif harvest; it may have been sown in Oct-Nov); **late kharif** = highest in Oct-Nov; "
             f"**December peak**; **never green** (never above {GREEN}). Historically rabi-active = rabi peak in >= 2 "
             "of the reference seasons 2019-20 .. 2022-23. No comparison with drought declarations is made here.", "",
             "## Median NDVI by month, reference seasons 2019-20 .. 2022-23", "", to_md(prof), "",
             "## Share of field-seasons by pattern (reference seasons)", "", to_md(pat), "",
             "## Historically rabi-active fields per site", "", to_md(tab.fillna(0).astype(int)), ""]
    (OUT / "RABI_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    print(prof.to_string(), "\n")
    print(pat.to_string(), "\n")
    print(tab.fillna(0).astype(int).to_string())


if __name__ == "__main__":
    main()
