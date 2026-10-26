import numpy as np
import pytest
from astrasentinel.telemetry import FEATURES, normal_samples, score_matrix, telemetry_series, evaluation

def test_synthetic_samples_are_reproducible():
    assert np.array_equal(normal_samples(20), normal_samples(20))

def test_schema_contains_four_features_and_events():
    data = telemetry_series()
    assert data['source'] == 'synthetic_demo_telemetry'
    assert not data['live_spacecraft_telemetry']
    assert len(data['records']) == 144
    assert set(data['records'][0]['measurements']) == set(FEATURES)
    assert any(record['anomaly'] for record in data['records'])

def test_extreme_telemetry_is_anomalous():
    result = score_matrix(np.array([[12.0, 90.0, 10.0, 20.0]]))['rows'][0]
    assert result['anomaly']
    assert result['anomaly_score'] > 0
    assert result['deviation_z'] > 5

def test_nonfinite_matrix_rejected():
    with pytest.raises(ValueError):
        score_matrix(np.array([[np.nan, 2, 3, 4]]))

def test_model_metrics_are_within_bounds():
    m = evaluation()
    assert m['label_source'] == 'controlled_synthetic_injections'
    assert 0 <= m['precision'] <= 1
    assert 0 <= m['recall'] <= 1
    assert m['confusion_matrix']['tp'] + m['confusion_matrix']['fn'] == m['anomaly_samples']
