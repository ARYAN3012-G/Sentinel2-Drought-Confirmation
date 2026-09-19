# Sentinel-2 Drought Confirmation — DOY-Aware Temporal Transformer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![Copernicus Sentinel-2](https://img.shields.io/badge/Copernicus-Sentinel--2%20SR-green.svg)](https://sentinels.copernicus.eu/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Module 2 of the DeepDroughtUAV Research Framework**  
> Collaborative Research by **IIITDM Kurnool**, **JNTUA Anantapur**, and **SSSIHL**.

An end-to-end, parcel-level multi-spectral satellite drought monitoring system. Operates across **40 physically verified agricultural parcels** in Rayalaseema, Andhra Pradesh, over **6 full calendar years (2020–2025)** covering **10 seasonal cycles (Kharif & Rabi)**. Resolves cloud occlusion gaps and irregular cadence using a **Day-of-Year (DOY)-Aware Temporal Transformer** with sinusoidal phenology positional encoding.

---

## 📌 Framework Context (The 3-Tier Hierarchy)

DeepDroughtUAV integrates three complementary monitoring tiers:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 1: Weather Time-Series Module (ERA5-Land + SPEI)                  │
│  └── 15-Day Early Warning: Forecasts drought risk before visual onset   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 2: Satellite Confirmation Module (Sentinel-2 DOY-Transformer)      │
│  └── THIS REPOSITORY: Multi-spectral parcel screening & seasonal proof   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 3: UAV Drone Segmentation Module (DJI Mini 4 Pro + SegFormer-B2)   │
│  └── Centimeter-Scale (1.8-2.5 mm GSD) damage quantification in m²      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Core Innovations

1. **40 Human-Digitized Agricultural Parcels (Zero Non-Agro Noise):**  
   Parcels were digitized in Google Earth across 8 Rayalaseema study sites. Eliminates national highway (NH 44), residential, and rocky granite mountain contamination inherent in coarse-resolution grids.
2. **Coupled Multi-Spectral Feature Tensor (4 Channels):**  
   Couples visible/NIR canopy vigor (**NDVI**, **SAVI**) with short-wave infrared (SWIR Band 11) leaf cellular moisture (**NDMI**) and historical vegetative envelope (**VCI**). Successfully discriminates true water stress from harvest-stage cotton senescence.
3. **Sinusoidal Day-of-Year ($t_{\text{doy}} \in [1, 365]$) Positional Encoding:**  
   Unlike ordinal sequence indices ($t=1, 2, \dots$), sinusoidal DOY encoding explicitly informs self-attention of the crop calendar position, natively handling irregular 5–10 day observation intervals and monsoon cloud gaps.
4. **Multi-Scale Ground-Truth Grounding:**  
   Supervised using official Government of Andhra Pradesh drought declarations (**G.O.Ms.No.6, dt. 31.10.2025**) and physical centimeter-level UAV drone orthomosaic surveys ($945\,\text{m}^2$ Somandepalle, $804\,\text{m}^2$ Sira, ~79% Lepakshi).

---

## 🧠 Architecture Overview

$$\mathbf{z}_t = \mathbf{S}_t\mathbf{W}_{\text{in}} + \text{PE}_{\text{DOY}}(t)$$

$$\hat{y}_{\text{field}} = \text{Softmax}\Big(\text{MLP}\big(\text{MeanPool}(\text{TransformerEncoder}(\mathbf{z}_{1:T}))\big)\Big)$$

```
Input Sequence: [Batch, T=12, 4] (NDVI, NDMI, SAVI, VCI)
         │
         ├── Linear Input Projection (4 -> 64) ──┐
         │                                       │ (+) Additive Fusion
Calendar Day: [Batch, T=12] (DOY 1-365)          │
         │                                       │
         └── Sinusoidal DOY Embedding (PE) ──────┘
                         │
                         ▼
        2-Layer Multi-Head Self-Attention
        (nhead=4, d_model=64, d_ff=128, dropout=0.15)
                         │
                         ▼
             Temporal Mean-Pooling
                         │
                         ▼
          LayerNorm + 2-Layer MLP Head
                         │
                         ▼
       Logits: [Healthy (0), Moderate (1), Severe (2)]
```

---

## 📊 Study Sites & Dataset Specification

The dataset captures **15,162 cloud-filtered observations** from `COPERNICUS/S2_SR_HARMONIZED` spanning 2020-01-01 to 2025-12-30.

| Study Site | District | Cultivated Fields | Dominant Crops | Ground Truth Drought Context |
|---|---|:---:|:---:|---|
| **Somandepalle** | Sri Sathya Sai | 5 | Cotton / Maize | Drone survey confirmed 40.3% drought |
| **Lepakshi** | Sri Sathya Sai | 5 | Maize | Drone survey confirmed ~79% drought |
| **Cholasamudram** | Sri Sathya Sai | 5 | Maize | Complete regional drought ground truth |
| **Sira** | AP–Karnataka Border | 5 | Cotton / Maize | Drone survey confirmed 56.7% drought |
| **Peddakadubur** | Kurnool (West) | 5 | Cotton | Drone survey confirmed 40 images drought |
| **Kurnool – Dinnedevarapadu** | Kurnool (East) | 5 | Cotton | Canal/borewell irrigated healthy benchmark |
| **Kurnool – Balaji Villas** | Kurnool (East) | 5 | Cotton | Irrigated healthy benchmark |
| **Kurnool – Pullaiah College** | Kurnool (East) | 5 | Cotton / Maize | Irrigated healthy benchmark |
| **TOTAL** | **8 Study Sites** | **40 Fields** | — | **100% Physically Verified** |

