# Full Project Repository Tree

[Project home](../README.md)

~~~text
AstraSentinel-AI/
├── .github/
│   └── workflows/
│       ├── ci.yml                 Python, browser and standalone container CI
│       └── pages.yml              Pages publishing only after owner enablement
├── backend/
│   ├── __init__.py
│   ├── Dockerfile
│   ├── basic_auth.py             Optional hosted-demo credential middleware
│   ├── main.py                    FastAPI application
│   └── standalone.py              Mounts compiled React assets after API routes
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
│   ├── nginx.conf            Browser headers and request limits
│   ├── playwright.config.js Chromium integration test configuration
│   ├── e2e/
│   │   └── mission.spec.js   Browser flow and real screenshots
│   ├── tests/
│   │   ├── curves.test.mjs   Comparison curve alignment
│   │   └── groundTrack.test.mjs Geospatial plotting and dateline
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── api.js
│       ├── App.jsx                Mission pages and charts
│       ├── GroundTrack.jsx        Model-derived ground track map
│       ├── groundTrack.js        Projection and dateline split
│       ├── scenarioCurves.js     Common time-axis interpolation
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
│   ├── test_basic_auth.py         Credential handling and HTTP auth tests
│   ├── test_standalone_contract.py
│   ├── test_security_contracts.py
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
├── docker-compose.standalone.yml Single deployable container on 127.0.0.1:8080
├── Dockerfile.standalone        React+Python one-image production build
├── render.yaml                 Optional Render deployment manifest
├── .railway/
│   └── railway.ts              Current Railway infrastructure-as-code manifest
├── LICENSE
├── pyproject.toml
└── README.md
~~~

## Folder roles and why this structure is chosen

- **src/astrasentinel**: importable, framework-independent scientific models. Each can be unit-tested without the web app.
- **backend**: HTTP interface, schemas and request validation.
- **frontend**: visual mission-control application, 3D globe, SGP4 ground-track chart, unit tests and browser end-to-end screenshots.
- **tests**: reproducible offline quality checks and API integration.
- **docs/images**: original scalable 3D-style diagrams and project illustrations.
- **docs**: explanations, diagrams, source disclosures, test plan and interview presentation material.
- **.github/workflows**: automated Python tests and React build on source changes.
- **docker-compose.yml**: backend + frontend as a single runnable local stack.

The extensive original planning proposal also mentioned a production database, MLflow, and separate NASA/ISRO modules. Those would add **empty scaffolding** if created now, so the release deliberately contains only implemented capabilities and clearly documents possible expansions.
