"""Verify committed screenshots and scientific charts, not conceptual image placeholders."""
from pathlib import Path
from xml.etree import ElementTree
import json

ROOT = Path(__file__).resolve().parents[1] / "docs"
SCREEN = ROOT / "screenshots"
SCI = ROOT / "science"
PICS = ("01-mission-overview.png", "02-rocket-comparison.png",
        "03-rocket-lab.png", "04-orbit-ground-track.png")
PLOTS = ("rocket_ascent_demo.svg", "orbit_altitude_demo.svg",
         "orbit_latitude_demo.svg", "space_weather_kp_demo.svg",
         "telemetry_temperature_demo.svg", "telemetry_voltage_demo.svg",
         "rocket_velocity_demo.svg", "rocket_dynamic_pressure_demo.svg",
         "atmosphere_density_demo.svg", "rocket_thrust_sensitivity_demo.svg")


def test_all_automated_browser_screenshots_are_real_png_files():
    for name in PICS:
        path = SCREEN / name
        assert path.is_file(), name
        assert path.stat().st_size > 4096
        with path.open("rb") as fp:
            assert fp.read(8) == b"\x89PNG\r\n\x1a\n"
    description = (SCREEN / "README.md").read_text().lower()
    assert "running offline" in description
    assert "synthetic" in description


def test_all_generated_svg_graphs_exist_and_parse_safely():
    for name in PLOTS:
        path = SCI / name
        assert path.is_file(), name
        data = path.read_text()
        assert len(data) > 300
        root = ElementTree.fromstring(data)
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
        assert "<script" not in data.lower()


def test_report_provenance_is_honest_and_datasets_are_committed():
    report = json.loads((SCI / "mission_snapshot_demo.json").read_text())
    assert report["mode"] == "educational_research_demonstration"
    assert report["telemetry_ai"]["live_spacecraft_telemetry"] is False
    assert report["satellite"]["orbit_status"] == "demo"
    assert report["space_weather"]["status"] == "demo"
    for name in ("orbit_track_demo.csv", "rocket_trajectory_demo.csv",
                 "satellite_telemetry_demo.csv", "rocket_thrust_sensitivity_demo.csv"):
        assert (SCI / name).is_file()
    assert "synthetic" in (SCI / "README.md").read_text().lower()
