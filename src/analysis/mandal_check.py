"""
Mandal check: which official sub-district (mandal) does each site centre and each monitored field lie in?

Boundaries: geoBoundaries gbOpen IND ADM3 (source: Pathways Data / lgdirectory.gov.in, year 2018; CC BY 4.0).
A subset of the mandals around the 8 sites is kept in data/official/mandal_boundaries_2018_subset.geojson.
2018 boundaries pre-date the 2022 Andhra Pradesh reorganisation, in which the old Kurnool mandal was split
into Kurnool Urban and Kurnool Rural (the names used in the 2023-2026 orders) - so for the Kurnool sites this
check can say "Kurnool vs Kallur", not "Urban vs Rural".

    python src/analysis/mandal_check.py [--full path/to/geoBoundaries-IND-ADM3.geojson] [--rabi path/to/rabi_module]
Writes results/qc/MANDAL_CHECK.md and results/qc/mandal_check.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SUBSET = ROOT / "data" / "official" / "mandal_boundaries_2018_subset.geojson"
KEEP = ["Adoni", "Agali", "Chilamathur", "Gauribidanur", "Gorantla", "Gudibanda", "Hindupur", "Hiriyur", "Kallur",
        "Kosigi", "Kowthalam", "Kurnool", "Lepakshi", "Madhugiri", "Mantralayam", "Orvakal", "Pedda Kadubur",
        "Penukonda", "Rolla", "Sira", "Somandepalle"]
# mandal used for scoring in the replay / rabi protocol (data/official/drought_declarations.csv)
SCORED = {"Som": "Somandepalli", "Lep": "Lepakshi", "Cho": "Lepakshi", "Sira": "Sira taluk",
          "Ped": "Adoni (border with Peddakadubur)", "Din": "Kurnool Rural", "Bal": "Kurnool Urban",
          "Pul": "Kurnool Urban"}


def rings(geom):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return polys


def in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][:2]
        xj, yj = ring[j][:2]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def in_geom(x, y, geom):
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in rings(geom))


def centroid(geom):
    ring = rings(geom)[0][0]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def load_mandals(full: str | None):
    if full:
        d = json.loads(Path(full).read_text(encoding="utf-8"))
        feats = [f for f in d["features"] if f["properties"]["shapeName"] in KEEP]
        SUBSET.write_text(json.dumps({"type": "FeatureCollection", "source": "geoBoundaries gbOpen IND ADM3 "
                                      "(Pathways Data Pvt. Ltd., lgdirectory.gov.in, 2018), CC BY 4.0",
                                      "features": feats}), encoding="utf-8")
    return json.loads(SUBSET.read_text(encoding="utf-8"))["features"]


def which(x, y, mandals):
    hit = [m["properties"]["shapeName"] for m in mandals if in_geom(x, y, m["geometry"])]
    return hit[0] if hit else "outside subset"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full")
    ap.add_argument("--rabi", default=str(ROOT.parent / "rabi_module"))
    a = ap.parse_args()
    mandals = load_mandals(a.full)
    sites = pd.read_csv(ROOT / "data" / "sites.csv")
    rows = [dict(kind="site centre", site_code=r.site_code, field_id="-", x=r.centre_lon, y=r.centre_lat)
            for r in sites.itertuples()]
    segs = json.loads((ROOT / "data" / "gee_exports" / "field_segments_v2.geojson").read_text(encoding="utf-8"))
    used = set(pd.read_csv(C.FIELD_TS_FILE, usecols=["field_id"]).field_id)
    for f in segs["features"]:
        if f["properties"]["field_id"] in used:
            x, y = centroid(f["geometry"])
            rows.append(dict(kind="kharif field", site_code=f["properties"]["site_code"],
                             field_id=f["properties"]["field_id"], x=x, y=y))
    rabi = Path(a.rabi)
    if (rabi / "data" / "frozen" / "fields_v1.csv").exists():
        ids = set(pd.read_csv(rabi / "data" / "frozen" / "fields_v1.csv").field_id)
        for s in SCORED:
            g = json.loads((rabi / "data" / "gee_exports" / f"C1v2_candidates_{s}.geojson").read_text(encoding="utf-8"))
            for f in g["features"]:
                if f["properties"]["field_id"] in ids:
                    x, y = centroid(f["geometry"])
                    rows.append(dict(kind="rabi field", site_code=s, field_id=f["properties"]["field_id"], x=x, y=y))
    d = pd.DataFrame(rows)
    d["mandal_2018"] = [which(r.x, r.y, mandals) for r in d.itertuples()]
    d["scored_as"] = d.site_code.map(SCORED)
    out = ROOT / "results" / "qc"
    out.mkdir(parents=True, exist_ok=True)
    d.round(5).to_csv(out / "mandal_check.csv", index=False)

    order = list(SCORED)
    cen = d[d.kind == "site centre"].set_index("site_code").reindex(order)
    tab = (pd.crosstab([d.kind, d.site_code], d.mandal_2018).reindex(order, level=1))
    tab = tab[[c for c in tab.columns]].astype(int)

    def md(t):
        t = t.reset_index()
        r = ["| " + " | ".join(map(str, t.columns)) + " |", "|" + "---|" * len(t.columns)]
        return "\n".join(r + ["| " + " | ".join(str(v) for v in x) + " |" for x in t.itertuples(index=False)])

    lines = ["# Mandal check: site centres and monitored fields vs official sub-district boundaries", "",
             "Boundaries: geoBoundaries IND ADM3 (lgdirectory.gov.in, 2018). These pre-date the 2022 split of the "
             "old Kurnool mandal into Kurnool Urban / Kurnool Rural, so the Kurnool sites resolve to 'Kurnool' or "
             "'Kallur', not to Urban / Rural. Field position = centroid of its polygon vertices.", "",
             "## Site centres", "", md(cen[["mandal_2018", "scored_as"]]), "",
             "## Fields per site and mandal (counts)", "", md(tab), ""]
    (out / "MANDAL_CHECK.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
