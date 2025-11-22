import httpx
import inspect
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.logger import logs


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
