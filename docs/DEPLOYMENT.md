# Hosting, Local Deployment, Security and Release Guide

[← README](../README.md) · [API Reference](API_REFERENCE.md) · [Visual Gallery](VISUAL_GALLERY.md) · [Limitations](LIMITATIONS.md)

AstraSentinel AI has **two different web surfaces**. Choose intentionally:

| Surface | Files | Requirements | What visitors get |
|---|---|---|---|
| **Static job-portfolio showcase** | docs/index.html, docs/landing.css, docs/gallery/*.svg | Any static website host / optional GitHub Pages | Fast responsive site with project graphics, tech stack, documentation and source links. **No backend or interactive SGP4/API dashboard**. |
| **Interactive full-stack mission console** | frontend, backend, src | Persistent hosting for Python FastAPI and nginx/React or Docker Compose | The actual dashboard, orbital propagation, NOAA data ingestion, telemetry ML, rocket simulation and experiments. |

## 1. Preview the new portfolio landing page locally

From the repository root:

~~~bash
python -m http.server 8080 --directory docs
~~~

Open http://localhost:8080/. All image links are relative and work without API credentials.

## 2. Publish the *static showcase* using GitHub Pages

This repository includes a complete Pages-ready docs/index.html but **the owner must enable Pages on GitHub**. Publishing cannot be assumed from committing the code.

1. Open the repository's **Settings → Pages**.
2. Set **Build and deployment → Source → GitHub Actions**. This enables Pages publishing for the repository.
3. Open **Actions → AstraSentinel Static Portfolio Pages**, select **Run workflow** on `main`. Its [workflow source](../.github/workflows/pages.yml) uploads `docs/` and deploys it. Future changes under `docs/` trigger automatic publication.
4. In **Settings → Pages**, copy the actual deployed URL **only after** the Pages workflow succeeds and the page opens.
5. This hosted site is a responsive portfolio **showcase only**; it does not provide a running Python API. Do not represent it as the live mission dashboard.

The deployment workflow checks Pages enablement first and skips publication if Pages has not been turned on. A source commit cannot enable Pages with the default GitHub Actions token; repository settings still require the owner's action.

If GitHub Pages is unavailable on your account or repository plan, preview via the local command above or deploy the docs directory to another static hosting platform.

## 3. Run the real full-stack application with Docker

~~~bash
git clone https://github.com/harshakavali81-collab/AstraSentinel-AI.git
cd AstraSentinel-AI
docker compose up --build -d
~~~

Open the actual console at http://localhost:3000/ and Swagger at http://localhost:8000/docs.

## 3a. Restricted private staging profile

An additional [docker-compose.private.yml](../docker-compose.private.yml) is provided for a safer local or trusted reverse-proxy staging setup. Its Python backend **does not publish port 8000 to the host**, and the frontend binds to host loopback only.

Command: ASTRA_OFFLINE=1 docker compose -f docker-compose.private.yml up --build -d

Connect locally to http://localhost:3000, or front it with your **own secure authenticated HTTPS gateway**. This is **not** a complete public-production deployment: user authentication, quotas, traffic security, monitoring, storage policy and abuse prevention remain necessary.

nginx now includes basic browser security headers, a request-body cap, and a moderate request rate limit. This is defense in depth, not a guarantee of safety. The default development Compose still exposes backend port 8000 for local debugging; do not deploy that profile directly to a public IP.

## 3b. Single-container React + FastAPI application

The full React mission console **and** Python API can now be hosted together using [Dockerfile.standalone](../Dockerfile.standalone). This two-stage image compiles the React frontend once, installs the Python science package, and mounts the compiled assets through [backend/standalone.py](../backend/standalone.py) *after* the API routes.

~~~bash
docker compose -f docker-compose.standalone.yml up --build -d
curl http://127.0.0.1:8080/api/health
~~~

Open http://localhost:8080 for the **working React mission dashboard** and http://localhost:8080/docs for Swagger. This version defaults to `ASTRA_OFFLINE=1`, so it makes **no live science-source calls** and is reproducible for interviews. The browser still performs actual FastAPI requests for orbital/ML/simulation functions.

Hosting configurations included: [Render](../render.yaml) and [Railway](../railway.json). They point to the one-image Dockerfile and health-check endpoint. A provider account, deployment permission and platform setup are required to produce a real public URL. Most hosts assign a `PORT` environment variable, and the container uses it automatically.

**Important security boundary:** The standalone Python container does not pass through the nginx rate limits and browser headers of the two-container version. It is not a production-hardened public service by itself. Configure a trusted HTTPS proxy, request limits, access controls, logging and abuse protection **outside** the image before exposing it publicly. Keep the default demo data source mode when demonstrating to recruiters.

### Deterministic offline demonstration

Linux/macOS:
~~~bash
ASTRA_OFFLINE=1 docker compose up --build -d
~~~

Windows PowerShell:
~~~powershell
$env:ASTRA_OFFLINE="1"
docker compose up --build -d
~~~

This runs **historical example** orbital elements and **synthetic historical** Kp data; all satellite health samples remain simulated in any mode.

## 4. Requirements for a real Internet-hosted API/dashboard

A platform capable of Docker/container applications or a VPS is required. Before publishing an externally reachable interactive instance:

- Terminate HTTPS at a trusted reverse proxy, obtain certificates and configure a hostname.
- Expose **only** the frontend reverse proxy to the public Internet; remove the direct backend port mapping in a deployment-specific Compose override, keeping backend traffic private.
- Restrict CORS and request origins appropriately; validate DNS and proxy headers.
- Add authentication, per-IP or per-user rate limits and abuse protection for public resource-intensive API endpoints.
- Cap upstream HTTP timeouts and dashboard traffic, monitor memory/CPU, set request logs and alerts, and define resource limits.
- Pin/update dependencies and review image and Python/Node dependency security findings.
- Follow source attribution and TLE/weather data provider terms; display stale/demo indicators and separate historical from current observations.
- Do not advertise flight-grade accuracy or live private spacecraft diagnostics.

Do not put API keys, passwords or deployment secrets in the repository.

The **GitHub Pages static site does not host Python**. Deploying that portfolio page cannot make the interactive dashboard run on the Pages URL.

## 5. Validate a release

~~~bash
python -m pip install -e '.[dev]'
python -m pytest tests -v --cov=astrasentinel --cov-report=term-missing
python -m scripts.generate_demo_artifacts --output artifacts/reports
cd frontend
npm install
npm run build
~~~

GitHub Actions runs Python scientific tests, builds the frontend, checks the two-service Docker stack with real Chromium, and **also builds/smoke-tests the new single-container image** at port 8080. Successful runs publish a `astrasentinel-static-website` artifact ready for upload, alongside generated scientific graphs and actual dashboard screenshots.

**Scope statement:** Neither the static portfolio nor the interactive prototype is an operational satellite flight system, meteorological alert service, collision prediction system or certified rocket simulator.
