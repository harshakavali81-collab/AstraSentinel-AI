# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`CONTRIBUTING.md`](<../CONTRIBUTING.md>)
- [`Dockerfile.standalone`](<../Dockerfile.standalone>)
- [`LICENSE`](<../LICENSE>)
- [`README.md`](<../README.md>)
- [`SECURITY.md`](<../SECURITY.md>)
- [`backend`](<../backend>)
- [`backend/Dockerfile`](<../backend/Dockerfile>)
- [`backend/__init__.py`](<../backend/__init__.py>)
- [`backend/basic_auth.py`](<../backend/basic_auth.py>)
- [`backend/main.py`](<../backend/main.py>)
- [`backend/standalone.py`](<../backend/standalone.py>)
- [`docker-compose.private.yml`](<../docker-compose.private.yml>)
- [`docker-compose.standalone.yml`](<../docker-compose.standalone.yml>)
- [`docker-compose.yml`](<../docker-compose.yml>)
- [`docs`](<../docs>)
- [`docs/API_REFERENCE.md`](<../docs/API_REFERENCE.md>)
- [`docs/ARCHITECTURE.md`](<../docs/ARCHITECTURE.md>)
- [`docs/DATA_SOURCES.md`](<../docs/DATA_SOURCES.md>)
- [`docs/DEMO_GUIDE.md`](<../docs/DEMO_GUIDE.md>)
- [`docs/DEPLOYMENT.md`](<../docs/DEPLOYMENT.md>)
- [`docs/INTERVIEW_GUIDE.md`](<../docs/INTERVIEW_GUIDE.md>)
- [`docs/LIMITATIONS.md`](<../docs/LIMITATIONS.md>)
- [`docs/MODEL_CARD.md`](<../docs/MODEL_CARD.md>)
- [`docs/PHYSICS.md`](<../docs/PHYSICS.md>)
- [`docs/PROJECT_TREE.md`](<../docs/PROJECT_TREE.md>)
- [`docs/REPORTING.md`](<../docs/REPORTING.md>)
- [`docs/SCENARIO_LAB.md`](<../docs/SCENARIO_LAB.md>)
- [`docs/TEST_PLAN.md`](<../docs/TEST_PLAN.md>)
- [`docs/VISUAL_GALLERY.md`](<../docs/VISUAL_GALLERY.md>)
- [`docs/gallery`](<../docs/gallery>)
- [`docs/gallery/astrasentinel-banner.svg`](<../docs/gallery/astrasentinel-banner.svg>)
- [`docs/gallery/atmospheric-layers.svg`](<../docs/gallery/atmospheric-layers.svg>)
- [`docs/gallery/mission-control-ui-concept.svg`](<../docs/gallery/mission-control-ui-concept.svg>)
- [`docs/gallery/orbital-geometry.svg`](<../docs/gallery/orbital-geometry.svg>)
- [`docs/gallery/rocket-flight-analysis.svg`](<../docs/gallery/rocket-flight-analysis.svg>)
- [`docs/gallery/satellite-health-intelligence.svg`](<../docs/gallery/satellite-health-intelligence.svg>)
- [`docs/gallery/scientific-graphs.svg`](<../docs/gallery/scientific-graphs.svg>)
- [`docs/gallery/space-weather-observatory.svg`](<../docs/gallery/space-weather-observatory.svg>)
- [`docs/images`](<../docs/images>)
- [`docs/images/orbit-digital-twin.svg`](<../docs/images/orbit-digital-twin.svg>)
- [`docs/images/rocket-physics-3d.svg`](<../docs/images/rocket-physics-3d.svg>)
- [`docs/images/system-architecture-3d.svg`](<../docs/images/system-architecture-3d.svg>)
- [`docs/index.html`](<../docs/index.html>)
- [`docs/landing.css`](<../docs/landing.css>)
- [`docs/science`](<../docs/science>)
- [`docs/science/README.md`](<../docs/science/README.md>)
- [`docs/science/atmosphere_density_demo.svg`](<../docs/science/atmosphere_density_demo.svg>)
- [`docs/science/mission_snapshot_demo.json`](<../docs/science/mission_snapshot_demo.json>)
- [`docs/science/orbit_altitude_demo.svg`](<../docs/science/orbit_altitude_demo.svg>)
- [`docs/science/orbit_latitude_demo.svg`](<../docs/science/orbit_latitude_demo.svg>)
- [`docs/science/orbit_track_demo.csv`](<../docs/science/orbit_track_demo.csv>)
- [`docs/science/rocket_ascent_demo.svg`](<../docs/science/rocket_ascent_demo.svg>)
- [`docs/science/rocket_dynamic_pressure_demo.svg`](<../docs/science/rocket_dynamic_pressure_demo.svg>)
- [`docs/science/rocket_thrust_sensitivity_demo.csv`](<../docs/science/rocket_thrust_sensitivity_demo.csv>)
- [`docs/science/rocket_thrust_sensitivity_demo.svg`](<../docs/science/rocket_thrust_sensitivity_demo.svg>)
- [`docs/science/rocket_trajectory_demo.csv`](<../docs/science/rocket_trajectory_demo.csv>)
- [`docs/science/rocket_velocity_demo.svg`](<../docs/science/rocket_velocity_demo.svg>)
- [`docs/science/satellite_telemetry_demo.csv`](<../docs/science/satellite_telemetry_demo.csv>)
- [`docs/science/space_weather_kp_demo.svg`](<../docs/science/space_weather_kp_demo.svg>)
- [`docs/science/telemetry_temperature_demo.svg`](<../docs/science/telemetry_temperature_demo.svg>)
- [`docs/science/telemetry_voltage_demo.svg`](<../docs/science/telemetry_voltage_demo.svg>)
- [`docs/screenshots`](<../docs/screenshots>)
- [`docs/screenshots/01-mission-overview.png`](<../docs/screenshots/01-mission-overview.png>)
- [`docs/screenshots/02-rocket-comparison.png`](<../docs/screenshots/02-rocket-comparison.png>)
- [`docs/screenshots/03-rocket-lab.png`](<../docs/screenshots/03-rocket-lab.png>)
- [`docs/screenshots/04-orbit-ground-track.png`](<../docs/screenshots/04-orbit-ground-track.png>)
- [`docs/screenshots/README.md`](<../docs/screenshots/README.md>)
- [`frontend`](<../frontend>)
- [`frontend/Dockerfile`](<../frontend/Dockerfile>)
- [`frontend/e2e`](<../frontend/e2e>)
- [`frontend/e2e/mission.spec.js`](<../frontend/e2e/mission.spec.js>)
- [`frontend/index.html`](<../frontend/index.html>)
- [`frontend/nginx.conf`](<../frontend/nginx.conf>)
- [`frontend/package.json`](<../frontend/package.json>)
- [`frontend/playwright.config.js`](<../frontend/playwright.config.js>)
- [`frontend/src`](<../frontend/src>)
- [`frontend/src/App.jsx`](<../frontend/src/App.jsx>)
- [`frontend/src/AtmospherePage.jsx`](<../frontend/src/AtmospherePage.jsx>)
- [`frontend/src/GroundTrack.jsx`](<../frontend/src/GroundTrack.jsx>)
- [`frontend/src/MissionExportPanel.jsx`](<../frontend/src/MissionExportPanel.jsx>)
- [`frontend/src/OrbitGlobe.jsx`](<../frontend/src/OrbitGlobe.jsx>)
- [`frontend/src/ScenarioLab.jsx`](<../frontend/src/ScenarioLab.jsx>)
- [`frontend/src/api.js`](<../frontend/src/api.js>)
- [`frontend/src/groundTrack.js`](<../frontend/src/groundTrack.js>)
- [`frontend/src/main.jsx`](<../frontend/src/main.jsx>)
- [`frontend/src/scenarioCurves.js`](<../frontend/src/scenarioCurves.js>)
- [`frontend/src/styles.css`](<../frontend/src/styles.css>)
- [`frontend/tests`](<../frontend/tests>)
- [`frontend/tests/curves.test.mjs`](<../frontend/tests/curves.test.mjs>)
- [`frontend/tests/groundTrack.test.mjs`](<../frontend/tests/groundTrack.test.mjs>)
- [`frontend/vite.config.js`](<../frontend/vite.config.js>)
- [`pyproject.toml`](<../pyproject.toml>)
- [`render.yaml`](<../render.yaml>)
- [`scripts`](<../scripts>)
- [`scripts/__init__.py`](<../scripts/__init__.py>)
- [`scripts/generate_demo_artifacts.py`](<../scripts/generate_demo_artifacts.py>)
- [`src`](<../src>)
- [`src/astrasentinel`](<../src/astrasentinel>)
- [`src/astrasentinel/__init__.py`](<../src/astrasentinel/__init__.py>)
- [`src/astrasentinel/atmosphere.py`](<../src/astrasentinel/atmosphere.py>)
- [`src/astrasentinel/ingestion.py`](<../src/astrasentinel/ingestion.py>)
- [`src/astrasentinel/orbit.py`](<../src/astrasentinel/orbit.py>)
- [`src/astrasentinel/reporting.py`](<../src/astrasentinel/reporting.py>)
- [`src/astrasentinel/rocket.py`](<../src/astrasentinel/rocket.py>)
- [`src/astrasentinel/scenarios.py`](<../src/astrasentinel/scenarios.py>)
- [`src/astrasentinel/telemetry.py`](<../src/astrasentinel/telemetry.py>)
- [`tests`](<../tests>)
- [`tests/conftest.py`](<../tests/conftest.py>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_basic_auth.py`](<../tests/test_basic_auth.py>)
- [`tests/test_gallery.py`](<../tests/test_gallery.py>)
- [`tests/test_ingestion.py`](<../tests/test_ingestion.py>)
- [`tests/test_orbit.py`](<../tests/test_orbit.py>)
- [`tests/test_portfolio_site.py`](<../tests/test_portfolio_site.py>)
- [`tests/test_published_assets.py`](<../tests/test_published_assets.py>)
- [`tests/test_reporting.py`](<../tests/test_reporting.py>)
- [`tests/test_rocket.py`](<../tests/test_rocket.py>)
- [`tests/test_scenarios.py`](<../tests/test_scenarios.py>)
- [`tests/test_security_contracts.py`](<../tests/test_security_contracts.py>)
- [`tests/test_standalone_contract.py`](<../tests/test_standalone_contract.py>)
- [`tests/test_telemetry.py`](<../tests/test_telemetry.py>)
