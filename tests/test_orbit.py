import math
import pytest
from datetime import datetime, timezone
from astrasentinel.orbit import EARTH_RADIUS_KM, gmst_radians, teme_to_ecef, propagate
from astrasentinel.ingestion import satellite_elements

def test_rotated_position_preserves_radius():
    r = (6790, 130, 70)
    v = teme_to_ecef(r, 2461000.0)
    assert math.sqrt(sum(z*z for z in v)) == pytest.approx(math.sqrt(sum(z*z for z in r)))

def test_gmst_stays_between_zero_and_two_pi():
    assert 0 <= gmst_radians(2461000.0) < 2 * math.pi

def test_sgp4_iss_reference_epoch_is_low_earth_orbit():
    result = propagate(satellite_elements(), samples=13, span_minutes=10)
    assert len(result['points']) == 13
    assert 200 < result['points'][6]['altitude_km'] < 600
    assert 80 < result['period_minutes'] < 110
    assert 45 < result['inclination_deg'] < 60
    assert result['status'] == 'demo'
    assert result['elements_age_hours'] > 0

def test_demo_is_centered_at_historical_epoch_not_today():
    result = propagate(satellite_elements(), samples=3)
    center = datetime.fromisoformat(result['points'][1]['time'])
    epoch = datetime.fromisoformat(result['epoch'])
    assert abs((center - epoch).total_seconds()) < 0.1

def test_reject_unbounded_samples():
    with pytest.raises(ValueError):
        propagate(satellite_elements(), samples=5000)
