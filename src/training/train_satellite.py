"""
train_satellite.py

Complete training and benchmarking pipeline for Module 2 (Satellite Drought Confirmation).
Compares 4 models:
  1. DOY-Aware Temporal Transformer (Proposed)
  2. Bidirectional LSTM (Deep Sequence Baseline)
  3. XGBoost (Tabular Baseline)
  4. Random Forest (Tabular Baseline)

Saves results to results/satellite_benchmark_results.csv
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score,
    f1_score, roc_auc_score, confusion_matrix
)
from sklearn.preprocessing import label_binarize

# Setup paths
import sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from data.satellite_dataset import build_satellite_sequences, SatellitePyTorchDataset
from models.satellite_transformer import DOYAwareTemporalTransformer
from models.satellite_baselines import SatelliteLSTM, extract_tabular_features

# Output directories
RESULTS_DIR = ROOT_DIR / "results"
MODELS_DIR = ROOT_DIR / "models" / "satellite"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using Compute Device: {DEVICE}")

def evaluate_predictions(y_true, y_pred, y_prob=None, model_name=""):
    acc = accuracy_score(y_true, y_pred)
    bacc = balanced_accuracy_score(y_true, y_pred)
    mf1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    hf1 = f1_score(y_true, y_pred, labels=[0], average="macro", zero_division=0)
    modf1 = f1_score(y_true, y_pred, labels=[1], average="macro", zero_division=0)
    sevf1 = f1_score(y_true, y_pred, labels=[2], average="macro", zero_division=0)

    roc = 0.0
    if y_prob is not None:
        try:
            yb = label_binarize(y_true, classes=[0, 1, 2])
            roc = roc_auc_score(yb, y_prob, multi_class="ovr", average="macro")
        except Exception:
            pass

    return {
        "Model": model_name,
        "Accuracy": round(acc, 4),
        "Balanced_Acc": round(bacc, 4),
        "Macro_F1": round(mf1, 4),
        "Healthy_F1": round(hf1, 4),
        "Moderate_F1": round(modf1, 4),
        "Severe_F1": round(sevf1, 4),
        "ROC_AUC": round(roc, 4)
    }

def train_neural_model(model, train_loader, val_loader, test_loader, class_weights, epochs=25, lr=5e-4):
    criterion = nn.CrossEntropyLoss(weight=class_weights.to(DEVICE))
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    best_val_f1 = -1.0
    best_weights = None

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for X_b, doy_b, y_b in train_loader:
            X_b, doy_b, y_b = X_b.to(DEVICE), doy_b.to(DEVICE), y_b.to(DEVICE)
            optimizer.zero_grad()
            logits = model(X_b, doy_b)
            loss = criterion(logits, y_b)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()
        scheduler.step()

        # Validation
        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for X_b, doy_b, y_b in val_loader:
                X_b, doy_b = X_b.to(DEVICE), doy_b.to(DEVICE)
                logits = model(X_b, doy_b)
                preds = logits.argmax(dim=-1).cpu().numpy()
                val_preds.extend(preds)
                val_targets.extend(y_b.numpy())

        val_f1 = f1_score(val_targets, val_preds, average="macro", zero_division=0)
        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            best_weights = {k: v.cpu().clone() for k, v in model.state_dict().items()}

    # Load best weights and evaluate on held-out test set
    model.load_state_dict(best_weights)
    model.to(DEVICE)
    model.eval()

    test_preds, test_probs, test_targets = [], [], []
    with torch.no_grad():
        for X_b, doy_b, y_b in test_loader:
            X_b, doy_b = X_b.to(DEVICE), doy_b.to(DEVICE)
            logits = model(X_b, doy_b)
            probs = torch.softmax(logits, dim=-1).cpu().numpy()
            preds = probs.argmax(axis=-1)
            test_probs.append(probs)
            test_preds.extend(preds)
            test_targets.extend(y_b.numpy())

    test_probs = np.concatenate(test_probs, axis=0)
    return np.array(test_targets), np.array(test_preds), test_probs

def main():
    print("=" * 70)
    print("   MODULE 2: SATELLITE DROUGHT CONFIRMATION — MODEL BENCHMARK   ")
    print("=" * 70)

    # 1. Build Sequences
    print("\n[Step 1/4] Constructing chronological multi-year sequences...")
    train_d, val_d, test_d = build_satellite_sequences()
    print(f"  Train: {train_d['X'].shape[0]} | Val: {val_d['X'].shape[0]} | Test: {test_d['X'].shape[0]}")

    # Compute balanced class weights for loss
    class_counts = np.bincount(train_d["y"], minlength=3)
    total_samples = len(train_d["y"])
    # Safe inverse frequency weights
    weights = [total_samples / (3.0 * max(c, 1)) for c in class_counts]
    class_weights_t = torch.tensor(weights, dtype=torch.float32)
    print(f"  Class counts (Train): {class_counts.tolist()}")
    print(f"  Inverse class weights: {[round(w, 2) for w in weights]}")

    # PyTorch DataLoaders
    train_loader = DataLoader(SatellitePyTorchDataset(train_d), batch_size=64, shuffle=True)
    val_loader   = DataLoader(SatellitePyTorchDataset(val_d), batch_size=128, shuffle=False)
    test_loader  = DataLoader(SatellitePyTorchDataset(test_d), batch_size=128, shuffle=False)

    results = []

    # -------------------------------------------------------------------------
    # Model 1: DOY-Aware Temporal Transformer (Proposed)
    # -------------------------------------------------------------------------
    print("\n[Step 2/4] Training DOY-Aware Temporal Transformer...")
    t0 = time.time()
    transformer = DOYAwareTemporalTransformer(
        input_dim=4, num_classes=3, d_model=64, nhead=4, num_layers=2, dropout=0.15
    ).to(DEVICE)

    y_test, pred_trans, prob_trans = train_neural_model(
        transformer, train_loader, val_loader, test_loader, class_weights_t, epochs=30, lr=6e-4
    )
    t_time = round(time.time() - t0, 1)

    res_trans = evaluate_predictions(y_test, pred_trans, prob_trans, "DOY-Aware Temporal Transformer")
    res_trans["Train_Time_s"] = t_time
    results.append(res_trans)
    torch.save(transformer.state_dict(), MODELS_DIR / "best_doy_transformer.pt")
    print(f"  --> Transformer Macro F1: {res_trans['Macro_F1']:.4f} | Severe F1: {res_trans['Severe_F1']:.4f} ({t_time}s)")

    # -------------------------------------------------------------------------
    # Model 2: Bidirectional LSTM
    # -------------------------------------------------------------------------
    print("\n[Step 3/4] Training Bidirectional LSTM Baseline...")
    t0 = time.time()
    bilstm = SatelliteLSTM(input_dim=4, hidden_dim=32, num_layers=2, num_classes=3, dropout=0.2).to(DEVICE)
    y_test, pred_lstm, prob_lstm = train_neural_model(
        bilstm, train_loader, val_loader, test_loader, class_weights_t, epochs=30, lr=8e-4
    )
    t_time = round(time.time() - t0, 1)

    res_lstm = evaluate_predictions(y_test, pred_lstm, prob_lstm, "Bidirectional LSTM")
    res_lstm["Train_Time_s"] = t_time
    results.append(res_lstm)
    torch.save(bilstm.state_dict(), MODELS_DIR / "best_satellite_lstm.pt")
    print(f"  --> BiLSTM Macro F1: {res_lstm['Macro_F1']:.4f} | Severe F1: {res_lstm['Severe_F1']:.4f} ({t_time}s)")

    # -------------------------------------------------------------------------
    # Models 3 & 4: Tabular Baselines (Random Forest & XGBoost)
    # -------------------------------------------------------------------------
    print("\n[Step 4/4] Training Tabular Baselines (Random Forest & XGBoost)...")
    X_tab_tr = extract_tabular_features(train_d["X"], train_d["doy"])
    X_tab_te = extract_tabular_features(test_d["X"], test_d["doy"])
    y_tr, y_te = train_d["y"], test_d["y"]

    # Random Forest
    t0 = time.time()
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, n_jobs=-1)
    rf.fit(X_tab_tr, y_tr)
    pred_rf = rf.predict(X_tab_te)
    prob_rf = rf.predict_proba(X_tab_te)
    t_time = round(time.time() - t0, 1)

    res_rf = evaluate_predictions(y_te, pred_rf, prob_rf, "Random Forest")
    res_rf["Train_Time_s"] = t_time
    results.append(res_rf)
    joblib.dump(rf, MODELS_DIR / "rf_satellite.joblib")
    print(f"  --> Random Forest Macro F1: {res_rf['Macro_F1']:.4f} | Severe F1: {res_rf['Severe_F1']:.4f} ({t_time}s)")

    # XGBoost
    t0 = time.time()
    xgb = XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.08, random_state=42, n_jobs=-1)
    xgb.fit(X_tab_tr, y_tr)
    pred_xgb = xgb.predict(X_tab_te)
    prob_xgb = xgb.predict_proba(X_tab_te)
    t_time = round(time.time() - t0, 1)

    res_xgb = evaluate_predictions(y_te, pred_xgb, prob_xgb, "XGBoost")
    res_xgb["Train_Time_s"] = t_time
    results.append(res_xgb)
    joblib.dump(xgb, MODELS_DIR / "xgb_satellite.joblib")
    print(f"  --> XGBoost Macro F1: {res_xgb['Macro_F1']:.4f} | Severe F1: {res_xgb['Severe_F1']:.4f} ({t_time}s)")

    # -------------------------------------------------------------------------
    # Save & Display Results Table
    # -------------------------------------------------------------------------
    df_results = pd.DataFrame(results)
    csv_out = RESULTS_DIR / "satellite_benchmark_results.csv"
    df_results.to_csv(csv_out, index=False)

    print("\n" + "=" * 80)
    print("   FINAL SATELLITE MODULE BENCHMARK RESULTS (TEST SET: KHARIF 2025)   ")
    print("=" * 80)
    print(df_results.to_string(index=False))
    print("=" * 80)
    print(f"\nSaved benchmark results to: {csv_out}")
    print(f"Saved trained models to: {MODELS_DIR}")

    # Confusion matrix for DOY Transformer
    cm = confusion_matrix(y_test, pred_trans)
    print("\nConfusion Matrix — DOY-Aware Temporal Transformer:")
    print("                   Pred Healthy | Pred Moderate | Pred Severe")
    print(f"True Healthy    :  {cm[0,0]:11d} |  {cm[0,1]:12d} |  {cm[0,2]:10d}")
    print(f"True Moderate   :  {cm[1,0]:11d} |  {cm[1,1]:12d} |  {cm[1,2]:10d}")
    print(f"True Severe     :  {cm[2,0]:11d} |  {cm[2,1]:12d} |  {cm[2,2]:10d}")

if __name__ == "__main__":
    main()
