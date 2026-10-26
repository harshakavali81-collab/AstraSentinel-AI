"""Generate reproducible, network-free machine-readable reports and an original plot.

Usage:
    python -m scripts.generate_demo_artifacts --output artifacts/reports
All values are explicitly DEMO / SIMULATED. No outside HTTP calls.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from astrasentinel.ingestion import satellite_elements, space_weather
from astrasentinel.orbit import propagate
from astrasentinel.telemetry import telemetry_series
from astrasentinel.rocket import simulate
from astrasentinel.reporting import build_mission_report


def save_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("Expected at least one CSV row")
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def science_plot_svg(
    points: list[dict], title: str, x_key: str, y_key: str,
    width: int = 1040, height: int = 540,
) -> str:
    """Build a compact original SVG chart with units taken from explicit input labels."""
    if len(points) < 2:
        raise ValueError("Need at least two plot points")
    left, top, plot_width, plot_height = 95, 140, width - 150, height - 225
    xs = [float(row[x_key]) for row in points]
    ys = [float(row[y_key]) for row in points]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(0.0, min(ys)), max(ys)
    if x1 == x0:
        raise ValueError("X-axis needs more than one time")
    if y1 == y0:
        y1 = y0 + 1
    coords = []
    for x, y in zip(xs, ys):
        px = left + plot_width * (x - x0) / (x1 - x0)
        py = top + plot_height * (1 - (y - y0) / (y1 - y0))
        coords.append(f"{px:.1f},{py:.1f}")
    line = " ".join(coords)
    grid = []
    labels = []
    for i in range(6):
        py = top + i * plot_height / 5
        value = y1 - i * (y1 - y0) / 5
        grid.append(f'<line x1="{left}" y1="{py:.1f}" x2="{left + plot_width}" '
                    f'y2="{py:.1f}" stroke="#24455a" stroke-dasharray="4 8"/>')
        labels.append(f'<text x="{left - 15}" y="{py + 4:.1f}" '
                      f'text-anchor="end" font-size="12" fill="#afc8d7">{value:.2f}</text>')
    safe_title = escape(title)
    safe_x = escape(x_key.replace("_", " "))
    safe_y = escape(y_key.replace("_", " "))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"
role="img" aria-label="{safe_title} — generated offline educational simulation">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop stop-color="#12344d"/><stop offset="1" stop-color="#061120"/>
</linearGradient></defs>
<rect width="{width}" height="{height}" rx="23" fill="url(#bg)"/>
<text x="{left}" y="62" fill="#76edd2" font-family="Arial" font-size="14" letter-spacing="3">ASTRASENTINEL AI / GENERATED SCIENCE GRAPH</text>
<text x="{left}" y="103" fill="#e9fbff" font-family="Arial" font-weight="bold" font-size="30">{safe_title}</text>
{''.join(grid)}{''.join(labels)}
<polyline fill="none" stroke="#76eed5" stroke-width="3.5" stroke-linejoin="round" points="{line}"/>
<text x="{left + plot_width / 2:.1f}" y="{height-57}" text-anchor="middle" fill="#afc8d7" font-size="16" font-family="Arial">{safe_x}</text>
<text x="{left}" y="{height-22}" fill="#7599af" font-family="Arial" font-size="12">{safe_y} · EDUCATIONAL MODEL · NOT REAL FLIGHT DATA</text>
</svg>'''


def generate(output: Path) -> list[Path]:
    """Create fixed-epoch demo data, so artifact byte content is reproducible."""
    os.environ["ASTRA_OFFLINE"] = "1"
    output.mkdir(parents=True, exist_ok=True)
    orbit = propagate(satellite_elements())
    weather = space_weather()
    tele = telemetry_series()
    rocket = simulate()
    report = build_mission_report(
        orbit, weather, tele, rocket,
        generated_at=datetime(2024, 3, 7, tzinfo=timezone.utc),
    )
    files = {
        "mission_snapshot_demo.json": json.dumps(report, indent=2, sort_keys=True) + "\n",
        "rocket_ascent_demo.svg": science_plot_svg(
            rocket["points"], "Rocket vertical ascent", "time_s", "altitude_km",
        ),
    }
    for name, content in files.items():
        (output / name).write_text(content, encoding="utf-8")
    save_csv(output / "rocket_trajectory_demo.csv", rocket["points"])
    save_csv(output / "orbit_track_demo.csv", [
        {**{k: row[k] for k in ("time", "altitude_km", "latitude_deg", "longitude_deg")},
         **{f"ecef_{axis}_km": row["ecef_km"][idx] for idx, axis in enumerate("xyz")}}
        for row in orbit["points"]
    ])
    save_csv(output / "satellite_telemetry_demo.csv", [
        {
            "time": row["time"], **row["measurements"], "anomaly": row["anomaly"],
            "anomaly_score": row["anomaly_score"],
            "leading_deviation": row["leading_deviation"],
            "synthetic_injected": row["synthetic_injected"],
        }
        for row in tele["records"]
    ])
    return sorted(output.iterdir())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/reports"))
    args = parser.parse_args()
    for path in generate(args.output):
        print(path)


if __name__ == "__main__":
    main()
