import json
import csv
from datetime import datetime, timezone
import pytest

from astrasentinel.ingestion import satellite_elements, space_weather
from astrasentinel.orbit import propagate
from astrasentinel.rocket import simulate
from astrasentinel.telemetry import telemetry_series
from astrasentinel.reporting import build_mission_report
from scripts.generate_demo_artifacts import generate, science_plot_svg


def test_report_has_provenance_and_non_operational_disclosure():
    result = build_mission_report(
        propagate(satellite_elements(), samples=3), space_weather(),
        telemetry_series(), simulate(),
        generated_at=datetime(2024, 3, 7, tzinfo=timezone.utc))
    assert result["satellite"]["orbit_status"] == "demo"
    assert result["space_weather"]["status"] == "demo"
    assert result["telemetry_ai"]["live_spacecraft_telemetry"] is False
    assert len(result["limitations"]) >= 4
    assert "not failure probabilities" in " ".join(result["limitations"])


def test_empty_series_rejected():
    with pytest.raises(ValueError):
        build_mission_report({"points": []}, {}, {"records": []}, {"points": []})


def test_report_artifacts_are_reproducible(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    a = generate(first)
    b = generate(second)
    assert len(a) == len(b) == 15
    assert [p.name for p in a] == [p.name for p in b]
    for src, dst in zip(a, b):
        assert src.read_bytes() == dst.read_bytes(), src.name
    report = json.loads((first / "mission_snapshot_demo.json").read_text())
    assert report["mode"] == "educational_research_demonstration"
    with (first / "orbit_track_demo.csv").open(newline="") as f:
        assert len(list(csv.DictReader(f))) == 121
    with (first / "rocket_trajectory_demo.csv").open(newline="") as f:
        assert len(list(csv.DictReader(f))) > 100
    assert "<polyline" in (first / "rocket_ascent_demo.svg").read_text()
    with (first / "rocket_thrust_sensitivity_demo.csv").open(newline="") as f:
        cases = list(csv.DictReader(f))
        assert len(cases) == 4
        assert float(cases[0]["apogee_km"]) < float(cases[-1]["apogee_km"])
    assert "<polyline" in (first / "rocket_thrust_sensitivity_demo.svg").read_text()
    for plot in [
        "orbit_altitude_demo.svg", "orbit_latitude_demo.svg",
        "space_weather_kp_demo.svg", "telemetry_temperature_demo.svg",
        "telemetry_voltage_demo.svg", "rocket_velocity_demo.svg",
        "rocket_dynamic_pressure_demo.svg", "atmosphere_density_demo.svg",
    ]:
        assert "<polyline" in (first / plot).read_text(), plot


def test_generated_graph_needs_trajectory():
    with pytest.raises(ValueError):
        science_plot_svg([{"time_s": 0, "altitude_km": 0}],
                         "Rocket", "time_s", "altitude_km")
