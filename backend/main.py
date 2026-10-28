"""FastAPI surface for the educational mission dashboard."""
from __future__ import annotations

from dataclasses import fields
from typing import Literal
from astrasentinel.scenarios import compare_scenarios
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

from astrasentinel.atmosphere import density
from astrasentinel.ingestion import satellite_elements, space_weather
from astrasentinel.orbit import current_orbit
from astrasentinel.rocket import RocketConfig, simulate
from astrasentinel.telemetry import FEATURES, score_matrix, telemetry_series, evaluation
from astrasentinel.reporting import build_mission_report

app = FastAPI(
    title="AstraSentinel AI API",
    version="1.0.0",
    description="Educational space-mission digital twin. Predictions are not operational advice.",
)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173",
                  "http://127.0.0.1:5173"], allow_credentials=False,
                  allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


class RocketRequest(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)

    dry_mass_kg: float = 480
    propellant_kg: float = 900
    thrust_n: float = 30000
    burn_time_s: float = 60
    drag_coefficient: float = 0.42
    area_m2: float = 1.0
    density_multiplier: float = 1.0
    duration_s: float = 420
    dt_s: float = 0.2


class ScenarioCompareRequest(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    parameter: Literal["thrust_n", "propellant_kg", "density_multiplier",
                       "drag_coefficient", "area_m2"] = "thrust_n"
    values: list[float] = Field(default_factory=lambda: [25000, 30000, 35000, 40000],
                                min_length=2, max_length=7)
    baseline: RocketRequest = Field(default_factory=RocketRequest)


class TelemetryRequest(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)

    battery_voltage_v: float = Field(ge=0, le=100)
    temperature_c: float = Field(ge=-150, le=250)
    bus_current_a: float = Field(ge=0, le=100)
    attitude_error_deg: float = Field(ge=0, le=180)


@app.get("/")
def root():
    # In the single-container release, "/" must render the compiled React UI.
    # Development/two-container mode retains its original JSON service index.
    frontend_dist = os.getenv("ASTRA_WEB_DIST")
    if frontend_dist:
        index = Path(frontend_dist) / "index.html"
        if not index.is_file():
            raise HTTPException(503, "Compiled frontend HTML unavailable")
        return FileResponse(index, media_type="text/html")
    return {"project": "AstraSentinel AI", "api_docs": "/docs",
            "dashboard": "frontend: http://localhost:5173 (dev) or http://localhost:3000 (Docker)"}


@app.get("/api/health")
def health():
    return {"ok": True, "service": "astrasentinel", "version": "1.0.0"}


@app.get("/api/satellite")
def satellite():
    elements = satellite_elements()
    return {"name": elements["name"], "catalog_id": 25544,
            "source": elements["source"], "source_url": elements["source_url"],
            "tle": [elements["line1"], elements["line2"]]}


@app.get("/api/orbit")
def orbit():
    try:
        return current_orbit()
    except ValueError as exc:
        raise HTTPException(502, "Orbit propagation unavailable: " + str(exc)) from exc


@app.get("/api/weather")
def weather():
    return space_weather()


@app.get("/api/telemetry")
def telemetry():
    return telemetry_series()


@app.get("/api/model/evaluation")
def model_evaluation():
    return evaluation()


@app.post("/api/telemetry/score")
def score(body: TelemetryRequest):
    vector = [[getattr(body, feature) for feature in FEATURES]]
    return score_matrix(vector)["rows"][0]


@app.post("/api/rocket")
def rocket(body: RocketRequest):
    try:
        config = RocketConfig(**body.model_dump())
        return simulate(config)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@app.post("/api/rocket/compare")
def compare_rocket(body: ScenarioCompareRequest):
    """Bounded, reproducible educational physics experiment (max seven runs)."""
    try:
        return compare_scenarios(body.parameter, body.values,
                                 RocketConfig(**body.baseline.model_dump()))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@app.get("/api/rocket/demo")
def rocket_demo():
    return simulate()


@app.get("/api/atmosphere")
def atmosphere():
    heights_km = list(range(0, 101, 2))
    return {
        "model": "isothermal exponential approximation",
        "scale_height_m": 8500,
        "sea_level_density_kg_m3": 1.225,
        "points": [{"altitude_km": km, "density_kg_m3": density(km * 1000)}
                   for km in heights_km],
    }


@app.get("/api/mission/report")
def mission_report():
    """Create a source-attributed snapshot on demand, with no operational safety claims."""
    try:
        return build_mission_report(current_orbit(), space_weather(),
                                    telemetry_series(), simulate())
    except ValueError as exc:
        raise HTTPException(502, "Mission report unavailable: " + str(exc)) from exc
