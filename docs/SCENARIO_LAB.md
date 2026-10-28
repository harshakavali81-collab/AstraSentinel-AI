# Rocket Scenario Comparison Lab

[Project home](../README.md) · [REST API](API_REFERENCE.md) · [Physics](PHYSICS.md) · [Run the demo](DEMO_GUIDE.md)

## Purpose

Show real software-engineering experimentation with an educational one-dimensional rocket model. The application provides a bounded parameter comparison engine rather than untestable screenshots of futuristic dashboards.

## Experiment workflow

1. Choose one factor from thrust, propellant mass, atmospheric density multiplier, drag coefficient or reference frontal area.
2. Supply 2–7 distinct numeric values within the bounds implemented by `RocketConfig.validate`.
3. Keep the other model inputs at one common baseline. The application runs `simulate` for each scenario using the same semi-implicit Euler integrator.
4. Review apogee, peak vertical speed and maximum modeled dynamic pressure for every scenario.
5. The React dashboard draws comparison trajectories and allows CSV/JSON export. Curve points are downsampled, but reported metrics come from each full numerical run.

## A reproducible API example

```bash
curl -X POST http://localhost:8000/api/rocket/compare \
  -H "Content-Type: application/json" \
  -d '{"parameter":"density_multiplier","values":[0.5,1,2]}'
```

The expected *direction* for the supplied rocket model is lower apogee as air density increases, because stronger quadratic drag opposes vertical motion. Likewise, larger thrust values generally increase apogee in the default scenario. **These are model sensitivities, not predictions for a real rocket vehicle.**

## Implementation map

- Scientific model and bounds: [scenarios.py](../src/astrasentinel/scenarios.py)
- Underlying vertical integrator: [rocket.py](../src/astrasentinel/rocket.py)
- HTTP schemas and endpoint: [backend/main.py](../backend/main.py)
- Responsive dashboard: [ScenarioLab.jsx](../frontend/src/ScenarioLab.jsx)
- Deterministic tests: [test_scenarios.py](../tests/test_scenarios.py)
- API tests: [test_api.py](../tests/test_api.py)
- Reproducible 4-case thrust plot and CSV: [report generator](../scripts/generate_demo_artifacts.py)

## Limitations and honest claims

- The model omits wind, lift, lateral motion, flight control, steering, staging and calibrated upper-atmosphere behavior.
- No Monte Carlo dispersion, measurement uncertainty, tolerances, failure distribution or validation against real launch data is supplied.
- The comparison may change when the numerical step size or physical assumptions change.
- The model cannot be used to choose flight hardware, launch settings or operational safety thresholds.

The results are suitable for **educational sensitivity analysis, REST API demonstration, responsive charting and software testing**, not real aerospace mission planning.
