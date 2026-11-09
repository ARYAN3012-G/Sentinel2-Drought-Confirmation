"""
Read the GPS position stored in DJI drone photos and write them as a Google Earth file,
so the surveyed fields can be digitised exactly.

Usage:
    python tools/drone_gps_to_kml.py <photo folder> [<photo folder> ...]

Folders are searched recursively for .jpg/.jpeg. Outputs (in data/polygons/):
    drone_photo_points.kml   one pin per photo, grouped by site and flight date
    drone_photo_points.csv   file, date, site, lat, lon, altitude
    drone_flights.csv        per site/date: photo count, centre, extent in metres
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image
from PIL.ExifTags import GPSTAGS

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "polygons"

# Village / area centres from study_sites_google_earth.kml (used only to name the site)
SITES = {
    "Somandepalle": (14.0082, 77.6051),
    "Lepakshi": (13.7998, 77.6194),
    "Cholasamudram": (13.8118, 77.5687),
    "Sira": (13.7975, 76.9750),
    "Peddakadubur": (15.7826, 77.2528),
    "Kurnool_Dinnedevarapadu": (15.7715, 78.0471),
    "Kurnool_Balaji_Villas": (15.7834, 78.0561),
    "Kurnool_Pullaiah": (15.7982, 78.0806),
}


def dist_m(a, b):
    lat = math.radians((a[0] + b[0]) / 2)
    dy = (a[0] - b[0]) * 111_320
    dx = (a[1] - b[1]) * 111_320 * math.cos(lat)
    return math.hypot(dx, dy)


def to_deg(v, ref):
    d = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
    return -d if ref in ("S", "W") else d


def read_gps(path):
    exif = Image.open(path).getexif()
    gps = {GPSTAGS.get(k, k): v for k, v in exif.get_ifd(0x8825).items()}
    if "GPSLatitude" not in gps:
        return None
    lat = to_deg(gps["GPSLatitude"], gps["GPSLatitudeRef"])
    lon = to_deg(gps["GPSLongitude"], gps["GPSLongitudeRef"])
    alt = float(gps.get("GPSAltitude", 0))
    dt = exif.get(306, "")  # DateTime "YYYY:MM:DD HH:MM:SS"
    date = dt[:10].replace(":", "-") if dt else ""
    return lat, lon, alt, date


def nearest_site(lat, lon):
    name, d = min(((n, dist_m((lat, lon), c)) for n, c in SITES.items()), key=lambda t: t[1])
    return (name if d < 15_000 else "unknown"), d


def main(folders):
    rows, skipped = [], 0
    for folder in folders:
        for p in sorted(Path(folder).rglob("*")):
            if p.suffix.lower() not in (".jpg", ".jpeg"):
                continue
            try:
                g = read_gps(p)
            except Exception:
                g = None
            if g is None:
                skipped += 1
                continue
            lat, lon, alt, date = g
            site, d = nearest_site(lat, lon)
            rows.append(dict(file=p.name, date=date, site=site, lat=round(lat, 6),
                             lon=round(lon, 6), alt_m=round(alt, 1), dist_to_pin_m=round(d)))
    if not rows:
        sys.exit("No photos with GPS found.")
    # One photo can be copied into several folders: keep the first copy only
    seen, uniq = set(), []
    for r in rows:
        if r["file"] not in seen:
            seen.add(r["file"])
            uniq.append(r)
    rows = uniq

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "drone_photo_points.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    groups = defaultdict(list)
    for r in rows:
        groups[(r["site"], r["date"])].append(r)

    with open(OUT_DIR / "drone_flights.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["site", "date", "photos", "centre_lat", "centre_lon",
                    "extent_ns_m", "extent_ew_m", "centre_to_pin_m"])
        for (site, date), rs in sorted(groups.items()):
            lats = [r["lat"] for r in rs]
            lons = [r["lon"] for r in rs]
            c = (sum(lats) / len(lats), sum(lons) / len(lons))
            ns = dist_m((min(lats), c[1]), (max(lats), c[1]))
            ew = dist_m((c[0], min(lons)), (c[0], max(lons)))
            pin = dist_m(c, SITES[site]) if site in SITES else float("nan")
            w.writerow([site, date, len(rs), round(c[0], 6), round(c[1], 6),
                        round(ns), round(ew), round(pin)])

    kml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
           '<name>Drone photo positions</name>',
           '<Style id="p"><IconStyle><scale>0.5</scale><color>ff00ffff</color>'
           '<Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>'
           '</IconStyle><LabelStyle><scale>0</scale></LabelStyle></Style>']
    for (site, date), rs in sorted(groups.items()):
        kml.append(f"<Folder><name>{site} {date} ({len(rs)} photos)</name>")
        for r in rs:
            kml.append(f"<Placemark><name>{r['file']}</name><styleUrl>#p</styleUrl>"
                       f"<Point><coordinates>{r['lon']},{r['lat']},0</coordinates></Point></Placemark>")
        kml.append("</Folder>")
    kml.append("</Document></kml>")
    (OUT_DIR / "drone_photo_points.kml").write_text("\n".join(kml), encoding="utf-8")

    print(f"{len(rows)} photos with GPS, {skipped} without GPS")
    print(f"Wrote {OUT_DIR / 'drone_photo_points.kml'}")
    print(f"Wrote {OUT_DIR / 'drone_flights.csv'}")
    for (site, date), rs in sorted(groups.items()):
        print(f"  {site:26s} {date}  {len(rs):5d} photos")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
