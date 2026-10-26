# Model Card — Synthetic Satellite Health Anomaly Detection

[Project home](../README.md) · [Test plan](TEST_PLAN.md)

| Category | Specification |
|---|---|
| Model | scikit-learn IsolationForest |
| Inputs | battery_voltage_v, temperature_c, bus_current_a, attitude_error_deg |
| Normal training data | 1,800 seeded synthetic records, seed 42 |
| Trees | 120 |
| Contamination | 0.035 |
| Subsampling | max_samples=256 |
| Reproducibility | random_state=42, deterministic generator |
| Evaluation | 420 separate seeded synthetic observations, controlled fault injection |
| Outputs | Anomaly flag; -decision_function anomaly score; largest feature z-deviation |
| Label provenance | Entirely artificial fault-injection labels; **not actual spacecraft anomalies** |

## Method

A latent synthetic load factor introduces correlation among voltage, current and temperature. The nominal dataset also adds independent noise and nonnegative attitude errors. The Isolation Forest trains on **only simulated normal samples**, without anomaly labels.

The evaluation sample uses an independent seed and inserts large artificial faults into selected feature channels (voltage, temperature, current and attitude). The backend calculates a confusion matrix, precision, recall and false alarm rate at runtime. These numbers summarize performance **only against this synthetic injection design**, not actual aerospace operational performance.

## Explainability

Predicted anomalies are accompanied by the most unusually standardized feature, measured in deviations from the synthetic training mean and standard deviation. The strongest z-deviation is a **descriptive diagnostic**, not a causal explanation. The anomaly score is the negative IsolationForest decision_function, with larger positive values indicating more unusual samples. It is not a calibrated probability of hardware failure.

## Appropriate and inappropriate usage

Appropriate: learning unsupervised modeling, reproducible data generation, numerical validation, REST model inference, error rates and interpretable dashboard displays.

Inappropriate: real-world spacecraft safety decisions, failure prediction claims, on-orbit anomaly alerts, predictive maintenance promises, causal diagnosis or mission probability estimates. Further work requires permitted labeled real telemetry, mission-domain expertise, threshold calibration, robustness checks and drift analysis.

## Reproducibility

The process trains in-memory the first time scoring is requested and caches the fitted model for that server process. This keeps the reference implementation simple and avoids untrusted pickle artifacts. Run the tests using the documented offline setup for repeatable behavior.
