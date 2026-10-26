# Reproducible Testing and Scientific Verification

[Project home](../README.md)

The pytest fixture sets ASTRA_OFFLINE=1 automatically. The tests require **no external space-science network access** and thus do not exhaust data-source rate limits.

| Test | Primary assertions |
|---|---|
| tests/test_ingestion.py | Parse TLE, reject malformed pairs, accept NOAA modern and legacy Kp schemas, reject unphysical values, verify demo label |
| tests/test_orbit.py | Approximate rotation preserves norm, GMST angle range, ISS-formatted historic TLE produces LEO-like altitude/period, demo anchored to epoch |
| tests/test_rocket.py | Atmosphere density monotonicity, drag sign, inverse-square gravity trend, bounded integration, denser atmosphere gives reduced apogee |
| tests/test_telemetry.py | Fixed seed repeatability, four expected features, anomaly flag for extreme cases, finite-value validation and evaluation ranges |
| tests/test_api.py | Health, orbit, data provenance, weather, telemetry scoring, rocket runs, validation errors, atmosphere output |
| .github/workflows/ci.yml | Python 3.11 test job plus production React build on pushes and PRs |

## Run locally

~~~bash
python -m pip install -e '.[dev]'
python -m pytest tests -v --cov=astrasentinel --cov-report=term-missing
cd frontend
npm install
npm run build
~~~

Windows PowerShell can use the same pytest command since the fixture forces ASTRA_OFFLINE=1. The command does not require real satellite telemetry or API keys.

## Source and scientific validation gaps

- There are unit/integration *sanity checks* for the orbit engine, not a published precision comparison against authoritative SGP4 reference vectors or Earth Orientation Parameters.
- The exponential atmosphere is not validated against NRLMSISE-00 or the 1976 Standard Atmosphere.
- The rocket integrator has not been assessed by step-size convergence against a higher-order reference method or flight telemetry.
- The ML detector is evaluated only against seeded artificial fault injections; there is no mission-realistic failure distribution.
- Frontend bundling is checked; a full browser end-to-end screenshot regression suite has not been added.

## Future gates

Introduce numerical reference vectors, convergence tests, simulated extreme-altitude cases, mock upstream failures and source rate-limit tests, full browser interaction tests, hosting security scans, training-data drift checks and external domain review before claiming a stronger validation standard.
