import httpx
import inspect
from typing import Optional
from app.core.config import settings
from app.core.logger import logs
from app.models.weather_models import WeatherData


class WeatherRepo:
    async def get_current_weather(self, lat: float, lon: float) -> Optional[WeatherData]:
        """Fetch current weather data for given coordinates"""
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "hourly": "precipitation_probability",
            "forecast_days": 1
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(settings.OPEN_METEO_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "current_weather" in data:
                    current = data["current_weather"]
                    
                    # Get precipitation probability from hourly forecast
                    precip_prob = None
                    if "hourly" in data and "precipitation_probability" in data["hourly"]:
                        hourly_precip = data["hourly"]["precipitation_probability"]
                        if hourly_precip:
                            # Average the next few hours
                            precip_prob = sum(hourly_precip[:6]) / min(len(hourly_precip), 6)
                    
                    return WeatherData(
                        temperature=current.get("temperature"),
                        precipitation_probability=precip_prob,
                        windspeed=current.get("windspeed"),
                        weather_code=current.get("weathercode")
                    )
                return None
            except Exception as e:
                logs.define_logger(
                    level=40, 
                    message=f"Error fetching weather: {str(e)}", 
                    loggName=inspect.stack()[0]
                )
                return None
