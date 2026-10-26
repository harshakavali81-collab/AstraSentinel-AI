# Scientific Integrity, Security and Limitations

This is an **educational software research demonstrator**, not an operational or flight-qualified space product.

1. **No official affiliation:** Not created by, approved by, or directly connected to NASA, ISRO, SpaceX, CelesTrak or NOAA.
2. **Source estimates vs measured state:** Public GP/TLEs give SGP4 orbital estimates and may be stale. The system reports epoch and status.
3. **Artificial satellite health telemetry:** No authentic private spacecraft sensor stream is used. Training, injections, metrics and demonstration predictions all use synthetic data.
4. **No calibrated failure probability:** IsolationForest decision scores indicate unusualness under a synthetic baseline, not a probability of spacecraft damage or fault.
5. **Simplified atmosphere and rocket:** Not valid for flight planning or certification; omit winds, steering, staging, complex drag, thermal and atmospheric profiles.
6. **Approximate Earth-frame calculation:** Simplified GMST rotation omits precise Earth-orientation corrections; illustrative continental texture is not georeferenced.
7. **No conjunction risk engine:** No collision probability, maneuvers, orbit determination uncertainty model, debris warning or operational mission commanding.
8. **Unavailable upstream data:** Explicitly labeled historical/synthetic fallbacks keep the demo working; no claim that fallback readings are current.
9. **Not a hosted production service:** Publishing the source repository does not provision a public application URL. Deployment, authentication, audit logging and rate limiting are separate work.
10. **No persistent database / ML registry yet:** PostgreSQL, MLflow, space-weather alerting, scheduled ingestion and account management are planned extensions, not currently delivered features.

## Production hardening checklist

- Establish authenticated users, request quotas, HTTPS, reverse-proxy protections, logs and telemetry.
- Add persistent source cache, historical timestamps, data retention and backups.
- Pin and regularly update dependencies, enable vulnerability scanning and container CI.
- Add numerical reference-vector verification and high-order orbital/rocket validation.
- Add a versioned model artifact pipeline with permitted representative datasets and domain review.
- Deploy through a controlled provider and clearly distinguish simulation mode from public live-source mode.

See [System Architecture](ARCHITECTURE.md), [Data Sources](DATA_SOURCES.md) and [Testing](TEST_PLAN.md).
