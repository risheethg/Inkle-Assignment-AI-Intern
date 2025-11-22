from pydantic import BaseModel

class LocationData(BaseModel):
    name: str
    lat: float
    lon: float
