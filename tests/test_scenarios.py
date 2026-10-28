"""Physics experiments are deterministic, bounded and fully labeled as synthetic."""
import math
import pytest

from astrasentinel.rocket import RocketConfig
from astrasentinel.scenarios import PARAMETERS, compare_scenarios


def test_rocket_parameter_sweep_is_deterministic():
    a = compare_scenarios("thrust_n", [25000.0, 30000.0, 35000.0])
    b = compare_scenarios("thrust_n", [25000.0, 30000.0, 35000.0])
    assert a == b
    assert a["mode"] == "deterministic_educational_parameter_study"
    assert len(a["scenarios"]) == 3
    assert all(2 <= len(s["curve"]) <= 181 for s in a["scenarios"])
    assert all(math.isfinite(pt["altitude_km"]) for s in a["scenarios"]
               for pt in s["curve"])
    assert "no uncertainty analysis" in a["disclaimer"].lower()


def test_thrust_sweep_has_expected_direction_in_default_educational_case():
    result = compare_scenarios("thrust_n", [25000.0, 35000.0])
    low, high = result["scenarios"]
    assert high["metrics"]["apogee_km"] > low["metrics"]["apogee_km"]
    assert result["parameter_unit"] == "N"


def test_air_density_sweep_has_expected_direction():
    result = compare_scenarios("density_multiplier", [0.5, 1.0, 2.0])
    apogees = [s["metrics"]["apogee_km"] for s in result["scenarios"]]
    assert apogees[0] > apogees[1] > apogees[2]


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_sweep_rejects_non_finite_values(value):
    with pytest.raises(ValueError):
        compare_scenarios("thrust_n", [30000, value])


def test_sweep_rejects_duplicates_unsupported_and_limits():
    with pytest.raises(ValueError, match="unique"):
        compare_scenarios("thrust_n", [30000, 30000])
    with pytest.raises(ValueError, match="Unsupported"):
        compare_scenarios("unknown", [1, 2])
    with pytest.raises(ValueError):
        compare_scenarios("thrust_n", list(range(8)))
    with pytest.raises(ValueError):
        compare_scenarios("density_multiplier", [0.0, 1.0])
    with pytest.raises(ValueError):
        compare_scenarios("thrust_n", [20000, 23000],
                          RocketConfig(dt_s=0.0))


def test_every_supported_parameter_has_valid_unit():
    assert all(unit and low < high for unit, low, high in PARAMETERS.values())
