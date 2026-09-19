"""
satellite_simulator.py

Generates realistic, physics-grounded multi-year Sentinel-2 time series (2020–2025)
for all 40 verified agricultural fields across the 8 Rayalaseema study sites.
Grounded in:
  - 5-day Sentinel-2 revisit cadence + monsoon cloud masking
  - Dual-crop phenology (Kharif: Jun–Nov, Rabi: Dec–Apr)
  - AP Govt annual drought notifications (2020 Rabi, 2023 Kharif, 2025 Kharif G.O.Ms.No.6)
  - Drone UAV ground-truth confirmations (Somandepalle 40.3%, Sira 56.7%, Lepakshi ~79%, Peddakadubur)
  - Kurnool healthy benchmark cluster
"""
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd

# Set deterministic seed
np.random.seed(42)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
GEOJSON_PATH = ROOT_DIR / "data" / "polygons" / "verified_40_fields.geojson"
OUTPUT_DIR = ROOT_DIR / "data" / "processed" / "satellite"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Study site classifications and baseline drought probabilities
DROUGHT_DECLARED_SITES = {
    "Somandepalle": {"rainfed_risk": 0.85, "soil": "red_loam"},
    "Lepakshi": {"rainfed_risk": 0.90, "soil": "red_sandy"},
    "Cholasamudram": {"rainfed_risk": 0.95, "soil": "red_sandy"},
    "Sira": {"rainfed_risk": 0.80, "soil": "mixed_red_black"},
    "Peddakadubur": {"rainfed_risk": 0.65, "soil": "black_cotton"},
    "Kurnool_Dinnedevarapadu": {"rainfed_risk": 0.15, "soil": "black_cotton"},
    "Kurnool_Balaji_Villas": {"rainfed_risk": 0.10, "soil": "alluvial_loam"},
    "Kurnool_Pullaiah": {"rainfed_risk": 0.15, "soil": "mixed_black"},
}

# Historical Rayalaseema drought severity factor per year (2020-2025)
# Grounded in AP State Disaster Management Authority historical records:
# 2020: Rabi dry spell in South Rayalaseema
# 2021: Normal monsoon, mild localized stress
# 2022: Excess rainfall (healthy)
# 2023: Severe Kharif drought across Anantapur/Sathya Sai (45 mandals declared)
# 2024: Moderate dry spell
# 2025: Confirmed Kharif drought (G.O.Ms.No.6 dt. 31.10.2025) & UAV drone confirmed
YEARLY_DROUGHT_FACTOR = {
    2020: 0.40,  # moderate regional stress (Rabi spell)
    2021: 0.20,  # mostly normal
    2022: 0.10,  # wet year
    2023: 0.75,  # historical severe drought year in southern Rayalaseema
    2024: 0.35,  # moderate stress
    2025: 0.85   # verified drought year per G.O.Ms.No.6 and drone surveys
}

def get_crop_phenology(doy: int, is_drought: int, soil: str, field_noise: float):
    """
    Computes expected NDVI, NDMI, SAVI for a specific Day of Year (DOY).
    Accounts for dual cropping (Kharif Jun-Nov, Rabi Dec-Apr) and drought suppression.
    """
    base_ndvi = 0.16 if soil == "red_sandy" else 0.19
    base_ndmi = -0.18
    base_savi = base_ndvi * 0.85

    # 1. Kharif Season (DOY 160 - 330: June to November)
    if 160 <= doy <= 330:
        rel_t = (doy - 160) / 170.0
        curve = math.sin(rel_t * math.pi) ** 1.8

        if is_drought == 2:  # Severe drought
            peak_ndvi = 0.28 + 0.05 * field_noise
            peak_ndmi = -0.06 + 0.04 * field_noise
        elif is_drought == 1:  # Moderate drought
            peak_ndvi = 0.46 + 0.06 * field_noise
            peak_ndmi = 0.12 + 0.05 * field_noise
        else:  # Healthy
            peak_ndvi = 0.72 + 0.07 * field_noise
            peak_ndmi = 0.34 + 0.05 * field_noise

        ndvi = base_ndvi + (peak_ndvi - base_ndvi) * curve
        ndmi = base_ndmi + (peak_ndmi - base_ndmi) * curve
        savi = ndvi * 0.90

    # 2. Rabi Season (DOY 335 to DOY 100: December to mid-April)
    elif doy >= 335 or doy <= 100:
        if doy >= 335:
            rel_t = (doy - 335) / 130.0
        else:
            rel_t = (doy + 30) / 130.0
        rel_t = min(max(rel_t, 0.0), 1.0)
        curve = math.sin(rel_t * math.pi) ** 1.5

        if is_drought == 2:
            peak_ndvi = 0.32 + 0.04 * field_noise
            peak_ndmi = 0.01 + 0.04 * field_noise
        elif is_drought == 1:
            peak_ndvi = 0.48 + 0.05 * field_noise
            peak_ndmi = 0.15 + 0.04 * field_noise
        else:
            peak_ndvi = 0.65 + 0.06 * field_noise
            peak_ndmi = 0.28 + 0.05 * field_noise

        ndvi = base_ndvi + (peak_ndvi - base_ndvi) * curve
        ndmi = base_ndmi + (peak_ndmi - base_ndmi) * curve
        savi = ndvi * 0.90

    # 3. Summer Fallow (DOY 101 to 159: mid-April to May)
    else:
        ndvi = base_ndvi + np.random.normal(0, 0.015)
        ndmi = base_ndmi + np.random.normal(0, 0.02)
        savi = base_savi + np.random.normal(0, 0.015)

    # Realistic sensor & atmospheric noise
    ndvi = float(np.clip(ndvi + np.random.normal(0, 0.02), 0.05, 0.95))
    ndmi = float(np.clip(ndmi + np.random.normal(0, 0.025), -0.40, 0.70))
    savi = float(np.clip(savi + np.random.normal(0, 0.02), 0.04, 0.90))

    return ndvi, ndmi, savi

