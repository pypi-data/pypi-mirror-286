from pydantic import BaseModel


class Orbit(BaseModel):
    orbits: str
    apoapsis_km: str
    periapsis_km: str
    inclination_deg: str
    period_min: str
