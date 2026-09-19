"""
satellite_transformer.py

DOY-Aware Temporal Transformer for Satellite Drought Confirmation.
Key Innovations:
  1. Multi-spectral Input Projection (NDVI, NDMI, SAVI, VCI -> d_model)
  2. Sinusoidal Day-of-Year (DOY) Temporal Positional Encoding:
     Captures crop calendar seasonality and phenology (Kharif/Rabi cycles).
  3. Multi-Head Self-Attention for cross-timestep spectral interaction.
  4. Temporal Mean-Pooling + Imbalance-Aware Classification Head.
"""
from __future__ import annotations
import math
import torch
import torch.nn as nn

class SinusoidalDOYEmbedding(nn.Module):
    """Encodes calendar Day-of-Year (1-365) into d_model dimensional space."""
    def __init__(self, d_model: int):
        super().__init__()
        self.d_model = d_model
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        self.register_buffer("div_term", div_term)

    def forward(self, doy: torch.Tensor) -> torch.Tensor:
        """
        Args:
            doy: (B, T) LongTensor of Day-of-Year values [1, 365]
        Returns:
            pe: (B, T, d_model)
        """
        B, T = doy.shape
        pe = torch.zeros(B, T, self.d_model, device=doy.device)
        angles = (doy.float() / 365.25) * (2.0 * math.pi)  # (B, T)
        phase = angles.unsqueeze(-1) * self.div_term.unsqueeze(0).unsqueeze(0)  # (B, T, d_model//2)
        pe[:, :, 0::2] = torch.sin(phase)
        pe[:, :, 1::2] = torch.cos(phase[:, :, :self.d_model // 2])
        return pe


class DOYAwareTemporalTransformer(nn.Module):
    def __init__(
        self,
        input_dim: int = 4,        # NDVI, NDMI, SAVI, VCI
        num_classes: int = 3,      # Healthy (0), Moderate (1), Severe (2)
        d_model: int = 64,
        nhead: int = 4,
        num_layers: int = 2,
        dim_feedforward: int = 128,
        dropout: float = 0.15
    ):
        super().__init__()
        self.d_model = d_model

        # 1. Feature Projection
        self.input_proj = nn.Linear(input_dim, d_model)
        self.proj_norm = nn.LayerNorm(d_model)

        # 2. DOY Positional Encoding
        self.doy_embed = SinusoidalDOYEmbedding(d_model)
        self.dropout = nn.Dropout(dropout)

        # 3. Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation="gelu",
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # 4. Classification Head
        self.norm = nn.LayerNorm(d_model)
        self.classifier = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(32, num_classes)
        )

    def forward(self, x: torch.Tensor, doy: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x:   (B, T, 4) spectral features
            doy: (B, T) day of year integers
        Returns:
            logits: (B, num_classes)
        """
        # Project spectral indices
        h = self.input_proj(x)
        h = self.proj_norm(h)

        # Add calendar phenology embedding
        pe = self.doy_embed(doy)
        h = self.dropout(h + pe)

        # Self-attention over observation timesteps
        h = self.transformer(h)  # (B, T, d_model)

        # Global temporal mean pooling
        h_pool = h.mean(dim=1)   # (B, d_model)
        h_norm = self.norm(h_pool)

        # Predict drought class logits
        logits = self.classifier(h_norm)
        return logits


if __name__ == "__main__":
    B, T = 8, 12
    dummy_x = torch.randn(B, T, 4)
    dummy_doy = torch.randint(1, 365, (B, T))
    model = DOYAwareTemporalTransformer()
    out = model(dummy_x, dummy_doy)
    print("Model initialized successfully!")
    print(f"Input: {dummy_x.shape}, DOY: {dummy_doy.shape} -> Output: {out.shape}")
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total trainable parameters: {n_params:,}")
