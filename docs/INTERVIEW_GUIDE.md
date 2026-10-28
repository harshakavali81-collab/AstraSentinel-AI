# AstraSentinel AI — Job Interview Explanation

[Project home](../README.md) · [Architecture diagram](images/system-architecture-3d.svg)

## Tell me about your project (45 seconds)

AstraSentinel AI is my educational space-mission digital twin combining orbital mechanics, anomaly detection, atmospheric science and full-stack development. I built a FastAPI backend that fetches public ISS orbital elements from CelesTrak and space-weather readings from NOAA. SGP4 propagates the ISS orbit into time-tagged 3D positions, which I render using React and Three.js. For AI, I use an IsolationForest trained on reproducible **synthetic** satellite sensor values with simulated anomalies and evaluation metrics. I also implemented an interactive rocket simulator with changing mass, thrust, gravity and drag. I validate the modules with offline pytest tests and automate the checks with GitHub Actions.

## Five useful follow-up Q&A prompts

**Why SGP4 instead of drawing an ellipse?** GP/TLE elements are fitted for the SGP4 general perturbations model, so using an SGP4 library produces a more relevant time-dependent orbital estimate than a generic static ellipse.

**Why IsolationForest?** Fault labels may be limited. It learns the distribution of healthy synthetic samples, and I examine unusual combinations of telemetry using anomaly score plus feature deviation diagnostics. My reported metrics describe only artificially injected synthetic faults, not real spacecraft reliability.

**How does the rocket simulation work?** At every time step, the model updates mass during the engine burn and computes thrust, altitude-dependent gravity and signed drag. It integrates velocity and altitude numerically and plots the simulated trajectory.

**How is the rocket scenario comparison designed?** I implemented a deterministic one-factor-at-a-time experiment engine that validates two to seven unique bounded parameter values, runs the 1D rocket solver for each case, and returns metrics plus downsampled altitude/velocity data. A React page compares the curves and exports CSV/JSON. This is not uncertainty quantification or an operational launch optimizer.

**How is the system reproducible?** I use fixed dataset/model seeds, cache and label public sources, include an offline mode, test source parsing/physics/API behavior and build the React app in GitHub Actions.

**What would you improve?** I would validate coordinate frames against reference standards, use higher-fidelity atmosphere and integration, add OMM satellite catalog support, introduce PostgreSQL historical storage and validate ML with approved real mission data.

## Resume bullets (adapt after reviewing the demo)

- Developed an educational aerospace AI digital twin using Python, FastAPI and React, connecting public CelesTrak TLE and NOAA space-weather datasets.
- Built an interactive Three.js 3D Earth viewer for SGP4-propagated ISS trajectories and Earth-frame approximate coordinate exploration.
- Trained and evaluated an IsolationForest anomaly detector using controlled, seeded **synthetic satellite telemetry**, exposing interpretable REST predictions.
- Implemented a rocket physics engine plus bounded scenario-sensitivity experiments, a REST comparison API, interactive React charts, and CSV/JSON exports; verified with deterministic tests and Docker CI.

**Be accurate:** do not claim a NASA/ISRO/SpaceX partnership, real satellite telemetry training, flight-certified simulations, validated collision prediction, or a live hosted production deployment.
