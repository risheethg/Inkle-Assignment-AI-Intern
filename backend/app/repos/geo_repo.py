import httpx
import inspect
from typing import Optional
from app.core.config import settings
from app.core.logger import logs
from app.models.location_models import LocationData

class GeoRepo:
    async def get_coordinates(self, place_name: str) -> Optional[LocationData]:
        """Get coordinates with fallback to Photon API if Nominatim fails"""
        
        # Try Nominatim first
        result = await self._get_coordinates_nominatim(place_name)
        if result:
            return result
        
        # Fallback to Photon API
        logs.define_logger(
            level=30, 
            message=f"Nominatim failed for {place_name}, trying Photon API fallback", 
            loggName=inspect.stack()[0]
        )
        return await self._get_coordinates_photon(place_name)
    
    async def _get_coordinates_nominatim(self, place_name: str) -> Optional[LocationData]:
        """Primary geocoding using Nominatim"""
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
                    message=f"Nominatim error for {place_name}: {str(e)}", 
                    loggName=inspect.stack()[0]
                )
                return None
    
    async def _get_coordinates_photon(self, place_name: str) -> Optional[LocationData]:
        """Fallback geocoding using Photon API (komoot.io)"""
        params = {
            "q": place_name,
            "limit": 1
        }
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.get("https://photon.komoot.io/api/", params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("features") and len(data["features"]) > 0:
                    feature = data["features"][0]
                    coords = feature["geometry"]["coordinates"]
                    props = feature.get("properties", {})
                    
                    # Photon returns [lon, lat] order
                    return LocationData(
                        name=props.get("name", place_name),
                        lat=coords[1],
                        lon=coords[0]
                    )
                return None
            except Exception as e:
                logs.define_logger(
                    level=40, 
                    message=f"Photon API error for {place_name}: {str(e)}", 
                    loggName=inspect.stack()[0]
                )
                return None