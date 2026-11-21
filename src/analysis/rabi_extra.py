"""
EXPLORATORY rabi indicators (added after the main analysis showed that rainfed greenness hardly
responds in rabi). Rules fixed before looking at the outcome against the declarations:

  A  Rabi sowing: a field is SOWN in rabi y (1 Dec y - 31 Mar y+1) if its NDVI shows a crop cycle
     in that window: 90th percentile > 0.35 and 90th - 10th percentile > 0.15 (the crop-cycle rule
     of Earth Engine script A). Site sown share vs its normal = mean share in rabi 2019-20 ... 2022-23
     (training years). FLAG: sown share < 75 % of normal.
  B  Irrigated fields: mean Dec-Feb SVI per irrigated field (the fields actually cropped in rabi).
     FLAG: site median < -1 (the confirmation threshold used everywhere).

    python src/analysis/rabi_extra.py
Output: results/events/{rabi_extra.csv, RABI_EXTRA_REPORT.md}
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "events"
NORMAL = [2019, 2020, 2021, 2022]          # rabi 2019-20 ... 2022-23 (training years)
EVAL = [2023, 2024, 2025]                  # rabi 2023-24, 2024-25, 2025-26 (declarations available)
SOWN_P90, SOWN_RANGE, SOWING_FLAG, IRR_FLAG = 0.35, 0.15, 0.75, C.STRESS_Z


def window(y):
    return pd.Timestamp(f"{y}-12-01"), pd.Timestamp(f"{y + 1}-03-31")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    gov = pd.read_csv(C.ROOT / "data" / "official" / "drought_declarations.csv")
    gov = gov[gov.season == "rabi"]
    sites = pd.read_csv(C.SITES_TABLE).set_index("site_code")
    rows = []
    for y in NORMAL + EVAL:
        lo, hi = window(y)
        s = f[f.date.between(lo, hi) & f.NDVI.notna()]
        q = s.groupby("field_id").NDVI.quantile([0.1, 0.9]).unstack()
        sown = ((q[0.9] > SOWN_P90) & (q[0.9] - q[0.1] > SOWN_RANGE)).rename("sown")
        core = f[f.date.between(lo, pd.Timestamp(f"{y + 1}-02-28")) & (f.irrigated == 1)]
        irr = core.groupby("field_id").SVI.mean().rename("irr_svi")
        meta = f.groupby("field_id")[["site_code", "irrigated"]].first()
        t = meta.join(sown).join(irr)
        for code, g in t.groupby("site_code"):
            rows.append(dict(rabi=y, site=code, sown_share=g.sown.mean(),
                             sown_share_rainfed=g[g.irrigated == 0].sown.mean(),
                             irr_svi_median=g[g.irrigated == 1].irr_svi.median(),
                             irr_fields_below_normal=(g[g.irrigated == 1].irr_svi < -1).mean(),
                             irr_fields=int(g[g.irrigated == 1].irr_svi.notna().sum())))
    d = pd.DataFrame(rows)
    normal = d[d.rabi.isin(NORMAL)].groupby("site").sown_share.mean().rename("sown_share_normal")
    e = d[d.rabi.isin(EVAL)].join(normal, on="site")
    e["sown_pct_of_normal"] = (100 * e.sown_share / e.sown_share_normal).round()
    e["A_sowing_flag"] = e.sown_share < SOWING_FLAG * e.sown_share_normal
    e["B_irrigated_flag"] = e.irr_svi_median < IRR_FLAG
    e = e.merge(gov[["site_code", "year", "status"]].rename(columns={"site_code": "site", "year": "rabi",
                                                                      "status": "official"}),
                on=["site", "rabi"], how="left")
    e["mandal"] = e.site.map(sites["mandal"])
    e["rabi_label"] = e.rabi.astype(str) + "-" + (e.rabi + 1).astype(str).str[2:]
    e.to_csv(OUT / "rabi_extra.csv", index=False)

    # each official decision once (mandal x rabi); ambiguous / unknown excluded
    def lev(s):
        s = str(s).lower()
        return np.nan if ("unknown" in s or "/" in s or s == "nan") else 2 if s.startswith("severe") else \
            1 if s.startswith("moderate") else 0
    e["level"] = e.official.map(lev)
    m = (e[e.level.notna()].groupby(["rabi_label", "mandal"])
         .agg(official=("official", "first"), level=("level", "first"), sites=("site", ", ".join),
              sown_pct_of_normal=("sown_pct_of_normal", "min"), A=("A_sowing_flag", "any"),
              irr_svi_median=("irr_svi_median", "min"), B=("B_irrigated_flag", "any")).reset_index())
    summ = []
    for name, col in (("A sowing (< 75 % of normal)", "A"), ("B irrigated SVI (< -1)", "B"),
                      ("A or B", None)):
        flag = (m.A | m.B) if col is None else m[col]
        sev, nd = m.level == 2, m.level == 0
        summ.append({"indicator": name, "severe declared: flagged": f"{int(flag[sev].sum())}/{int(sev.sum())}",
                     "not declared: flagged (false alarm)": f"{int(flag[nd].sum())}/{int(nd.sum())}"})
    summ = pd.DataFrame(summ)
    cols = ["rabi_label", "site", "mandal", "official", "sown_pct_of_normal", "A_sowing_flag",
            "irr_svi_median", "irr_fields_below_normal", "B_irrigated_flag", "irr_fields"]
    lines = ["# Exploratory rabi indicators", "",
             "**Exploratory.** Added after the main analysis showed that the greenness of rainfed kharif fields "
             "hardly responds in rabi. Rules fixed before comparing with the declarations (see the script header): "
             f"A = a rabi crop cycle is found in < {SOWING_FLAG:.0%} of the site's normal share of fields "
             f"(normal = rabi 2019-20 to 2022-23); B = median Dec-Feb SVI of the irrigated fields < {IRR_FLAG:g}. "
             "Few cases: read as indication, not proof. Caveat: the Dec-Mar window also catches late kharif crops "
             "(e.g. cotton still green in December), so the sown share mixes late kharif and true rabi crops.", "",
             "## Each official decision once (mandal x rabi season)", "", to_md(summ, index=False), "",
             to_md(m.drop(columns=["level"]).round(2), index=False), "",
             "## Per site", "", to_md(e[cols].round(2), index=False), ""]
    (OUT / "RABI_EXTRA_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(summ.to_string(index=False))
    print(m.drop(columns=["level"]).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
