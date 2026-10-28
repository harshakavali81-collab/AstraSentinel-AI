# Contributing to AstraSentinel AI

AstraSentinel AI is an educational aerospace AI and software engineering demonstration, not a flight-operations service.

## Local validation

1. Install Python 3.11+ dependencies with `python -m pip install -e '.[dev]'`.
2. Run `python -m pytest tests -v`; fixtures enforce deterministic no-network mode.
3. In `frontend/`, run `npm install` and `npm run build`.
4. Optionally verify full-stack integration with `ASTRA_OFFLINE=1 docker compose up --build`, then GET `/api/health` through localhost:3000.

## Contribution standards

- Add tests for scientific models, ingestion parsing, API routes and numerical edge cases.
- Label public, synthetic, historical and demo measurements distinctly. Never invent mission sensor readings.
- Do not claim agency affiliation, trained real-satellite telemetry models, certified rocket physics or precision geodetic reference frames.
- Make UI form controls accessible with labels and keyboard support.
- Keep diagrams and docs aligned with the actual implementation.
- Do not submit secrets, credentials or personally identifying datasets.
- Explain assumptions, limitations and tests in pull requests.

For security concerns, see [SECURITY.md](SECURITY.md).
