"""
Tourism Agent - Parent agent that orchestrates the entire tourism system
Analyzes user queries and delegates to child agents (Weather Agent, Places Agent)
"""
from typing import Dict, Any
from app.services.weather_agent import WeatherAgent
from app.services.places_agent import PlacesAgent
from app.services.ai_client import ai_client
from app.repos.geo_repo import GeoRepo
from app.core.logger import logs
import inspect
import json

class TourismAgent:
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
        self.geo_repo = GeoRepo()
        self.name = "Tourism AI Agent"
    
    async def analyze_query(self, user_query: str) -> Dict[str, Any]:
        """
        Analyze user query to determine:
        1. What place they're asking about
        2. Whether they want weather information
        3. Whether they want tourist attractions
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a query analyzer for a tourism system. "
                    "Analyze the user's query and extract:\n"
                    "1. The place/location they're asking about\n"
                    "2. Whether they want weather information (true/false)\n"
                    "3. Whether they want tourist attractions/places to visit (true/false)\n\n"
                    "Respond ONLY with a JSON object in this exact format:\n"
                    '{"place": "place name", "wants_weather": true/false, "wants_places": true/false}\n\n'
                    "Examples:\n"
                    "Query: 'I'm going to Bangalore, what is the temperature there?'\n"
                    'Response: {"place": "Bangalore", "wants_weather": true, "wants_places": false}\n\n'
                    "Query: 'I'm going to Paris, let's plan my trip.'\n"
                    'Response: {"place": "Paris", "wants_weather": false, "wants_places": true}\n\n'
                    "Query: 'What can I do in Tokyo and what's the weather like?'\n"
                    'Response: {"place": "Tokyo", "wants_weather": true, "wants_places": true}'
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        try:
            response = await ai_client.chat_completion(messages, temperature=0.3)
            # Parse JSON response
            analysis = json.loads(response.strip())
            return analysis
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error analyzing query: {str(e)}",
                loggName=inspect.stack()[0]
            )
            # Return default analysis
            return {
                "place": None,
                "wants_weather": False,
                "wants_places": True
            }
    
    async def process_query(self, user_query: str) -> str:
        """
        Main entry point - processes user query and orchestrates child agents
        """
        try:
            # Step 1: Analyze the query
            analysis = await self.analyze_query(user_query)
            place_name = analysis.get("place")
            wants_weather = analysis.get("wants_weather", False)
            wants_places = analysis.get("wants_places", False)
            
            # Step 2: Validate place exists
            if not place_name:
                return "I couldn't identify which place you're asking about. Could you please specify the location?"
            
            location = await self.geo_repo.get_coordinates(place_name)
            if not location:
                return f"I don't know if {place_name} exists or I couldn't find information about it. Please check the spelling or try a different location."
            
            # Step 3: Gather information from child agents
            weather_info = None
            places_info = None
            
            if wants_weather:
                weather_info = await self.weather_agent.get_weather_info(place_name)
            
            if wants_places:
                places = await self.places_agent.get_tourist_places(place_name)
                if places:
                    places_info = "\n".join(places)
            
            # Step 4: Generate final response
            return await self._generate_final_response(
                user_query=user_query,
                place_name=place_name,
                weather_info=weather_info,
                places_info=places_info
            )
        
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error in Tourism Agent: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return "I encountered an error processing your request. Please try again."
    
    async def _generate_final_response(
        self,
        user_query: str,
        place_name: str,
        weather_info: str = None,
        places_info: str = None
    ) -> str:
        """
        Generate final natural language response combining all information
        """
        # Build context for AI
        context_parts = []
        
        if weather_info:
            context_parts.append(f"Weather information: {weather_info}")
        
        if places_info:
            context_parts.append(f"Tourist attractions:\n{places_info}")
        
        if not context_parts:
            return f"I couldn't find any information about {place_name}."
        
        context = "\n\n".join(context_parts)
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful tourism assistant. "
                    "Combine the provided information into a natural, conversational response. "
                    "Be enthusiastic and helpful. Format lists of places clearly. "
                    "Keep the response concise but informative."
                )
            },
            {
                "role": "user",
                "content": (
                    f"User asked: '{user_query}'\n"
                    f"Location: {place_name}\n\n"
                    f"Available information:\n{context}\n\n"
                    f"Generate a natural response that addresses the user's question."
                )
            }
        ]
        
        try:
            response = await ai_client.chat_completion(messages, temperature=0.7)
            return response
        except Exception as e:
            logs.define_logger(
                level=30,
                message=f"AI response generation failed, using fallback: {str(e)}",
                loggName=inspect.stack()[0]
            )
            # Simple fallback
            parts = []
            if weather_info:
                parts.append(weather_info)
            if places_info:
                parts.append(f"These are the places you can visit:\n{places_info}")
            return " ".join(parts) if parts else f"Information about {place_name} is currently unavailable."
