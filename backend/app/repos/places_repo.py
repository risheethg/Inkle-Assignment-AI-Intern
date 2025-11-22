import httpx
import inspect
from typing import List
from app.core.config import settings
from app.core.logger import logs

class PlacesRepo:
    async def get_tourist_attractions(self, lat: float, lon: float) -> List[str]:
        query = f"""
        [out:json];
        node["tourism"="attraction"](around:5000, {lat}, {lon});
        out limit 5;
        """
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(settings.OVERPASS_URL, params={"data": query})
                data = response.json()
                
                places = []
                if "elements" in data:
                    for element in data["elements"]:
                        if "tags" in element and "name" in element["tags"]:
                            places.append(element["tags"]["name"])
                return places
            except Exception as e:
                logs.define_logger(
                    level=40, 
                    message=f"Error fetching places: {str(e)}", 
                    loggName=inspect.stack()[0]
                )
                return []