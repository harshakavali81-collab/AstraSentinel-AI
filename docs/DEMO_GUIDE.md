# Demo Guide — Run and Present AstraSentinel

[Project home](../README.md) · [Interview guide](INTERVIEW_GUIDE.md)

## How to launch

**Docker:** clone the repository and run docker compose up --build. Access the dashboard at http://localhost:3000 and the API docs at http://localhost:8000/docs.

**Development:** Python 3.11 with pip install -e '.[dev]', then python -m uvicorn backend.main:app --reload. In another terminal, cd frontend; npm install; npm run dev. Open http://localhost:5173.

**Offline:** Set ASTRA_OFFLINE=1 on the backend process. With Docker, change the ASTRA_OFFLINE entry in docker-compose.yml to "1". The weather series becomes synthetic historical data and the orbit uses an illustrative 2024 epoch TLE. The labels make it clear those are not current measurements.

## Eight-screen walkthrough

1. **Mission overview:** Explain the data cards. ISS altitude is an SGP4 estimate; Kp is NOAA space-weather context; flagged anomalies are synthetic. Show data-source labels.
2. **Orbital explorer:** Drag and zoom the Three.js planet, scrub the timeline, and show changing 3D points and latitude/longitude. Explain why a TLE requires SGP4 and why Earth rotation is applied.
3. **Satellite health AI:** Show battery-voltage and temperature series, compare anomaly alerts, and input a strongly abnormal reading. Explain IsolationForest, independent synthetic evaluation and interpretation limits.
4. **Space weather:** Read the NOAA Kp series and geomagnetic storm Kp=5 threshold. Point out observation age and transparent offline fallback.
5. **Rocket lab:** Run the default simulator, then change the atmospheric multiplier from 0.6 to 2.0 and compare apogee. Explain mass loss, thrust, inverse-square gravity and drag.
6. **Scenario comparison:** Compare 0.5×, 1× and 2× density multipliers, inspect three resulting simulation curves, and download the metrics as CSV or JSON.
7. **Atmospheric density:** Move the atmosphere multiplier to compare density curves using the logarithmic chart.
8. **System architecture:** Walk through the diagrams, repository tree, API docs, test cases and GitHub Actions status.

## Demonstration scenarios

| Exercise | Expected behavior |
|---|---|
| Run in offline mode | All dashboard modules remain navigable, labeled historical/synthetic |
| Move the orbit time scrubber | The satellite changes position on the 3D SGP4 path |
| Score a very high temperature/current hypothetical sample | Model marks the extreme values as anomalous |
| Run a controlled rocket scenario experiment | View comparisons, baseline deltas, graphs and CSV/JSON export |
| Increase atmospheric density while holding everything else fixed | Lower simulated rocket apogee in the simplified model |
| Send an invalid negative rocket mass | Validation error (422) |
| Repeat the test suite | Stable scientific and API tests without external network calls |

## Static showcase

Start a local web server from the repository root using `python -m http.server 8080 --directory docs`. The static portfolio website links to project features but does **not** host FastAPI. To publish it, follow [the deployment instructions](DEPLOYMENT.md) and enable GitHub Pages on `main /docs` if appropriate.

## Troubleshooting

- If React cannot reach the API, check http://localhost:8000/api/health and ensure the Vite proxy or Docker nginx proxy is active.
- If the globe is black, enable hardware-accelerated WebGL in the browser. The rest of the API/chart interface works separately.
- If public datasets time out, start offline demo mode and explain the data provenance.
- If Docker reports ports already in use, modify the exposed 3000 or 8000 port mappings in docker-compose.yml.

The SVG diagrams represent original 3D-style **technical illustrations**, not screenshots of a live launch or current satellite imagery. A production live demo URL has not been deployed as part of the source repository.
