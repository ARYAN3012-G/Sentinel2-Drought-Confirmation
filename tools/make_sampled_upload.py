"""
Turn Earth Engine script A's segment export into the upload for script B.

    python tools/make_sampled_upload.py [data/gee_exports/field_segments_v2.geojson]

Reads all field segments, keeps the randomly sampled ones (property sampled = 1, chosen in
script A with a fixed seed), checks the sample (20 rainfed + 10 irrigated per site, 240 in all)
and writes src/gee/upload/sampled_fields_v2.zip (shapefile, WGS84). Upload it in Earth Engine:
Assets -> NEW -> Shape files -> pick the zip -> asset name sampled_fields_v2.
"""
from __future__ import annotations

import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path

import shapefile  # pyshp

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "gee_exports" / "field_segments_v2.geojson"
OUT = ROOT / "src" / "gee" / "upload" / "sampled_fields_v2.zip"
WGS84 = ('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],'
         'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]')


def _clockwise(ring) -> bool:
    return sum((x2 - x1) * (y2 + y1) for (x1, y1), (x2, y2) in zip(ring[:-1], ring[1:])) > 0


def merge_site_files():
    """Script A with SPLIT_SEGMENTS = true exports one file per site: merge them into one."""
    parts = sorted(SRC.parent.glob("field_segments_v2_*.geojson"))
    if SRC.exists() or not parts:
        return
    feats = [f for p in parts for f in json.loads(p.read_text())["features"]]
    SRC.write_text(json.dumps({"type": "FeatureCollection", "features": feats}))
    print(f"Merged {len(parts)} site files ({len(feats)} segments) -> {SRC.name}")


def main():
    merge_site_files()
    feats = [f for f in json.loads(SRC.read_text())["features"] if int(f["properties"]["sampled"]) == 1]
    per = Counter((f["properties"]["site_code"], int(f["properties"]["irrigated"])) for f in feats)
    print(f"{len(feats)} sampled fields; per site (rainfed, irrigated):",
          {s: (per[(s, 0)], per[(s, 1)]) for s in sorted({k[0] for k in per})})
    if len(feats) != 240:
        print("WARNING: expected 240 (20 rainfed + 10 irrigated x 8 sites) - a site may have too few segments")
    shp, shx, dbf = io.BytesIO(), io.BytesIO(), io.BytesIO()
    w = shapefile.Writer(shp=shp, shx=shx, dbf=dbf, shapeType=shapefile.POLYGON)
    w.field("field_id", "C", 30); w.field("site", "C", 30); w.field("site_code", "C", 8)
    w.field("weather", "C", 30); w.field("irrigated", "N", 1); w.field("area_ha", "N", 8, 2)
    w.field("pixels", "N", 6)
    for f in feats:
        g, p = f["geometry"], f["properties"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        rings = []
        for poly in polys:                      # shapefile: outer ring clockwise, holes anticlockwise
            for k, r in enumerate(poly):
                r = [list(map(float, pt[:2])) for pt in r]
                rings.append(r if _clockwise(r) == (k == 0) else r[::-1])
        w.poly(rings)
        w.record(p["field_id"], p["site"], p["site_code"], p["weather_site"], int(p["irrigated"]),
                 float(p["area_ha"]), int(p["pixels"]))
    w.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for ext, buf in (("shp", shp), ("shx", shx), ("dbf", dbf)):
            z.writestr(f"sampled_fields_v2.{ext}", buf.getvalue())
        z.writestr("sampled_fields_v2.prj", WGS84)
    print(f"Wrote {OUT} - upload it as Earth Engine asset 'sampled_fields_v2'")


if __name__ == "__main__":
    main()
