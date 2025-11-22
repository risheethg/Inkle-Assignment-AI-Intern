from pydantic import BaseModel
from typing import Optional

class WeatherData(BaseModel):
    temperature: float
    precipitation_probability: Optional[float] = None
    windspeed: Optional[float] = None
    weather_code: Optional[int] = None
    
    def to_description(self) -> str:
        """Convert weather data to human-readable description"""
        desc = f"currently {self.temperature}°C"
        if self.precipitation_probability is not None:
            desc += f" with a chance of {self.precipitation_probability}% to rain"
        return desc
