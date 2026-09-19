"""
satellite_dataset.py

Builds sliding-window sequence datasets for Module 2 (Satellite Drought Confirmation).
Features:
  - 4 spectral channels: NDVI, NDMI, SAVI, VCI
  - Sinusoidal Day-of-Year (DOY) temporal encoding
  - Multi-year chronological split:
      Train: 2020–2023 (Historical normal + drought years)
      Val:   2024      (Prior year tuning)
      Test:  2025      (Operational test year with AP Govt Kharif declaration & UAV surveys)
  - PyTorch Dataset wrapper
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "satellite" / "pooled_satellite_40fields.csv"
FEATURES = ["NDVI", "NDMI", "SAVI", "VCI"]
SEQUENCE_LENGTH = 12  # ~60 to 90 days of seasonal observation history

def build_satellite_sequences(
    csv_path: Path = DATA_PATH,
    seq_len: int = SEQUENCE_LENGTH
) -> tuple[dict, dict, dict]:
    """
    Loads pooled satellite observations and constructs chronological sliding windows.
    Splits cleanly by calendar years:
      Train: 2020–2023
      Val:   2024
      Test:  2025
    """
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df.sort_values(["field_id", "date"]).reset_index(drop=True)

    train_X, train_doy, train_y, train_meta = [], [], [], []
    val_X, val_doy, val_y, val_meta = [], [], [], []
    test_X, test_doy, test_y, test_meta = [], [], [], []

    for field_id, field_df in df.groupby("field_id"):
        field_df = field_df.sort_values("date").reset_index(drop=True)
        n_obs = len(field_df)
        if n_obs < seq_len:
            continue

        feat_mat = field_df[FEATURES].values.astype(np.float32)
        doy_arr = field_df["doy"].values.astype(np.int64)
        labels = field_df["label"].values.astype(np.int64)
        dates = field_df["date"].values
        years = field_df["year"].values
        sites = field_df["site"].values

        n_seq = n_obs - seq_len + 1

        for i in range(n_seq):
            target_idx = i + seq_len - 1
            target_year = years[target_idx]
            target_date = dates[target_idx]
            target_label = labels[target_idx]

            x_window = feat_mat[i : i + seq_len]
            doy_window = doy_arr[i : i + seq_len]

            meta_entry = {
                "field_id": field_id,
                "site": sites[target_idx],
                "target_date": target_date
            }

            if target_year <= 2023:
                train_X.append(x_window)
                train_doy.append(doy_window)
                train_y.append(target_label)
                train_meta.append(meta_entry)
            elif target_year == 2024:
                val_X.append(x_window)
                val_doy.append(doy_window)
                val_y.append(target_label)
                val_meta.append(meta_entry)
            else:  # 2025
                test_X.append(x_window)
                test_doy.append(doy_window)
                test_y.append(target_label)
                test_meta.append(meta_entry)

    train_data = {
        "X": np.array(train_X, dtype=np.float32),
        "doy": np.array(train_doy, dtype=np.int64),
        "y": np.array(train_y, dtype=np.int64),
        "meta": pd.DataFrame(train_meta)
    }
    val_data = {
        "X": np.array(val_X, dtype=np.float32),
        "doy": np.array(val_doy, dtype=np.int64),
        "y": np.array(val_y, dtype=np.int64),
        "meta": pd.DataFrame(val_meta)
    }
    test_data = {
        "X": np.array(test_X, dtype=np.float32),
        "doy": np.array(test_doy, dtype=np.int64),
        "y": np.array(test_y, dtype=np.int64),
        "meta": pd.DataFrame(test_meta)
    }

    return train_data, val_data, test_data


class SatellitePyTorchDataset(Dataset):
    """PyTorch Dataset wrapper yielding (X, doy, y)."""
    def __init__(self, data_dict: dict):
        self.X = torch.tensor(data_dict["X"], dtype=torch.float32)
        self.doy = torch.tensor(data_dict["doy"], dtype=torch.long)
        self.y = torch.tensor(data_dict["y"], dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.doy[idx], self.y[idx]


if __name__ == "__main__":
    train_d, val_d, test_d = build_satellite_sequences()
    print("=== Satellite Sequence Dataset Built Successfully ===")
    print(f"Train sequences (2020-2023): {train_d['X'].shape}, Class dist: {np.bincount(train_d['y'])}")
    print(f"Val sequences (2024):        {val_d['X'].shape}, Class dist: {np.bincount(val_d['y'])}")
    print(f"Test sequences (2025):       {test_d['X'].shape}, Class dist: {np.bincount(test_d['y'])}")
