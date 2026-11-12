"""
Operational replay: run the integrated system every 5 days through each kharif season as if live,
with realistic data delays, and compare with the official drought declarations.

    python src/system/replay.py [--years 2023 2024 2025 2026]

On each issue date d (1 Jun - 30 Nov, every 5 days):
  weather  : AgERA5 is published ~WEATHER_DELAY_DAYS late -> SPEI-30/90 of day d - delay, and the
             weather module's +15-day forecast issued on that day (lead from d = 15 - delay days)
  satellite: Sentinel-2 images up to d - SAT_DELAY_DAYS (median SVI of the rainfed sampled fields,
             images at most 30 days old, at least MIN_SAT_FIELDS fields)
  status   : same rules as run_system.py (alarm / confirmed / continuing / insufficient data)
No crop model is used, so every year 2023-2026 is out-of-sample for the system (the weather model
is trained on 1979-2011; SVI normals exclude the scored year).

Per site and season: first alarm date, first confirmation date, and the official declaration
(data/official/drought_declarations.csv; AP G.O. dates). A declared mandal should be alarmed and
confirmed, ideally BEFORE the G.O.; a non-declared one should not be confirmed.
Outputs: results/replay/{replay_daily.csv, replay_seasons.csv, REPLAY_REPORT.md}
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

to_md = C.weather_module("utils/report.py").to_md
OUT = C.RESULTS_DIR / "replay"
WEATHER_DELAY_DAYS = 7      # AgERA5 publication delay (about one week)
SAT_DELAY_DAYS = 2          # Sentinel-2 L2A availability
MIN_SAT_FIELDS = 5
H = 15
GO_DATES = {2023: "2023-10-31", 2024: "2024-10-29", 2025: "2025-10-31", 2026: "2026-10-01"}


def level(status: str) -> int:
    """Declared level: 0 none, 1 moderate, 2 severe; NaN unknown / ambiguous."""
    s = str(status).lower()
    if "unknown" in s or "/" in s:
        return np.nan
    return 2 if s.startswith("severe") else 1 if s.startswith("moderate") else 0 if "not declared" in s else np.nan


def daily(years) -> pd.DataFrame:
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    w = pd.read_csv(C.CLEAN_DIR / "weather_5day.csv", parse_dates=["date"])
    fc = pd.read_csv(C.CLEAN_DIR / "weather_forecasts.csv", parse_dates=["date"])
    fc = fc[fc.h == H]
    rain = f[(f.irrigated == 0) & f.SVI_c.notna() & (f.age_c <= C.MAX_INPUT_AGE)]
    rows = []
    for y in years:
        for d in pd.date_range(f"{y}-06-01", f"{y}-11-30", freq="5D"):
            dw, ds = d - pd.Timedelta(days=WEATHER_DELAY_DAYS), d - pd.Timedelta(days=SAT_DELAY_DAYS)
            for code in C.SITE_ORDER:
                wx = C.SITES[code]["weather"]
                ww = w[(w.weather == wx) & (w.date <= dw)].tail(1)
                ff = fc[(fc.weather == wx) & (fc.date <= dw) & (fc.date > dw - pd.Timedelta(days=5))].tail(1)
                last = rain[(rain.site_code == code) & (rain.date <= ds)]
                last = last[last.date == last.date.max()] if len(last) else last
                last = last[(ds - last.date).dt.days <= C.STEP_DAYS]
                if not len(ww):
                    continue
                spei30, spei90 = float(ww.SPEI30.iloc[0]), float(ww.SPEI90.iloc[0])
                severe_fc = bool(len(ff) and ff[["p_healthy", "p_moderate", "p_severe"]].to_numpy()[0].argmax() == 2)
                alarm = spei30 < C.ALARM_SPEI or severe_fc
                ok = len(last) >= MIN_SAT_FIELDS
                med = float(last.SVI_c.median()) if len(last) else np.nan
                conf = ok and med < C.STRESS_Z
                status = ("insufficient satellite data" if not ok else
                          "drought" if alarm and conf else
                          "drought continuing" if conf and spei90 < C.ALARM_SPEI else
                          "watch" if alarm else "crop stress, no alarm" if conf else "normal")
                rows.append(dict(year=y, issue_date=d.date(), site=code, SPEI30=round(spei30, 2),
                                 SPEI90=round(spei90, 2), severe_forecast=severe_fc, alarm=alarm,
                                 rainfed_fields=len(last), median_SVI=round(med, 2) if ok else np.nan,
                                 confirmed=conf, status=status))
    return pd.DataFrame(rows)


def seasons(dd: pd.DataFrame) -> pd.DataFrame:
    gov = pd.read_csv(C.ROOT / "data" / "official" / "drought_declarations.csv")
    out = []
    for (y, s), g in dd.groupby(["year", "site"]):
        g = g.sort_values("issue_date")
        a = g[g.alarm].issue_date
        c = g[g.status.isin(["drought", "drought continuing"])].issue_date
        go = pd.Timestamp(GO_DATES[y]).date()
        dec = gov[(gov.site_code == s) & (gov.year == y)]
        st = dec.status.iloc[0] if len(dec) else "unknown"
        out.append(dict(year=y, site=s, official=st, official_level=level(st), GO_date=go,
                        first_alarm=a.min() if len(a) else None, first_confirmed=c.min() if len(c) else None,
                        confirmed_dates=int(len(c)), dates_with_satellite=int((g.status != "insufficient satellite data").sum()),
                        confirmed_before_GO=bool(len(c) and c.min() <= go),
                        lead_days_before_GO=int((go - c.min()).days) if len(c) and c.min() <= go else np.nan))
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs="+", type=int, default=[2023, 2024, 2025, 2026])
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    dd = daily(a.years)
    dd.to_csv(OUT / "replay_daily.csv", index=False)
    ss = seasons(dd)
    ss.to_csv(OUT / "replay_seasons.csv", index=False)
    known = ss[ss.official_level.notna()]
    tab = pd.crosstab(known.official_level.map({0: "not declared", 1: "moderate", 2: "severe"}),
                      known.confirmed_dates > 0, rownames=["official"], colnames=["system confirmed drought"])
    decl = known[known.official_level > 0]
    lines = ["# Operational replay of the integrated system, kharif 2023-2026", "",
             f"Every 5 days, 1 Jun - 30 Nov, with weather {WEATHER_DELAY_DAYS} days late (AgERA5) and "
             f"satellite {SAT_DELAY_DAYS} days late; alarm = SPEI-30 < {C.ALARM_SPEI} or a Severe +{H}-day "
             f"forecast; confirmed = median rainfed SVI < {C.STRESS_Z:g} from >= {MIN_SAT_FIELDS} fields. No "
             "crop model is used, so all years are out-of-sample. Official = AP G.O. drought mandal lists "
             "(Sira/Karnataka and the Adoni-Peddakadubur border site are excluded where unknown or ambiguous).", "",
             "## Season summary per site", "", to_md(ss, index=False), "",
             "## Agreement with official declarations (site-seasons with a known declaration)", "",
             to_md(tab), "",
             f"Declared site-seasons confirmed by the system before the G.O. date: "
             f"{int(decl.confirmed_before_GO.sum())} of {len(decl)}; median lead "
             f"{decl.lead_days_before_GO.median():.0f} days.", "",
             "Small sample (one area per mandal, 4 seasons): read as case evidence, not a statistical test.", ""]
    (OUT / "REPLAY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(to_md(tab))
    print(ss[["year", "site", "official", "first_alarm", "first_confirmed", "lead_days_before_GO"]].to_string(index=False))


if __name__ == "__main__":
    main()
