# AstraSentinel AI — Visual Gallery and Scientific Graphs

[← Project Home](../README.md) · [Architecture](ARCHITECTURE.md) · [Reports](REPORTING.md) · [Folder Tree](PROJECT_TREE.md)

Original, editable SVG illustrations developed for a polished space-AI research portfolio. Every image is stored as vector source under docs/gallery/. No image is a screenshot of operational spacecraft or NASA, ISRO or SpaceX systems.

**Scientific integrity:** Images show conceptual orbital geometry, modeled rocket results, and labeled synthetic telemetry or Kp examples. For reproducible *data* (not only illustrations), generate artifacts with the documented offline scientific pipeline.

## Panoramic GitHub Hero

![AstraSentinel AI space mission banner](gallery/astrasentinel-banner.svg)

A cinematic illustration of Earth, orbital path and satellite, designed as a recognizable repository header.

## 01 — 3D Orbital Geometry

![Inclined orbit schematic](gallery/orbital-geometry.svg)

The right-side latitude sweep is **schematic**, not an SGP4-propagated ground track. The actual backend returns computed orbital samples in /api/orbit.

## 02 — Satellite Health Intelligence

![AI anomaly detection visual](gallery/satellite-health-intelligence.svg)

The plotted peaks are artistic **synthetic example** anomalies, not real satellite observations and not numeric output from the backend ML detector.

## 03 — Solar Weather Observatory

![Solar and geomagnetic Kp concept](gallery/space-weather-observatory.svg)

The solar surface and the Kp bar values are illustrative. Live NOAA Kp values, when available, are fetched separately through the application.

## 04 — Rocket Flight Simulation Graph

![Rocket simulation graph](gallery/rocket-flight-analysis.svg)

The altitude and speed curves reproduce the default educational 1D rocket-simulator algorithm. Both are **display-scaled separately** to share a visual panel. The numeric metrics are simulated, not actual launch observations, and the plot is not flight certified.

## 05 — Earth's Atmospheric Layers

![Atmospheric density explorer](gallery/atmospheric-layers.svg)

The layer bands are an artistic visual analogy rather than geophysical heights drawn to scale. The density curve reflects a single 8500-meter exponential scale-height relationship, not a validated atmosphere model.

## 06 — Data Science Graph Collection

![Exponential-density and synthetic telemetry chart](gallery/scientific-graphs.svg)

Left: mathematical exponential-density relationship. Right: illustrative synthetic measurement spikes, not actual spacecraft measurements.

## 07 — Mission Dashboard Visual Design

![AstraSentinel user-interface concept](gallery/mission-control-ui-concept.svg)

Original mockup of the mission dashboard interface. This is **not a screenshot** of an actual browser session. The production-buildable React frontend lives in the frontend folder.

## More Original 3D-Style Engineering Diagrams

![Isometric system architecture](images/system-architecture-3d.svg)

![Educational rocket physics poster](images/rocket-physics-3d.svg)

![Original orbital digital twin](images/orbit-digital-twin.svg)

## Data-driven reports

Generate reproducible machine-readable simulation CSVs, JSON and an original rocket graph from the Python scientific engines:

~~~bash
python -m pip install -e '.[dev]'
python -m scripts.generate_demo_artifacts --output artifacts/reports
~~~

GitHub Actions also exposes these outputs as the downloadable artifact named astrasentinel-scientific-demo on successful workflow runs.

**Disclosure:** These SVG diagrams are original educational artwork. Do not describe them as space-agency imagery, a real solar flare observation, a measured satellite orbit map, or operational spacecraft health data.
