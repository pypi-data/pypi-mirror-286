from pydantic import BaseModel
from typing import List
from ..model.Duration import Duration
from ..model.Orbit import Orbit


class Mission(BaseModel):
    mission: str
    astronauts: List[str]
    program: str
    call_sign: str
    image_url: str
    launch_date_utc: str
    launch_mass_lbs: str
    launch_site: str
    launch_site_coord: str
    launch_vehicle: str
    landing_date_utc: str
    landing_site: str
    landing_site_coord: str
    recovery_ship: str
    duration: Duration
    earth_orbit: Orbit
    target_orbit: Orbit
