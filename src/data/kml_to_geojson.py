"""
kml_to_geojson.py

Parses an exported Google Earth KML file containing 8 sites x 5 fields = 40 polygons,
validates the coordinates, calculates field areas, and saves standardized GeoJSON.
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import math

def parse_kml_coordinates(coord_text):
    """Parses KML coordinate text 'lon,lat,alt lon,lat,alt ...' into [[lon, lat], ...]"""
    pts = []
    for pair in coord_text.strip().split():
        parts = pair.split(",")
        if len(parts) >= 2:
            pts.append([float(parts[0]), float(parts[1])])
    return pts

def estimate_polygon_area_ha(coords):
    """Approximate spherical area in hectares for lat/lon coordinates."""
    if len(coords) < 3:
        return 0.0
    total = 0.0
    for i in range(len(coords)):
        p1 = coords[i]
        p2 = coords[(i + 1) % len(coords)]
        total += (p2[0] - p1[0]) * math.pi / 180 * (2 + math.sin(p1[1] * math.pi / 180) + math.sin(p2[1] * math.pi / 180))
    area_m2 = abs(total * 6378137 * 6378137 / 2)
    return round(area_m2 / 10000.0, 2)

def convert_kml_to_geojson(kml_path, output_geojson_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Handle XML namespace
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    if not root.tag.endswith("kml"):
        ns = {}

    features = []
    
    # Find all Placemarks
    placemarks = root.findall(".//kml:Placemark", ns) if ns else root.findall(".//Placemark")

    site_mapping = {
        "som": "Somandepalle",
        "lep": "Lepakshi",
        "cho": "Cholasamudram",
        "sir": "Sira",
        "ped": "Peddakadubur",
        "din": "Kurnool_Dinnedevarapadu",
        "bal": "Kurnool_Balaji_Villas",
        "pul": "Kurnool_Pullaiah"
    }

    for pm in placemarks:
        name_elem = pm.find("kml:name", ns) if ns else pm.find("name")
        name = name_elem.text.strip() if name_elem is not None and name_elem.text else "Unnamed"

        # Ignore search circles and center pins
        if "circle" in name.lower() or "search boundary" in name.lower() or "center" in name.lower():
            continue

        # Look for Polygon
        polygon = pm.find(".//kml:Polygon", ns) if ns else pm.find(".//Polygon")
        if polygon is None:
            continue

        coord_elem = polygon.find(".//kml:coordinates", ns) if ns else polygon.find(".//coordinates")
        if coord_elem is None or not coord_elem.text:
            continue

        coords = parse_kml_coordinates(coord_elem.text)
        if len(coords) < 3:
            continue

        # Ensure closed ring
        if coords[0] != coords[-1]:
            coords.append(coords[0])

        area_ha = estimate_polygon_area_ha(coords)
        area_acres = round(area_ha * 2.47105, 2)

        # Detect site name from field name
        site_detected = "Unknown"
        name_lower = name.lower()
        for key, sname in site_mapping.items():
            if key in name_lower:
                site_detected = sname
                break

        features.append({
            "type": "Feature",
            "properties": {
                "field_id": name,
                "site": site_detected,
                "area_ha": area_ha,
                "area_acres": area_acres,
                "vertex_count": len(coords)
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "name": "Rayalaseema_40_Verified_Fields",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": features
    }

    Path(output_geojson_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_geojson_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)

    print(f"Successfully converted {len(features)} field polygons to {output_geojson_path}")
    return geojson

if __name__ == "__main__":
    import sys
    kml_file = sys.argv[1] if len(sys.argv) > 1 else "study_sites_google_earth.kml"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "data/polygons/verified_40_fields.geojson"
    convert_kml_to_geojson(kml_file, out_file)
