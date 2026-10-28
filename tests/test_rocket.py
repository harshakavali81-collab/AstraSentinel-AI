import math
import pytest
from astrasentinel.atmosphere import density, drag_force
from astrasentinel.rocket import RocketConfig, simulate, gravity, G0

def test_density_decreases_with_altitude():
    assert density(0) == pytest.approx(1.225)
    assert density(10000) < density(5000) < density(0)
    assert density(40000) > 0

def test_drag_opposes_velocity():
    assert drag_force(0, 100, 0.4, 1) < 0
    assert drag_force(0, -100, 0.4, 1) > 0
    assert drag_force(0, 0, 0.4, 1) == 0

def test_gravity_falls_with_height():
    assert gravity(0) == pytest.approx(G0)
    assert gravity(200000) < gravity(0)

def test_finite_nonnegative_rocket_trajectory():
    result = simulate()
    assert result['metrics']['apogee_km'] > 1
    assert result['metrics']['peak_velocity_m_s'] > 0
    assert all(p['altitude_km'] >= 0 and math.isfinite(p['velocity_m_s'])
               for p in result['points'])
    assert min(p['mass_kg'] for p in result['points']) >= result['configuration']['dry_mass_kg']

def test_more_air_density_reduces_apogee():
    a = simulate(RocketConfig(density_multiplier=0.6))
    b = simulate(RocketConfig(density_multiplier=2.0))
    assert a['metrics']['apogee_km'] > b['metrics']['apogee_km']

def test_bad_rocket_parameter_rejected():
    with pytest.raises(ValueError):
        simulate(RocketConfig(dry_mass_kg=-1))
    with pytest.raises(ValueError):
        simulate(RocketConfig(dt_s=0))


def test_non_integer_burn_boundary_splits_numerical_step():
    config = RocketConfig(burn_time_s=60.15, dt_s=0.2, duration_s=95)
    points = simulate(config)['points']
    at_burnout = [p for p in points if abs(p['time_s'] - 60.15) < 1e-7]
    assert len(at_burnout) == 1
    assert at_burnout[0]['mass_kg'] == pytest.approx(config.dry_mass_kg)
    assert at_burnout[0]['acceleration_m_s2'] < 0  # coast: drag plus gravity


def test_rocket_step_size_sanity_check():
    fine = simulate(RocketConfig(dt_s=0.1))['metrics']['apogee_km']
    standard = simulate(RocketConfig(dt_s=0.2))['metrics']['apogee_km']
    assert abs(fine - standard) / max(fine, 0.001) < 0.1
