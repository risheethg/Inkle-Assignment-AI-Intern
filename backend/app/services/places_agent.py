"""
Places Agent - Child agent that handles tourist attractions queries
Uses external Places API and AI to provide natural language responses
"""
from typing import Optional, List
from app.repos.geo_repo import GeoRepo
from app.repos.places_repo import PlacesRepo
from app.services.ai_client import ai_client
from app.core.logger import logs
import inspect

class PlacesAgent:
    def __init__(self):
        self.geo_repo = GeoRepo()
        self.places_repo = PlacesRepo()
        self.name = "Places Agent"
    
    async def get_tourist_places(self, place_name: str, limit: int = 5) -> Optional[List[str]]:
        """
        Fetch tourist attractions for a given place
        Returns a list of place names
        """
        try:
            # Step 1: Get coordinates for the place
            location = await self.geo_repo.get_coordinates(place_name)
            if not location:
                return None
            
            # Step 2: Get tourist attractions
            places = await self.places_repo.get_tourist_attractions(location.lat, location.lon, limit)
            if not places:
                return None
            
            return places
        
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error in Places Agent: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return None
    
    async def process_query(self, place_name: str, user_query: str) -> Optional[str]:
        """
        Process a places-related query with AI assistance
        """
        places = await self.get_tourist_places(place_name)
        
        if not places:
            return None
        
        # Format places list
        places_text = "\n".join(places)
        
        # Use AI to format response according to user's query
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a tourism assistant helping people discover places to visit. "
                    "Provide helpful, enthusiastic information about tourist attractions. "
                    "Keep responses natural and conversational."
                )
            },
            {
                "role": "user",
                "content": (
                    f"User asked: '{user_query}'\n"
                    f"Tourist attractions in {place_name}:\n{places_text}\n"
                    f"Provide a natural response listing these places."
                )
            }
        ]
        
        try:
            response = await ai_client.chat_completion(messages, temperature=0.7)
            return response
        except Exception as e:
            # Fallback to simple list if AI fails
            logs.define_logger(
                level=30,
                message=f"AI formatting failed, using simple list: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return f"In {place_name} these are the places you can go:\n{places_text}"
