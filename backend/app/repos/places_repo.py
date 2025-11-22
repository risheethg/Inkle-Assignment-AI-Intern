import httpx
import inspect
from typing import List
from app.core.config import settings
from app.core.logger import logs

class PlacesRepo:
    async def get_tourist_attractions(self, lat: float, lon: float, limit: int = 5) -> List[str]:
        """Fetch tourist attractions near given coordinates using multiple categories"""
        
        # Query for multiple tourism-related tags to get better results
        query = f"""
        [out:json][timeout:25];
        (
          node["tourism"="attraction"](around:10000,{lat},{lon});
          node["tourism"="museum"](around:10000,{lat},{lon});
          node["tourism"="viewpoint"](around:10000,{lat},{lon});
          node["historic"](around:10000,{lat},{lon});
          node["leisure"="park"](around:10000,{lat},{lon});
          way["tourism"="attraction"](around:10000,{lat},{lon});
          way["tourism"="museum"](around:10000,{lat},{lon});
          way["historic"](around:10000,{lat},{lon});
          way["leisure"="park"](around:10000,{lat},{lon});
        );
        out center tags {limit * 2};
        """
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    settings.OVERPASS_URL,
                    data=query,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                data = response.json()
                
                places = []
                seen_names = set()
                
                if "elements" in data:
                    for element in data["elements"]:
                        if "tags" in element and "name" in element["tags"]:
                            name = element["tags"]["name"]
                            # Avoid duplicates
                            if name not in seen_names:
                                places.append(name)
                                seen_names.add(name)
                                if len(places) >= limit:
                                    break
                
                return places[:limit]
            except Exception as e:
                logs.define_logger(
                    level=40, 
                    message=f"Error fetching places: {str(e)}", 
                    loggName=inspect.stack()[0]
                )
                return []