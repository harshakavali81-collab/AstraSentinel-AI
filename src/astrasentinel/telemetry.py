"""IsolationForest trained exclusively on seeded synthetic satellite telemetry."""
from __future__ import annotations

from functools import lru_cache
from datetime import datetime, timedelta, timezone
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, confusion_matrix

FEATURES = ["battery_voltage_v", "temperature_c", "bus_current_a", "attitude_error_deg"]


def normal_samples(size: int, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    load = rng.normal(0, 1, size)
    return np.column_stack([
        28.0 - 0.17 * load + rng.normal(0, 0.23, size),
        21.5 + 1.8 * load + rng.normal(0, 1.3, size),
        2.8 + 0.38 * load + rng.normal(0, 0.14, size),
        np.maximum(0, rng.normal(0.55, 0.2, size)),
    ])


def inject_anomalies(x: np.ndarray, indices: np.ndarray) -> np.ndarray:
    result = x.copy()
    for i, idx in enumerate(indices):
        channel = i % 4
        result[idx, channel] += [-5.8, 25.0, 3.5, 7.0][channel]
    return result


@lru_cache(maxsize=1)
def trained_model() -> tuple[IsolationForest, np.ndarray, np.ndarray]:
    train = normal_samples(1800, seed=42)
    model = IsolationForest(n_estimators=120, contamination=0.035,
                            max_samples=256, random_state=42, n_jobs=1)
    model.fit(train)
    return model, train.mean(axis=0), train.std(axis=0).clip(min=1e-6)


def score_matrix(matrix: np.ndarray) -> dict:
    model, means, scales = trained_model()
    x = np.asarray(matrix, dtype=float)
    if x.ndim != 2 or x.shape[1] != 4 or not np.isfinite(x).all():
        raise ValueError("Expected finite N x 4 telemetry values")
    labels = model.predict(x) == -1
    raw = -model.decision_function(x)  # positive suggests more anomalous
    z = abs((x - means) / scales)
    rows = []
    for i, item in enumerate(x):
        lead = int(np.argmax(z[i]))
        rows.append({
            "measurements": {feature: round(float(item[j]), 3)
                             for j, feature in enumerate(FEATURES)},
            "anomaly": bool(labels[i]),
            "anomaly_score": round(float(raw[i]), 4),
            "leading_deviation": FEATURES[lead],
            "deviation_z": round(float(z[i, lead]), 2),
        })
    return {"rows": rows, "score_definition": "-IsolationForest.decision_function;"
            " positive is anomalous, not a probability"}


def evaluation() -> dict:
    x = normal_samples(420, seed=77)
    indices = np.arange(12, 420, 21)
    x = inject_anomalies(x, indices)
    truth = np.zeros(len(x), dtype=bool)
    truth[indices] = True
    model, _, _ = trained_model()
    pred = model.predict(x) == -1
    tn, fp, fn, tp = confusion_matrix(truth, pred, labels=[False, True]).ravel()
    return {
        "label_source": "controlled_synthetic_injections",
        "test_samples": len(x), "anomaly_samples": int(truth.sum()),
        "precision": round(float(precision_score(truth, pred, zero_division=0)), 3),
        "recall": round(float(recall_score(truth, pred, zero_division=0)), 3),
        "false_alarm_rate": round(float(fp / max(1, fp + tn)), 3),
        "confusion_matrix": {"tp": int(tp), "tn": int(tn), "fp": int(fp), "fn": int(fn)},
        "model": "IsolationForest", "training_samples": 1800,
        "seed": 42, "features": FEATURES,
    }


def telemetry_series() -> dict:
    n = 144
    x = normal_samples(n, seed=109)
    indices = np.array([16, 43, 71, 100, 129])
    x = inject_anomalies(x, indices)
    result = score_matrix(x)
    start = datetime(2024, 3, 7, tzinfo=timezone.utc)
    for i, row in enumerate(result["rows"]):
        row["time"] = (start + timedelta(minutes=i * 4)).isoformat()
        row["synthetic_injected"] = bool(i in indices)
    return {
        "source": "synthetic_demo_telemetry", "live_spacecraft_telemetry": False,
        "feature_units": {"battery_voltage_v": "V", "temperature_c": "C",
                          "bus_current_a": "A", "attitude_error_deg": "deg"},
        "records": result["rows"], "model_metrics": evaluation(),
        "score_definition": result["score_definition"],
    }
