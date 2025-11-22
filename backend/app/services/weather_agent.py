"""
Weather Agent - Child agent that handles weather-related queries
Uses external Weather API and AI to provide natural language responses
"""
from typing import Optional
from app.repos.geo_repo import GeoRepo
from app.repos.weather_repo import WeatherRepo
from app.services.ai_client import ai_client
from app.core.logger import logs
import inspect

class WeatherAgent:
    def __init__(self):
        self.geo_repo = GeoRepo()
        self.weather_repo = WeatherRepo()
        self.name = "Weather Agent"
    
    async def get_weather_info(self, place_name: str) -> Optional[str]:
        """
        Fetch weather information for a given place
        Returns a natural language description of the weather
        """
        try:
            # Step 1: Get coordinates for the place
            location = await self.geo_repo.get_coordinates(place_name)
            if not location:
                return None
            
            # Step 2: Get weather data
            weather_data = await self.weather_repo.get_current_weather(location.lat, location.lon)
            if not weather_data:
                return None
            
            # Step 3: Format into natural language
            weather_desc = weather_data.to_description()
            return f"In {place_name} it's {weather_desc}."
        
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error in Weather Agent: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return None
    
    async def process_query(self, place_name: str, user_query: str) -> Optional[str]:
        """
        Process a weather-related query with AI assistance
        """
        weather_info = await self.get_weather_info(place_name)
        
        if not weather_info:
            return None
        
        # Use AI to format response according to user's query
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a weather information assistant. "
                    "Provide concise, helpful weather information based on the data given. "
                    "Keep responses natural and conversational."
                )
            },
            {
                "role": "user",
                "content": (
                    f"User asked: '{user_query}'\n"
                    f"Weather data: {weather_info}\n"
                    f"Provide a natural response to the user's query."
                )
            }
        ]
        
        try:
            response = await ai_client.chat_completion(messages, temperature=0.7)
            return response
        except Exception as e:
            # Fallback to raw data if AI fails
            logs.define_logger(
                level=30,
                message=f"AI formatting failed, using raw data: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return weather_info
