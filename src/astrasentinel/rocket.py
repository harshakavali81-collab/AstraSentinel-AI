"""One-dimensional vertical educational ascent, variable mass and quadratic drag.

Not a guidance system. Launch pad is at sea level; no winds, lift, staging,
Earth rotation, steering losses, or thermochemistry.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from .atmosphere import density, drag_force

G0 = 9.80665
R_EARTH_M = 6378137.0


@dataclass
class RocketConfig:
    dry_mass_kg: float = 480.0
    propellant_kg: float = 900.0
    thrust_n: float = 30000.0
    burn_time_s: float = 60.0
    drag_coefficient: float = 0.42
    area_m2: float = 1.0
    density_multiplier: float = 1.0
    duration_s: float = 420.0
    dt_s: float = 0.2

    def validate(self) -> None:
        if not (10 <= self.dry_mass_kg <= 1000000
                and 0 <= self.propellant_kg <= 1000000
                and 0 <= self.thrust_n <= 20000000
                and 1 <= self.burn_time_s <= 600
                and 0 <= self.drag_coefficient <= 3
                and 0.01 <= self.area_m2 <= 1000
                and 0.2 <= self.density_multiplier <= 5
                and 10 <= self.duration_s <= 900
                and 0.1 <= self.dt_s <= 2):
            raise ValueError("Rocket parameter outside supported educational bounds")


def gravity(altitude_m: float) -> float:
    return G0 * (R_EARTH_M / (R_EARTH_M + max(0, altitude_m))) ** 2


def simulate(config: RocketConfig | None = None) -> dict:
    config = config or RocketConfig()
    config.validate()
    h = 0.0
    v = 0.0
    t = 0.0
    peak_h = 0.0
    peak_v = 0.0
    max_q = 0.0
    points = []
    total_mass = config.dry_mass_kg + config.propellant_kg
    mdot = config.propellant_kg / config.burn_time_s
    # Allow two extra samples for the exact burn-boundary and landing event.
    # The burn split avoids accidentally applying thrust beyond the configured burn.
    step_count = math.ceil(config.duration_s / config.dt_s) + 2
    for i in range(step_count + 1):
        mass = max(config.dry_mass_kg, total_mass - mdot * min(t, config.burn_time_s))
        on = t < config.burn_time_s - 1e-10 and config.propellant_kg > 0
        thrust = config.thrust_n if on else 0.0
        drag = drag_force(max(0, h), v, config.drag_coefficient,
                          config.area_m2, config.density_multiplier)
        q = 0.5 * density(max(0, h), config.density_multiplier) * v * v
        acceleration = (thrust + drag) / mass - gravity(h)
        points.append({"time_s": round(t, 2), "altitude_km": round(h / 1000, 4),
                       "velocity_m_s": round(v, 3), "mass_kg": round(mass, 3),
                       "acceleration_m_s2": round(acceleration, 3),
                       "dynamic_pressure_pa": round(q, 2)})
        peak_h, peak_v, max_q = max(peak_h, h), max(peak_v, v), max(max_q, q)
        if i > 0 and h <= 0 and v < 0:
            break
        if i == step_count or t >= config.duration_s - 1e-10:
            break
        step = min(config.dt_s, config.duration_s - t)
        if on:
            step = min(step, config.burn_time_s - t)
        if step <= 0:
            break
        # Semi-implicit Euler integrates acceleration then position.
        v_next = v + acceleration * step
        h_next = h + v_next * step
        t += step
        v, h = v_next, max(0, h_next)
    return {
        "configuration": asdict(config), "assumptions": [
            "1D vertical point-mass ascent", "exponential atmosphere with fixed scale height",
            "quadratic drag; no wind or staging", "semi-implicit Euler integration",
            "not intended for real launch or flight certification",
        ],
        "metrics": {"apogee_km": round(peak_h / 1000, 3),
                    "peak_velocity_m_s": round(peak_v, 2),
                    "max_dynamic_pressure_pa": round(max_q, 2),
                    "simulated_time_s": round(t, 2)},
        "points": points,
    }
