"""
satellite_baselines.py

Baseline models for comparison against the DOY-Aware Temporal Transformer:
  1. SatelliteLSTM: Bidirectional LSTM
  2. Tabular Feature Extractor for Random Forest & XGBoost
"""
from __future__ import annotations
import numpy as np
import torch
import torch.nn as nn

class SatelliteLSTM(nn.Module):
    """Bidirectional LSTM with DOY feature concatenation."""
    def __init__(
        self,
        input_dim: int = 4,
        hidden_dim: int = 32,
        num_layers: int = 2,
        num_classes: int = 3,
        dropout: float = 0.2
    ):
        super().__init__()
        # Input: 4 spectral indices + 1 normalized DOY
        self.lstm = nn.LSTM(
            input_size=input_dim + 1,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        self.fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )

    def forward(self, x: torch.Tensor, doy: torch.Tensor) -> torch.Tensor:
        # Concatenate normalized DOY to input features
        doy_norm = (doy.float() / 365.25).unsqueeze(-1)  # (B, T, 1)
        x_cat = torch.cat([x, doy_norm], dim=-1)         # (B, T, 5)

        out, (hn, _) = self.lstm(x_cat)
        # Concatenate last forward and backward hidden states
        h_last = torch.cat([hn[-2], hn[-1]], dim=-1)
        return self.fc(h_last)


def extract_tabular_features(X: np.ndarray, doy: np.ndarray) -> np.ndarray:
    """
    Extracts summary statistics across the sequence window for tabular baselines.
    Features per spectral channel: [mean, std, min, max, last_val, delta]
    Output shape: (N, 4 * 6 + 2) = (N, 26)
    """
    N, T, F = X.shape
    features = []

    # Spectral channel statistics
    for f_idx in range(F):
        channel = X[:, :, f_idx]
        f_mean = np.mean(channel, axis=1, keepdims=True)
        f_std  = np.std(channel, axis=1, keepdims=True)
        f_min  = np.min(channel, axis=1, keepdims=True)
        f_max  = np.max(channel, axis=1, keepdims=True)
        f_last = channel[:, -1:]
        f_diff = channel[:, -1:] - channel[:, 0:1]  # overall trend
        features.extend([f_mean, f_std, f_min, f_max, f_last, f_diff])

    # DOY features: last observation DOY and seasonal sin/cos
    last_doy = doy[:, -1:]
    doy_sin = np.sin((last_doy / 365.25) * 2 * np.pi)
    doy_cos = np.cos((last_doy / 365.25) * 2 * np.pi)
    features.extend([doy_sin, doy_cos])

    return np.concatenate(features, axis=1).astype(np.float32)
