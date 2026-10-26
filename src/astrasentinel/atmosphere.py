"""Educational exponential atmosphere, not a space-weather-driven density model."""
import math

RHO0 = 1.225         # kg / m^3
SCALE_HEIGHT = 8500  # m, intentionally simplified


def density(altitude_m: float, density_multiplier: float = 1.0) -> float:
    if altitude_m < 0 or density_multiplier <= 0:
        raise ValueError("Altitude and density multiplier must be physical")
    return RHO0 * density_multiplier * math.exp(-min(altitude_m, 1e6) / SCALE_HEIGHT)


def drag_force(altitude_m: float, velocity_m_s: float, cd: float,
               area_m2: float, density_multiplier: float = 1.0) -> float:
    """Signed force opposing velocity; negative when ascending."""
    if cd < 0 or area_m2 < 0:
        raise ValueError("Cd and area must be nonnegative")
    rho = density(altitude_m, density_multiplier)
    return -0.5 * rho * cd * area_m2 * velocity_m_s * abs(velocity_m_s)