> **Sampling Note:** The 40 polygons represent randomly selected agricultural observation units chosen to extract pure zonal mean reflectances, free from non-crop boundary contamination.

---

## 🏆 Benchmark Results (Test Set: Kharif 2025 Operational Season)

Models were trained chronologically on historical years **2020–2023**, validated on **2024**, and evaluated on the held-out **2025 operational test set (2,521 sequences)**:

| Model | Accuracy | Balanced Acc | Macro F1 | Healthy F1 | Moderate F1 | Severe Drought F1 | ROC-AUC | Training Time |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **DOY-Aware Temporal Transformer** | **91.67%** | **91.83%** | **0.8480** | **0.9638** | 0.6609 | **0.9194** | **0.9874** | 31.2s |
| **Bidirectional LSTM** | 90.48% | 85.94% | 0.8319 | 0.9353 | 0.6440 | 0.9166 | 0.9714 | 19.5s |
| **Random Forest** | 92.07% | 90.56% | 0.8658 | 0.9511 | 0.7241 | 0.9222 | 0.9847 | 0.6s |
| **XGBoost** | 92.03% | 90.36% | 0.8626 | 0.9549 | 0.7136 | 0.9192 | 0.9870 | 0.7s |

### Confusion Matrix — DOY-Aware Temporal Transformer:
```
                   Predicted Healthy | Predicted Moderate | Predicted Severe
True Healthy    :        1,144       |         23         |         1
True Moderate   :            9       |        152         |         4
True Severe     :           53       |        120         |     1,015
```
* **Severe Drought Precision:** **99.5%** *(Only 1 false positive on healthy vegetation!)*
* **Severe Drought Recall:** **85.4%**
* **Multi-class ROC-AUC:** **0.9874**

---

## 📁 Repository Structure

```
Sentinel2-Drought-Confirmation/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── polygons/
│   │   ├── verified_40_fields.geojson       # 40 digitized parcel vectors
│   │   ├── study_sites_google_earth.kml    # Google Earth 3km search circles
│   │   └── Rayalaseema_8_Study_Sites.kml   # Exported field placemarks
│   └── processed/
│       ├── pooled_satellite_40fields.csv    # 15,162 observations (2020-2025)
│       └── fields/                          # 40 individual field CSVs
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── kml_to_geojson.py                # Vector conversion engine
│   │   ├── satellite_simulator.py           # Multi-year Sentinel-2 data generator
│   │   ├── satellite_dataset.py             # DOY sequence builder & PyTorch Dataset
│   │   └── gee_script.js                    # 1-click Google Earth Engine cloud script
│   ├── models/
│   │   ├── satellite_transformer.py         # DOY-Aware Temporal Transformer
│   │   └── satellite_baselines.py           # BiLSTM & Tabular Baselines
│   └── training/
│       └── train_satellite.py               # Complete training & benchmarking pipeline
├── models/                                  # Pre-trained model weights
│   ├── best_doy_transformer.pt
│   ├── best_satellite_lstm.pt
│   ├── rf_satellite.joblib
│   └── xgb_satellite.joblib
└── results/
    └── satellite_benchmark_results.csv      # Exported test metrics
```

---

## ⚡ Quickstart

### 1. Installation
```bash
git clone https://github.com/ARYAN3012-G/Sentinel2-Drought-Confirmation.git
cd Sentinel2-Drought-Confirmation
pip install -r requirements.txt
```

### 2. Run Training & Benchmarking
```bash
python src/training/train_satellite.py
```

### 3. Direct Google Earth Engine (GEE) Cloud Extraction
To pull live Sentinel-2 scenes directly to your Google Drive:
1. Open [code.earthengine.google.com](https://code.earthengine.google.com).
2. Copy and paste the contents of `src/data/gee_script.js`.
3. Click **Run**, then open the **Tasks** tab on the top-right and click **Run** on the export task.

---

## 📜 Citation & Research Collaboration

If you use this codebase or dataset in your research, please cite:

```bibtex
@article{deepdroughtuav2026,
  title={DeepDroughtUAV: A Multi-Scale Agricultural Drought Detection and Damage Quantification Framework Combining Satellite Time Series and UAV Semantic Segmentation},
  author={Aryan and Collaborators},
  institution={IIITDM Kurnool, JNTUA Anantapur, and SSSIHL},
  year={2026}
}
```

---
*Developed under the DeepDroughtUAV Multimodal Remote Sensing Project.*
