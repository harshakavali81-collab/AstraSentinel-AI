# Data Sources, Provenance and Caching

[Project home](../README.md) · [Physics](PHYSICS.md)

| Source | Live URL | Purpose | Cache |
|---|---|---|---|
| CelesTrak GP | https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE | ISS NORAD 25544 orbital elements | 7,200 seconds |
| NOAA SWPC | https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json | Planetary geomagnetic Kp observations | 900 seconds |
| Local synthetic generator | src/astrasentinel/telemetry.py | Nominal telemetry, controlled anomaly injections and evaluation data | Deterministic seed |
| Numerical simulator | src/astrasentinel/rocket.py | Hypothetical vertical flight trajectory | Recomputed per scenario |

CelesTrak documentation: https://celestrak.org/NORAD/documentation/gp-data-formats.php and usage policy: https://celestrak.org/usage-policy.php. Respect their request cadence in any multi-user deployment.

### NOAA 2026 JSON change

As of 2026, NOAA's Kp payload uses arrays of objects such as a record containing time_tag and Kp. The parser also accepts legacy header-first array payloads. Invalid timestamps and Kp values outside 0–9 are rejected. Reference: https://www.weather.gov/media/notification/pdf_2026/scn26-21_Data_Format_Changes_Impacting_SWPC_Products.pdf

### Offline and upstream-unavailable operation

ASTRA_OFFLINE=1 avoids all outbound science-data calls. Instead the ISS viewer uses an illustrative historical 2024 TLE, propagated **at its historical epoch**. The Kp chart uses explicitly **synthetic 2024 example readings**. These cannot be confused with current observations: status and source fields identify them. Source failures are cached briefly to prevent continuous retries.

A real fetched TLE is marked **stale** when older than 72 hours; a stale orbit is sampled near its element epoch. NOAA observations older than 12 hours are marked **stale**. The age is derived from the latest observation timestamp, not falsely presented as data freshness when a network request succeeds.

### External source boundaries

A publicly available TLE is not an official live position or flight telemetry stream; orbital uncertainties depend on observations and extrapolation time. Planetary Kp is environmental context and does not directly measure a particular satellite's exposure, performance or risk of failure. No official agency partnership is implied.
