import httpx
import inspect
from typing import Optional
from app.core.config import settings
from app.core.logger import logs
from app.models.location_models import LocationData

class GeoRepo:
    async def get_coordinates(self, place_name: str) -> Optional[LocationData]:
        params = {
            "q": place_name,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "TourismAIIntern/1.0",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.get(settings.NOMINATIM_URL, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                if data and isinstance(data, list) and len(data) > 0:
                    return LocationData(
                        name=data[0].get("display_name", place_name),
                        lat=float(data[0]["lat"]),
                        lon=float(data[0]["lon"])
                    )
                return None
            except Exception as e:
                logs.define_logger(
                    level=40, 
                    message=f"Error fetching coordinates for {place_name}: {str(e)}", 
                    loggName=inspect.stack()[0]
                )
                return None