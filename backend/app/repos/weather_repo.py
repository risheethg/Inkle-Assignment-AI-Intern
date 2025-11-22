import httpx
import inspect
from backend.app.core.config import settings
from backend.app.core.logger import logs
from backend.app.models.base_models import LocationData
from typing import List, Optional


class WeatherRepo:
    async def get_current_weather(self, lat: float, lon: float):
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(settings.OPEN_METEO_URL, params=params)
                return response.json()
            except Exception as e:
                logs.define_logger(
                    level=40, 
                    message=f"Error fetching weather: {str(e)}", 
                    loggName=inspect.stack()[0]
                )
                return None
