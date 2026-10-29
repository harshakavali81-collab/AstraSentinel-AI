# 🛰️ AstraSentinel AI

**An end-to-end aerospace AI/ML portfolio project: public orbital data + public space-weather observations + seeded telemetry ML + educational rocket simulation.**

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![AstraSentinel AI original panoramic space mission banner](<docs/gallery/astrasentinel-banner.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.


**Eight original, editable SVG pictures and graphs**, committed directly to this GitHub repository. Conceptual graphics are not real flight data or screenshots of an operational mission.

| 3D Orbital Science | Satellite Health AI |
|:---:|:---:|
| [![Orbital diagram](docs/gallery/orbital-geometry.svg)](docs/gallery/orbital-geometry.svg) | [![AI telemetry visualization](docs/gallery/satellite-health-intelligence.svg)](docs/gallery/satellite-health-intelligence.svg) |
| [Orbital geometry](docs/gallery/orbital-geometry.svg) | [Anomaly detection illustration](docs/gallery/satellite-health-intelligence.svg) |

| Space Weather | Rocket Trajectory Graph |
|:---:|:---:|
| [![Solar weather illustration](docs/gallery/space-weather-observatory.svg)](docs/gallery/space-weather-observatory.svg) | [![Rocket analysis curves](docs/gallery/rocket-flight-analysis.svg)](docs/gallery/rocket-flight-analysis.svg) |
| [Sun and Kp example](docs/gallery/space-weather-observatory.svg) | [Numerical rocket simulation](docs/gallery/rocket-flight-analysis.svg) |

| Earth's Atmospheric Layers | Mission Control Design |
|:---:|:---:|
| [![Atmospheric science](docs/gallery/atmospheric-layers.svg)](docs/gallery/atmospheric-layers.svg) | [![Mission control interface concept](docs/gallery/mission-control-ui-concept.svg)](docs/gallery/mission-control-ui-concept.svg) |
| [Atmospheric density](docs/gallery/atmospheric-layers.svg) | [Dashboard visual concept](docs/gallery/mission-control-ui-concept.svg) |

[**Explore all eight images, scientific graphs, and image explanations →**](docs/VISUAL_GALLERY.md)


## Live Link / Demo

Run the local demo using the setup guide below. No public deployment URL has been verified for this documentation update.

## Key Features

| Module | Functionality | Disclosure |
|---|---|---|
| Satellite data explorer | Fetch ISS (NORAD 25544) public CelesTrak TLE, show provenance | CelesTrak cached for two hours; offline historical demo |
| Interactive 3D orbit and ground track | SGP4 propagation, 121 samples, 3D Earth orbit and computed latitude/longitude chart with dateline breaks | Simplified TEME-to-ECEF approximation, no precision geodetic basemap |
| Space-weather observations | NOAA SWPC Kp data, timeline, storm threshold and freshness | Supports 2026 JSON shape, labeled fallback |
| Satellite Health ML | Seeded telemetry, IsolationForest, artificial fault injection, z-score diagnostics | Synthetic-only training and evaluation |
| Rocket Lab | 1D variable-mass ascent with gravity, density, thrust and drag | Educational numerical simulation |
| Rocket Scenario Comparison | Parameter sweeps comparing thrust, propellant, drag and density | Bounded reproducible experiments with chart and CSV/JSON export |
| Atmospheric Density Lab | Adjustable exponential density profile with logarithmic visualization | Simplified reference atmosphere, not empirical validation |
| Research Report Export | Download mission JSON and orbital, rocket and synthetic telemetry CSVs | Source-attributed snapshots; offline SVG/CSV/JSON generator |
| Mission dashboard | React/Vite, react-three-fiber/Three.js, Recharts, responsive styles | Served via nginx/Docker or Vite |
| API and verification | FastAPI endpoints, bounded request validation, pytest, GitHub Actions | Offline deterministic tests |

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![React](https://img.shields.io/badge/React-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

### Docker Compose

Requires Docker Desktop / Docker Engine with Compose.

~~~bash
git clone https://github.com/harshakavali81-collab/AstraSentinel-AI.git
cd AstraSentinel-AI
docker compose up --build
~~~

**Dashboard:** http://localhost:3000

**Swagger API:** http://localhost:8000/docs

**Backend health:** http://localhost:8000/api/health

**Private backend staging:** Use the dedicated docker-compose.private.yml file with ASTRA_OFFLINE=1 to bind the frontend only on 127.0.0.1:3000 and keep the backend private. See [deployment security guidance](docs/DEPLOYMENT.md). A trusted authenticated HTTPS edge is still required before any public deployment.

### One-container deployable web app

The complete **React mission dashboard and Python FastAPI API** can now run from a single image, using [Dockerfile.standalone](Dockerfile.standalone) and [backend/standalone.py](backend/standalone.py). This removes the requirement for a two-service Docker deployment on hosting providers.

~~~bash
docker compose -f docker-compose.standalone.yml up --build
~~~

Open **http://localhost:8080** for the real React dashboard and **http://localhost:8080/docs** for the actual Python API. The standalone demo defaults to historically labeled offline orbital/weather sources and synthetic satellite telemetry. It runs the original simulation and ML code, not mocked API responses.

**Optional reviewer login:** Set `ASTRA_DEMO_AUTH=1`, `ASTRA_DEMO_USER` and `ASTRA_DEMO_PASSWORD` through your host's secret environment variables to require HTTP Basic credentials on the standalone dashboard and API. Only use it behind HTTPS. The public health endpoint remains unprotected for platform readiness checks; it exposes no sensitive data.

Deployment manifests: [Render Blueprint](render.yaml) | [Railway IaC](.railway/railway.ts) | [Hosting guide](docs/DEPLOYMENT.md). Connecting your own hosting account and configuring a protected HTTPS deployment is still required before sharing an Internet URL. Static GitHub Pages does not run Python.

### Run directly with Python and Node.js

Requirements: Python 3.11+, Node 22+ and npm.

Terminal 1 (backend):

~~~bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m uvicorn backend.main:app --reload
~~~

Terminal 2 (frontend):

~~~bash
cd frontend
npm install
npm run dev
~~~

Then open **http://localhost:5173**. Vite proxies API requests to localhost:8000.

For a **network-independent demo**, set ASTRA_OFFLINE=1 in your backend environment. Docker users can run **ASTRA_OFFLINE=1 docker compose up --build** (PowerShell: set **$env:ASTRA_OFFLINE="1"** first) to enable deterministic offline simulation. Offline orbital data are an illustrative 2024 element pair, and weather charts use *synthetic historical example values*; both are clearly labeled.

## Challenges & Solutions

**Repository organization:** this project uses `src/`, `backend/`, `frontend/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

<div align="center">


### 3D Space Mission Digital Twin · Satellite Anomaly Intelligence · Rocket Physics

**An end-to-end aerospace AI/ML portfolio project: public orbital data + public space-weather observations + seeded telemetry ML + educational rocket simulation.**

[](https://github.com/harshakavali81-collab/AstraSentinel-AI/actions/workflows/ci.yml)





[Portfolio Website](docs/index.html) | [Visual Gallery](docs/VISUAL_GALLERY.md) | [Quick Start](#-quick-start) | [3D Diagrams](#-project-architecture) | [Project Tree](docs/PROJECT_TREE.md) | [API](docs/API_REFERENCE.md) | [Interview Guide](docs/INTERVIEW_GUIDE.md)

</div>



> **Important:** Orbital elements and geomagnetic readings are fetched from public sources when available. **All satellite health telemetry is synthetic**. The rocket and atmospheric simulators are simplified educational models, **not real-flight design tools**. The globe's geographical shapes are artistic, not a precision Earth map. No NASA, ISRO or SpaceX affiliation or private spacecraft data access is claimed.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/AstraSentinel-AI/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

See [LICENSE](LICENSE) for the existing terms.