def generate_satellite_timeseries():
    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    all_rows = []
    date_range = pd.date_range(start="2020-01-01", end="2025-12-31", freq="5D")

    print(f"Simulating Sentinel-2 time series for {len(geojson['features'])} fields across {len(date_range)} observation dates...")

    for feat in geojson["features"]:
        props = feat["properties"]
        field_id = props["field_id"]
        site = props["site"]
        area_ha = props["area_ha"]
        area_acres = props["area_acres"]

        site_meta = DROUGHT_DECLARED_SITES.get(site, {"rainfed_risk": 0.5, "soil": "red_loam"})
        soil = site_meta["soil"]
        field_noise = np.random.uniform(-0.5, 0.5)

        hist_ndvi_min = 0.12 + 0.03 * np.random.uniform(0, 1)
        hist_ndvi_max = 0.82 + 0.05 * np.random.uniform(0, 1)

        field_records = []
        for dt in date_range:
            year = dt.year
            doy = dt.dayofyear
            month = dt.month

            # Cloud masking probability: high in peak monsoon, low in winter
            cloud_prob = 0.35 if month in [7, 8] else (0.20 if month in [6, 9, 10] else 0.05)
            if np.random.random() < cloud_prob:
                continue

            # Determine drought state based on year severity factor and site rainfed risk
            year_factor = YEARLY_DROUGHT_FACTOR.get(year, 0.3)
            risk = year_factor * site_meta["rainfed_risk"] + 0.1 * field_noise

            if 105 <= doy <= 155:
                # Normal summer fallow
                is_drought = 0
            elif risk > 0.55:
                is_drought = 2  # Severe drought
            elif risk > 0.30:
                is_drought = 1  # Moderate drought
            else:
                is_drought = 0  # Healthy

            # In 2025 Kharif specifically: strictly enforce G.O.Ms.No.6 and drone survey truth
            if year == 2025 and 150 <= doy <= 340:
                if site in ["Somandepalle", "Lepakshi", "Cholasamudram", "Sira"]:
                    is_drought = 2
                elif site in ["Peddakadubur"]:
                    is_drought = 1 if np.random.random() < 0.6 else 2
                else:
                    is_drought = 0

            ndvi, ndmi, savi = get_crop_phenology(doy, is_drought, soil, field_noise)
            vci = float(np.clip(100.0 * (ndvi - hist_ndvi_min) / (hist_ndvi_max - hist_ndvi_min), 0.0, 100.0))

            row = {
                "date": dt.strftime("%Y-%m-%d"),
                "year": year,
                "doy": doy,
                "field_id": field_id,
                "site": site,
                "area_ha": area_ha,
                "area_acres": area_acres,
                "NDVI": round(ndvi, 4),
                "NDMI": round(ndmi, 4),
                "SAVI": round(savi, 4),
                "VCI": round(vci, 2),
                "label": is_drought
            }
            field_records.append(row)
            all_rows.append(row)

        df_field = pd.DataFrame(field_records)
        df_field.to_csv(OUTPUT_DIR / f"{field_id}.csv", index=False)

    df_pooled = pd.DataFrame(all_rows)
    pooled_path = OUTPUT_DIR / "pooled_satellite_40fields.csv"
    df_pooled.to_csv(pooled_path, index=False)

    print(f"\nGenerated multi-year satellite dataset:")
    print(f"  - Total observations across 40 fields: {len(df_pooled):,}")
    print(f"  - Date range: {df_pooled['date'].min()} to {df_pooled['date'].max()}")
    print(f"  - Class distribution:\n{df_pooled['label'].value_counts().to_dict()}")
    print(f"  - Saved pooled CSV to: {pooled_path}")
    return df_pooled

if __name__ == "__main__":
    generate_satellite_timeseries()
