# Orbital Mechanics, Atmosphere and Rocket Physics

[Project home](../README.md) · [3D satellite picture](images/orbit-digital-twin.svg) · [Rocket picture](images/rocket-physics-3d.svg)

## 1. ISS orbital propagation

CelesTrak serves general perturbation (GP) orbital elements in Two-Line Element format. The Python sgp4 library constructs a satellite record and predicts a time-tagged TEME position in kilometers.

For display, the backend rotates TEME positions about Earth using an approximate Greenwich Mean Sidereal Time angle. The rotated coordinates are approximately Earth-fixed, and estimated latitude/longitude can be derived from the resulting position vector.

~~~text
T = (JulianDate - 2451545.0) / 36525
GMST(deg) ~= 280.46061837 + 360.98564736629*(JD - 2451545)
             + 0.000387933*T^2 - T^3 / 38710000

X_ecef = cos(GMST)*X_teme + sin(GMST)*Y_teme
Y_ecef = -sin(GMST)*X_teme + cos(GMST)*Y_teme
Z_ecef = Z_teme

Altitude(km) ~= norm(R) - 6378.137
~~~

**Accuracy caveat:** A professional TEME-to-ECEF conversion needs precise polar motion and Earth orientation corrections. The project deliberately omits these. The Earth globe uses hand-drawn, stylized continental regions. Do not use it for geolocation, maneuver planning or collision prediction.

## 2. Approximate atmosphere

~~~text
density(h) = 1.225 kg/m^3 * density_multiplier * exp(-h / 8500 m)
~~~

It is a one-scale-height model that does not handle altitude-dependent molecular composition, temperature layers, horizontal winds, thermospheric density variability or solar activity. The simulator is not a validated standard atmosphere.

## 3. Drag and rocket acceleration

Drag always acts opposite the vertical velocity:

~~~text
DragForce = -0.5 * density(h) * Cd * area * velocity * abs(velocity)
gravity(h) = 9.80665 * (6378137 / (6378137 + h))^2
net_acceleration = (thrust + DragForce)/mass - gravity(h)
~~~

Mass decreases linearly until engine cutoff; it is bounded below by dry mass. Thrust is modeled as a fixed value during the burn and zero thereafter.

## 4. Numerical integration

The backend uses a semi-implicit Euler step:

~~~text
velocity_next = velocity + net_acceleration * timestep
altitude_next = max(0, altitude + velocity_next * timestep)
~~~

The default integration step is 0.2 seconds, with physical input bounds and a simulated duration cap. This approximation is fast and easy to inspect, but burn boundaries may fall between steps and accuracy has not been validated against real flight data. The simulation assumes vertical motion with no steering, lift, staging, winds, engine performance variation or orbital insertion.

## 5. Numerical checks

Automated tests confirm the Earth-frame rotation preserves vector norm; atmosphere density decreases with altitude; gravity decreases with height; drag always opposes velocity; masses stay at/above dry mass; altitude stays nonnegative; simulation outputs remain finite; and higher assumed air density decreases apogee for the demonstration case. This is **sanity checking**, not professional aerospace model validation.

![Rocket ascent and drag 3D-style diagram](images/rocket-physics-3d.svg)


## Burnout-boundary integration and step-size sanity checks

The semi-implicit Euler integration now **splits a time step at the prescribed engine burnout event**. For example, if the burn ends at 60.15 seconds and the configured step is 0.2 seconds, the integrator records a sample at 60.15 seconds and switches to coasting immediately afterward rather than applying full thrust through the rest of the nominal step. This improves event handling while remaining a low-order educational solver.

A deterministic unit test compares the default scenario at 0.1 and 0.2-second steps for broad numerical consistency. **This is not a rigorous convergence study, independently validated rocket dynamics, or a safety margin**.
