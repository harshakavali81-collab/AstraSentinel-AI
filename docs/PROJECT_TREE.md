# Full Project Repository Tree

[Project home](../README.md)

~~~text
AstraSentinel-AI/
├── .github/
│   └── workflows/
│       └── ci.yml                 Python and frontend CI
├── backend/
│   ├── __init__.py
│   ├── Dockerfile
│   └── main.py                    FastAPI application
├── src/
│   └── astrasentinel/
│       ├── __init__.py
│       ├── ingestion.py           CelesTrak, NOAA, caching, fallback
│       ├── orbit.py               SGP4, TEME, approximate ECEF
│       ├── atmosphere.py          Exponential density and drag
│       ├── reporting.py           Source-attributed science snapshots
│       ├── scenarios.py           Bounded rocket sensitivity experiments
│       ├── rocket.py              Rocket mass, gravity and integration
│       └── telemetry.py           Synthetic ML anomaly detection
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── api.js
│       ├── App.jsx                Mission pages and charts
│       ├── ScenarioLab.jsx        One-factor rocket comparison and CSV export
│       ├── AtmospherePage.jsx     Atmosphere visualization and multiplier
│       ├── MissionExportPanel.jsx  JSON and CSV browser exports
│       ├── OrbitGlobe.jsx         Three.js Earth and orbit
│       └── styles.css
├── scripts/
│   ├── __init__.py
│   └── generate_demo_artifacts.py   Offline CSV/JSON/SVG builder
├── tests/
│   ├── conftest.py                No-network fixture
│   ├── test_ingestion.py
│   ├── test_orbit.py
│   ├── test_portfolio_site.py
│   ├── test_gallery.py
│   ├── test_scenarios.py
│   ├── test_rocket.py
│   ├── test_telemetry.py
│   └── test_reporting.py
│   └── test_api.py
├── docs/
│   ├── index.html             Portfolio landing page, Pages-ready
│   ├── landing.css            Mobile-responsive landing styles
│   ├── DEPLOYMENT.md          Hosting and security guide
│   ├── SCENARIO_LAB.md        Sensitivity experiments and modeling limits
│   ├── gallery/
│   │   ├── astrasentinel-banner.svg
│   │   ├── orbital-geometry.svg
│   │   ├── satellite-health-intelligence.svg
│   │   ├── space-weather-observatory.svg
│   │   ├── rocket-flight-analysis.svg
│   │   ├── atmospheric-layers.svg
│   │   ├── scientific-graphs.svg
│   │   └── mission-control-ui-concept.svg
│   ├── VISUAL_GALLERY.md
│   ├── images/
│   │   ├── orbit-digital-twin.svg
│   │   ├── system-architecture-3d.svg
│   │   └── rocket-physics-3d.svg
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── DATA_SOURCES.md
│   ├── DEMO_GUIDE.md
│   ├── INTERVIEW_GUIDE.md
│   ├── LIMITATIONS.md
│   ├── MODEL_CARD.md
│   ├── PHYSICS.md
│   ├── PROJECT_TREE.md
│   ├── REPORTING.md
│   └── TEST_PLAN.md
├── .env.example
├── .dockerignore
├── CONTRIBUTING.md
├── SECURITY.md
├── .github/dependabot.yml
├── .gitignore
├── docker-compose.yml
├── docker-compose.private.yml    Private-backend loopback staging
├── LICENSE
├── pyproject.toml
└── README.md
~~~

## Folder roles and why this structure is chosen

- **src/astrasentinel**: importable, framework-independent scientific models. Each can be unit-tested without the web app.
- **backend**: HTTP interface, schemas and request validation.
- **frontend**: visual mission-control application and 3D globe.
- **tests**: reproducible offline quality checks and API integration.
- **docs/images**: original scalable 3D-style diagrams and project illustrations.
- **docs**: explanations, diagrams, source disclosures, test plan and interview presentation material.
- **.github/workflows**: automated Python tests and React build on source changes.
- **docker-compose.yml**: backend + frontend as a single runnable local stack.

The extensive original planning proposal also mentioned a production database, MLflow, and separate NASA/ISRO modules. Those would add **empty scaffolding** if created now, so the release deliberately contains only implemented capabilities and clearly documents possible expansions.
