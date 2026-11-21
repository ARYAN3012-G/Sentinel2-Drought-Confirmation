"""
Operational replay: run the integrated system every 5 days through each KHARIF and RABI season as
if live, with realistic data delays, and compare with the official drought declarations.

    python src/system/replay.py

Seasons (as in the Andhra Pradesh drought orders):
  kharif <y>      = South-West monsoon, issue dates 1 Jun - 30 Nov of year y
  rabi <y>-<y+1>  = North-East monsoon / rabi, issue dates 1 Dec of y - 31 Mar of y+1
Every season ends earlier if the data end (2026 kharif: partial).

On each issue date d (every 5 days):
  weather  : AgERA5 arrives ~WEATHER_DELAY_DAYS late -> SPEI-30/90 of day d - delay (not older than
             5 days) and the weather module's +15-day forecast issued that day
  satellite: Sentinel-2 images up to d - SAT_DELAY_DAYS (median SVI of the rainfed sampled fields,
             each field's latest image at most 30 days old ON THE ISSUE DATE, >= MIN_SAT_FIELDS fields)
  evidence : the dates of the weather and satellite data behind each status are saved. A confirmation
             is IN-SEASON if every image used was taken inside the evaluated season, otherwise it rests
             (partly) on images from before the season (CARRY-OVER of earlier stress). Both are reported.
  status   : same rules as run_system.py (alarm / confirmed / continuing / insufficient data)
No crop model is used. Seasons whose months overlap the field-selection period 2019-2023 (kharif
2023, rabi 2023-24) are RETROSPECTIVE; later seasons are PROSPECTIVE.
Thresholds (SPEI < -1, SVI < -1, >= 5 fields) and delays were fixed before this replay was written.
Outputs: results/replay/{replay_daily.csv, replay_seasons.csv, replay_mandal_seasons.csv, REPLAY_REPORT.md}
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
# default order dates (AP G.O.s); per-site dates in drought_declarations.csv take precedence
GO_DATES = {("kharif", 2023): "2023-10-31", ("kharif", 2024): "2024-10-29", ("kharif", 2025): "2025-10-31",
            ("kharif", 2026): "2026-10-01", ("rabi", 2023): "2024-03-16", ("rabi", 2024): "2025-03-31",
            ("rabi", 2025): "2026-03-31"}
SEASONS = [("kharif", 2023), ("rabi", 2023), ("kharif", 2024), ("rabi", 2024), ("kharif", 2025),
           ("rabi", 2025), ("kharif", 2026)]


def label(kind: str, y: int) -> str:
    return f"kharif {y}" if kind == "kharif" else f"rabi {y}-{str(y + 1)[2:]}"


def window(kind: str, y: int) -> tuple[pd.Timestamp, pd.Timestamp]:
    return ((pd.Timestamp(f"{y}-06-01"), pd.Timestamp(f"{y}-11-30")) if kind == "kharif"
            else (pd.Timestamp(f"{y}-12-01"), pd.Timestamp(f"{y + 1}-03-31")))


def level(status: str) -> float:
    """Declared level: 0 none, 1 moderate, 2 severe; NaN unknown / ambiguous."""
    s = str(status).lower()
    if "unknown" in s or "/" in s:
        return np.nan
    return 2 if s.startswith("severe") else 1 if s.startswith("moderate") else 0 if "not declared" in s else np.nan


def data_end(w: pd.DataFrame, f: pd.DataFrame) -> pd.Timestamp:
    """Last issue date the data allow (weather and satellite publication delays)."""
    return min(w["date"].max() + pd.Timedelta(days=WEATHER_DELAY_DAYS),
               f.loc[f.SVI_c.notna(), "date"].max() + pd.Timedelta(days=SAT_DELAY_DAYS))


def daily(seasons, stress_z: float = C.STRESS_Z) -> pd.DataFrame:
    f = pd.read_csv(C.CLEAN_DIR / "fields_5day.csv", parse_dates=["date"])
    w = pd.read_csv(C.CLEAN_DIR / "weather_5day.csv", parse_dates=["date"])
    fc = pd.read_csv(C.CLEAN_DIR / "weather_forecasts.csv", parse_dates=["date"])
    fc = fc[fc.h == H]
    rain = f[(f.irrigated == 0) & f.SVI_c.notna()].copy()
    rain["image_date"] = rain.date - pd.to_timedelta(rain.age_c, unit="D")
    last = data_end(w, f)
    rows = []
    for kind, y in seasons:
        start, end = window(kind, y)
        end = min(end, last)
        if end < start:
            continue
        for d in pd.date_range(start, end, freq="5D"):
            dw, ds = d - pd.Timedelta(days=WEATHER_DELAY_DAYS), d - pd.Timedelta(days=SAT_DELAY_DAYS)
            for code in C.SITE_ORDER:
                wx = C.SITES[code]["weather"]
                ww = w[(w.weather == wx) & (w.date <= dw)].tail(1)
                if not len(ww) or (dw - ww.date.iloc[0]).days > C.STEP_DAYS:      # no stale weather
                    continue
                ff = fc[(fc.weather == wx) & (fc.date <= dw) & (fc.date > dw - pd.Timedelta(days=5))].tail(1)
                sat = rain[(rain.site_code == code) & (rain.date <= ds)]
                sat = sat[sat.date == sat.date.max()] if len(sat) else sat
                sat = sat[((ds - sat.date).dt.days <= C.STEP_DAYS)
                          & ((d - sat.image_date).dt.days <= C.MAX_INPUT_AGE)]     # age on the issue date
                spei30, spei90 = float(ww.SPEI30.iloc[0]), float(ww.SPEI90.iloc[0])
                severe_fc = bool(len(ff) and ff[["p_healthy", "p_moderate", "p_severe"]].to_numpy()[0].argmax() == 2)
                alarm = spei30 < C.ALARM_SPEI or severe_fc
                ok = len(sat) >= MIN_SAT_FIELDS
                med = float(sat.SVI_c.median()) if len(sat) else np.nan
                conf = ok and med < stress_z
                img0 = sat.image_date.min() if len(sat) else pd.NaT
                img1 = sat.image_date.max() if len(sat) else pd.NaT
                status = ("insufficient satellite data" if not ok else
                          "drought" if alarm and conf else
                          "drought continuing" if conf and spei90 < C.ALARM_SPEI else
                          "watch" if alarm else "crop stress, no alarm" if conf else "normal")
                trig = [t for t, on in (("SPEI-30", spei30 < C.ALARM_SPEI), ("forecast", severe_fc)) if on]
                if not alarm and conf and spei90 < C.ALARM_SPEI:
                    trig = ["SPEI-90 (continuing)"]
                rows.append(dict(kind=kind, year=y, season=label(kind, y), issue_date=d.date(), site=code,
                                 weather_date=ww.date.iloc[0].date(), SPEI30=round(spei30, 2),
                                 SPEI90=round(spei90, 2), severe_forecast=severe_fc, alarm=alarm,
                                 trigger="+".join(trig), rainfed_fields=len(sat),
                                 median_SVI=round(med, 2) if ok else np.nan,
                                 images_from=img0.date() if len(sat) else None,
                                 images_to=img1.date() if len(sat) else None,
                                 max_image_age_at_issue=int((d - img0).days) if len(sat) else np.nan,
                                 images_in_season=bool(len(sat) and img0 >= start),
                                 confirmed=conf, status=status))
    return pd.DataFrame(rows)


def seasons_table(dd: pd.DataFrame) -> pd.DataFrame:
    gov = pd.read_csv(C.ROOT / "data" / "official" / "drought_declarations.csv")
    if "season" not in gov:
        gov["season"] = "kharif"
    sites = pd.read_csv(C.SITES_TABLE).set_index("site_code")
    out = []
    for (kind, y, s), g in dd.groupby(["kind", "year", "site"]):
        g = g.sort_values("issue_date")
        a = g[g.alarm].issue_date
        cg = g[g.status.isin(["drought", "drought continuing"])]
        c = cg.issue_date
        ci = cg[cg.images_in_season].issue_date                 # confirmed on in-season images only
        dec = gov[(gov.site_code == s) & (gov.year == y) & (gov.season == kind)]
        od = dec.order_date.iloc[0] if len(dec) and isinstance(dec.order_date.iloc[0], str) else ""
        go = pd.Timestamp(od if od else GO_DATES[(kind, y)]).date()
        st = dec.status.iloc[0] if len(dec) else "unknown"
        _, end = window(kind, y)
        retro = y <= max(C.TRAIN_YEARS)          # kharif 2023 and rabi 2023-24
        out.append(dict(season=label(kind, y), kind=kind, year=y, site=s, mandal=sites.loc[s, "mandal"],
                        weather_cell=sites.loc[s, "agera5_cell"],
                        design="retrospective" if retro else "prospective",
                        season_end=max(g.issue_date),
                        partial_season=max(g.issue_date) < (end - pd.Timedelta(days=4)).date(),
                        official=st, official_level=level(st), GO_date=go,
                        first_alarm=a.min() if len(a) else None, first_confirmed=c.min() if len(c) else None,
                        first_confirmed_status=cg.status.iloc[0] if len(c) else None,
                        first_confirmed_images=(f"{cg.images_from.iloc[0]} .. {cg.images_to.iloc[0]}"
                                                if len(c) else None),
                        first_confirmed_in_season=ci.min() if len(ci) else None,
                        confirmed_dates=int(len(c)), confirmed_dates_in_season=int(len(ci)),
                        dates_with_satellite=int((g.status != "insufficient satellite data").sum()),
                        site_dates=int(len(g)),
                        confirmed_before_GO=bool(len(c) and c.min() <= go),
                        lead_days_before_GO=int((go - c.min()).days) if len(c) and c.min() <= go else np.nan))
    return pd.DataFrame(out)


def counts(k: pd.DataFrame) -> dict:
    """Eventual detection and advance warning, separately, per declared level."""
    out = {}
    for lev, name in ((2, "severe"), (1, "moderate")):
        g = k[k.official_level == lev]
        out[f"{name}: confirmed (eventually)"] = f"{int((g.confirmed_dates > 0).sum())}/{len(g)}"
        out[f"{name}: before order"] = f"{int(g.confirmed_before_GO.sum())}/{len(g)}"
        out[f"{name}: confirmed on in-season images"] = f"{int((g.confirmed_dates_in_season > 0).sum())}/{len(g)}"
    g = k[k.official_level == 0]
    out["not declared: confirmed (false alarm)"] = f"{int((g.confirmed_dates > 0).sum())}/{len(g)}"
    return out


def mandal_seasons(known: pd.DataFrame) -> pd.DataFrame:
    """Each official decision once: sites in one mandal pooled (confirmed if any site is)."""
    rows = []
    for (season, m), g in known.groupby(["season", "mandal"], sort=False):
        if g.official_level.nunique() != 1:
            continue
        conf = g[g.confirmed_dates > 0]
        first = min(conf.first_confirmed) if len(conf) else None
        fi = g.first_confirmed_in_season.dropna()
        fs = conf.loc[conf.first_confirmed == first].iloc[0] if len(conf) else None
        go = g.GO_date.iloc[0]
        rows.append(dict(season=season, kind=g.kind.iloc[0], design=g.design.iloc[0], mandal=m,
                         sites=", ".join(g.site), official=g.official.iloc[0],
                         official_level=g.official_level.iloc[0], order_date=go, system_first_confirmed=first,
                         first_status=fs.first_confirmed_status if fs is not None else None,
                         first_images=fs.first_confirmed_images if fs is not None else None,
                         first_confirmed_in_season=min(fi) if len(fi) else None,
                         confirmed_dates=int(first is not None), confirmed_dates_in_season=int(len(fi) > 0),
                         confirmed_before_GO=bool(first is not None and first <= go),
                         partial_season=bool(g.partial_season.any())))
    return pd.DataFrame(rows)


def by_group(df: pd.DataFrame, unit: str) -> pd.DataFrame:
    rows = []
    for name, k in (("kharif, retrospective (2023)", df[(df.kind == "kharif") & (df.design == "retrospective")]),
                    ("kharif, prospective (2024-2026)", df[(df.kind == "kharif") & (df.design == "prospective")]),
                    ("rabi, retrospective (2023-24)", df[(df.kind == "rabi") & (df.design == "retrospective")]),
                    ("rabi, prospective (2024-25, 2025-26)", df[(df.kind == "rabi") & (df.design == "prospective")]),
                    ("all seasons", df)):
        rows.append({unit: name, **counts(k)})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sensitivity", nargs="*", type=float, default=[-0.75, -1.25],
                    help="extra confirmation thresholds to report (robustness only; -1 is the rule)")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    dd = daily(SEASONS)
    dd.to_csv(OUT / "replay_daily.csv", index=False)
    ss = seasons_table(dd)
    ss.to_csv(OUT / "replay_seasons.csv", index=False)
    known = ss[ss.official_level.notna()]
    md = mandal_seasons(known)
    md.to_csv(OUT / "replay_mandal_seasons.csv", index=False)
    by_site, by_mandal = by_group(known, "site-seasons"), by_group(md, "mandal-seasons")
    partial = ss[ss.partial_season].groupby("season").season_end.max()
    cover = ss.groupby("kind").apply(lambda g: g.dates_with_satellite.sum() / max(1, g.site_dates.sum()))
    decl = known[known.official_level > 0]
    lines = ["# Operational replay of the integrated system: kharif and rabi, 2023-2026", "",
             f"Every 5 days; kharif = 1 Jun - 30 Nov, rabi = 1 Dec - 31 Mar; weather {WEATHER_DELAY_DAYS} days "
             f"late (AgERA5), satellite {SAT_DELAY_DAYS} days late; weather older than {C.STEP_DAYS} days is not "
             f"used. Alarm = SPEI-30 < {C.ALARM_SPEI} or a Severe +{H}-day forecast; confirmed = median rainfed "
             f"SVI < {C.STRESS_Z:g} from >= {MIN_SAT_FIELDS} fields, each field's latest image at most "
             f"{C.MAX_INPUT_AGE} days old on the issue date. No crop model is used.", "",
             "**Carry-over vs in-season.** A confirmation counts as *in-season* only if every image behind it was "
             "taken inside the evaluated season. Early in a season (especially 1 December, the first rabi issue "
             "date) the latest images still show the end of the previous season, so a confirmation then reports "
             "CONTINUING earlier stress, not new stress in the season's own crops. Both counts are shown; "
             "'drought continuing' (SVI low while SPEI-90 < -1) is carry-over of weather drought by construction.",
             "",
             "**Data ends.** " + ("; ".join(f"{s}: partial, last issue date {d}" for s, d in partial.items())
                                  if len(partial) else "all seasons complete") + ".", "",
             "**Retrospective vs prospective.** The farmland mask, field segments and irrigation flag were derived "
             "from 2019-2023 imagery, so kharif 2023 and rabi 2023-24 are RETROSPECTIVE; later seasons are "
             "PROSPECTIVE with respect to every fitted or selected component.", "",
             "**Thresholds fixed in advance.** SPEI < -1 (moderate drought, McKee et al. 1993 / WMO convention), "
             "SVI < -1 (one standard deviation below the field's normal), >= 5 fields and the data delays were set in "
             "run_system.py before this replay was written; they were not tuned on it.", "",
             "**Satellite coverage** (share of site-dates with at least 5 clear, labelled rainfed fields): "
             + ", ".join(f"{k} {v:.0%}" for k, v in cover.items())
             + ". A possible reason for the weak rabi response (a hypothesis, not tested here): fewer rainfed "
             "fields carry a crop after December, and December greenness is dominated by late kharif crops.", "",
             "## Each official decision counted once (mandal x season)", "",
             "Lepakshi and Cholasamudram lie in Lepakshi mandal and share one weather cell; Balaji Villas and "
             "Pullaiah lie in Kurnool Urban and share one weather cell. Each mandal-season is one event (confirmed if "
             "any of its sites is confirmed); ambiguous (Adoni / Peddakadubur border) and unknown (Sira, Karnataka "
             "rabi) cases are excluded.", "",
             to_md(by_mandal, index=False), "",
             "## Site-seasons", "", to_md(by_site, index=False), "",
             f"Median lead before the order, declared site-seasons confirmed in advance: "
             f"{decl.lead_days_before_GO.median():.0f} days.", "",
             "## Mandal x season detail", "",
             to_md(md.drop(columns=["official_level", "confirmed_dates"]), index=False), "",
             "## Season summary per site", "", to_md(ss, index=False), "",
             "Small sample (one area per mandal; declarations are administrative decisions, not field-level "
             "ground truth): read as case evidence, not a statistical test. '0/10 false alarms' means no flag in "
             "ten undeclared cases; with so few, spatially related cases the true rate could still be about 30% "
             "(approximate 95% upper bound for 0/10). Site-to-mandal assignment uses the site centre, not a "
             "polygon overlay with official mandal boundaries.", ""]
    sens = []
    for z in [C.STRESS_Z] + list(a.sensitivity):
        k = known if z == C.STRESS_Z else seasons_table(daily(SEASONS, z)).pipe(lambda t: t[t.official_level.notna()])
        sens.append({"confirmation threshold (SVI <)": z, **counts(mandal_seasons(k))})
    lines += ["## Sensitivity to the confirmation threshold (mandal-seasons, all seasons; the rule stays SVI < -1)", "",
              to_md(pd.DataFrame(sens), index=False), ""]
    (OUT / "REPLAY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(by_mandal.to_string(index=False))
    print(md[["season", "mandal", "official", "system_first_confirmed", "confirmed_before_GO"]].to_string(index=False))
    print("satellite coverage:", cover.round(2).to_dict())


if __name__ == "__main__":
    main()
