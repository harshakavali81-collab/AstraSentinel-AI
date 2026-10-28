# Mission Report and Reproducible Scientific Artifacts

[Project home](../README.md) · [API](API_REFERENCE.md) · [Test Plan](TEST_PLAN.md)

## Why there are two export workflows

1. **Interactive dashboard exports:** Mission Overview includes buttons for a consolidated JSON research report plus orbital, telemetry and rocket CSV files. Orbit CSV records contain explicit source/coordinate-frame columns; telemetry CSV includes the synthetic-injection flags. The JSON report reflects the server's current source provenance. The rocket export on Mission Overview uses the **default preview scenario**, not previously adjusted inputs on a separate Rocket Lab page.
2. **Deterministic offline report generator:** A Python command builds a fully reproducible snapshot and scientific data figures using the illustrative 2024 TLE, synthetic NOAA example points, synthetic telemetry, and the educational rocket model. It does not access public data services and must never be represented as live observations.

## Generate reports and graphs

Prerequisite: install project dependencies with pip install -e '.[dev]' from the repository root.

~~~bash
python -m scripts.generate_demo_artifacts --output artifacts/reports
~~~

The command produces **15 reproducible offline files**:

| Output | Contents |
|---|---|
| mission_snapshot_demo.json | Complete mission snapshot, scientific configuration, data sources, synthetic model metrics, limitations |
| orbit_track_demo.csv | Historical demo orbit positions, time and approximate Earth coordinates |
| satellite_telemetry_demo.csv | Synthetic sensor readings, injected labels, anomaly scores and explanations |
| rocket_trajectory_demo.csv | Numerical rocket altitude, velocity, acceleration, mass and dynamic pressure across time |
| rocket_ascent_demo.svg | Original data-driven vector graph of the simulated rocket altitude curve |
| orbit_altitude_demo.svg | Historical demo orbit's estimated altitude across the sampled period |
| orbit_latitude_demo.svg | Historical demo orbit's approximate latitude sweep |
| space_weather_kp_demo.svg | Synthetic historical Kp index series; **not** current NOAA observations |
| telemetry_temperature_demo.svg | Seeded synthetic subsystem temperature time series |
| telemetry_voltage_demo.svg | Seeded synthetic battery-voltage time series |
| rocket_velocity_demo.svg | Vertical velocity computed by the 1D educational integrator |
| rocket_dynamic_pressure_demo.svg | Dynamic pressure computed from the 1D rocket and exponential atmosphere |
| atmosphere_density_demo.svg | Exponential air density at 0–100 km, not a standard atmosphere |
| rocket_thrust_sensitivity_demo.csv | Actual model output for 25, 30, 35 and 40 kN default rocket experiment |
| rocket_thrust_sensitivity_demo.svg | Data-driven thrust versus apogee chart for the same one-factor study |

![Example 3D-style rocket physics](images/rocket-physics-3d.svg)

GitHub Actions additionally runs this command after the Python tests and uploads these files as a **30-day downloadable Actions artifact named astrasentinel-scientific-demo**. Use the [Actions tab](https://github.com/harshakavali81-collab/AstraSentinel-AI/actions/workflows/ci.yml), select a successful workflow run and open the artifact section to retrieve them. Workflow artifacts are not persisted forever; they can always be regenerated locally.

## Real dashboard screenshots

The CI full-stack job also drives the actual application using headless Chromium. It records **Mission Overview, Rocket Scenario Comparison and Rocket Lab** screenshots, checks scenario inputs and downloaded CSV content, and uploads the screenshots and traces as the separate **astrasentinel-browser-e2e** GitHub Actions artifact (30-day retention). These are browser captures, not the conceptual SVG illustrations in the repository gallery.

## JSON report fields

The REST route **GET /api/mission/report** gives a source-attributed report with:

- UTC creation timestamp and schema version.
- Satellite name/NORAD ID, TLE source and age, status, reference-frame explanation, period and inclination.
- NOAA planetary Kp source/status and observation age.
- Synthetic telemetry model details, flags, evaluation precision, recall and false alarm rate.
- Default illustrative rocket scenario, apogee/velocity/dynamic-pressure metrics and numerical assumptions.
- Explicit limitations forbidding operational interpretation.

Reports are **not** engineering certification or real spacecraft diagnostics.

## Reproducibility checks

The integration tests generate the offline dataset twice, compare bytes for all 15 outputs, verify CSV sizes and verify science-limitation disclosures. The fixed report timestamp used by the reproducible fixture is historical; the interactive API returns the current report creation timestamp.

Use report files in job portfolios with visible **SIMULATED / DEMO** labels.
