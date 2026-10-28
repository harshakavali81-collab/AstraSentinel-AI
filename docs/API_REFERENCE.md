# AstraSentinel AI — REST API

[Project home](../README.md) · [Architecture](ARCHITECTURE.md)

Start the Python server and browse the generated **OpenAPI / Swagger interface** at http://localhost:8000/docs.

| Verb | Endpoint | Description |
|---|---|---|
| GET | / | Project name and user-facing URLs |
| GET | /api/health | Application health and version |
| GET | /api/satellite | ISS 25544 TLE and provenance |
| GET | /api/orbit | SGP4 time samples: ECEF xyz, estimated latitude/longitude, altitude, element age |
| GET | /api/weather | Latest NOAA planetary Kp, chart history, source and freshness |
| GET | /api/telemetry | Simulated telemetry, detector flags, diagnostics and evaluation results |
| GET | /api/model/evaluation | Synthetic test-set precision, recall, false alarm rate and confusion matrix |
| POST | /api/telemetry/score | Score one hypothetical telemetry record |
| GET | /api/rocket/demo | Run the default educational rocket case |
| POST | /api/rocket | Run an input-controlled rocket case |
| POST | /api/rocket/compare | Run 2–7 reproducible one-factor rocket experiments and return metrics plus plot points |
| GET | /api/atmosphere | Calculate reference exponential density curve |

### Try orbital and weather datasets

~~~bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/orbit
curl http://localhost:8000/api/weather
curl http://localhost:8000/api/model/evaluation
~~~

### Score a telemetry sample

~~~bash
curl -X POST http://localhost:8000/api/telemetry/score \
  -H "Content-Type: application/json" \
  -d '{"battery_voltage_v":27.8,"temperature_c":23,"bus_current_a":3,"attitude_error_deg":0.6}'
~~~

The result contains anomaly (boolean), anomaly_score, leading_deviation, deviation_z and a measurements object. A larger positive score suggests a deviation from the fitted **synthetic** baseline; this is not a probability.

### Simulate a customized rocket scenario

~~~bash
curl -X POST http://localhost:8000/api/rocket \
  -H "Content-Type: application/json" \
  -d '{"dry_mass_kg":480,"propellant_kg":900,"thrust_n":33000,"burn_time_s":60,"drag_coefficient":0.42,"area_m2":1,"density_multiplier":1.2,"duration_s":420,"dt_s":0.2}'
~~~

The result contains a configuration, documented assumptions, metrics (apogee_km, peak_velocity_m_s, max_dynamic_pressure_pa, simulated_time_s), and trajectory points (time_s, altitude_km, velocity_m_s, mass_kg, acceleration_m_s2, dynamic_pressure_pa).

### Compare launch-physics scenarios

The new bounded experiment interface compares 2–7 unique values of one supported parameter while the rest remain at the baseline values.

~~~bash
curl -X POST http://localhost:8000/api/rocket/compare \
  -H "Content-Type: application/json" \
  -d '{"parameter":"thrust_n","values":[25000,30000,35000,40000],"baseline":{"density_multiplier":1}}'
~~~

The response includes the original baseline configuration and metrics, named variant runs with individual metrics, separately downsampled altitude/velocity curves, apogee change relative to the baseline, parameter units, assumptions and a mandatory scientific disclaimer. Values outside the model's parameter bounds or more than seven scenarios return 422. No mission success probabilities, flight safety advice or calibrated error intervals are inferred.

### Error and data status contracts

- Inputs violating Pydantic or numerical physics ranges return **HTTP 422**.
- Unusable SGP4 propagation returns **HTTP 502** instead of pretending to have an orbit.
- The GET responses surface source names such as CelesTrak, NOAA SWPC, bundled_historical_demo and synthetic_historical_demo.
- Orbit status is current/stale/demo. Weather status is live/stale/demo.
- Some source calls may block up to the configured 10-second upstream timeout before the demo fallback is returned.

Use the dynamically generated /openapi.json as the authoritative detailed response schema. The API is for demonstration and does not currently have public-hosting authentication or rate limiting.
