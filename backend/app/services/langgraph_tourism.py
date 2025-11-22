"""
LangGraph Tourism Agent System
Multi-agent workflow using LangGraph for better state management and parallel execution
"""
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
import operator
import json

from app.services.ai_client import ai_client
from app.repos.geo_repo import GeoRepo
from app.repos.weather_repo import WeatherRepo
from app.repos.places_repo import PlacesRepo
from app.core.logger import logs
import inspect


# Define the shared state
class TourismState(TypedDict):
    """Shared state that flows through the graph"""
    query: str
    conversation_history: list[dict] | None  # Store previous conversation
    location: str | None
    needs_weather: bool
    needs_places: bool
    weather_info: str | None
    places_info: list[str] | None
    final_response: str | None
    error: str | None


class LangGraphTourismAgent:
    """Tourism agent system using LangGraph for orchestration"""
    
    def __init__(self):
        self.geo_repo = GeoRepo()
        self.weather_repo = WeatherRepo()
        self.places_repo = PlacesRepo()
        self.graph = self._build_graph()
    
    # ========== NODE FUNCTIONS ==========
    
    async def analyze_query_node(self, state: TourismState) -> TourismState:
        """Analyze the user query to determine intent and extract location"""
        try:
            logs.define_logger(
                level=20,
                message=f"Analyzing query: {state['query']}",
                loggName=inspect.stack()[0]
            )
            
            # Build context from conversation history
            context = ""
            if state.get('conversation_history') and len(state['conversation_history']) > 0:
                context = "\n\nPrevious conversation context:\n"
                for msg in state['conversation_history'][-4:]:  # Last 4 messages for context
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    context += f"{role}: {content}\n"
            
            prompt = f"""Analyze this tourism query and extract information in JSON format.
{context}
Current Query: "{state['query']}"

Important: If the current query refers to previous context (e.g., "that place", "there", "it"), extract the location from the conversation history above.

Return a JSON object with:
- location: The city/place name mentioned or referenced (string or null)
- needs_weather: true if asking about weather/temperature/climate
- needs_places: true if asking about places to visit/attractions/things to do

Example: {{"location": "Paris", "needs_weather": true, "needs_places": true}}

Return ONLY the JSON, no other text."""

            response = await ai_client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Clean the response - remove markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```"):
                # Remove markdown code blocks
                lines = cleaned_response.split("\n")
                cleaned_response = "\n".join([l for l in lines if not l.startswith("```")])
            
            # Try to find JSON in the response
            try:
                analysis = json.loads(cleaned_response.strip())
            except:
                # If JSON parsing fails, try to extract JSON from text
                import re
                json_match = re.search(r'\{[^}]+\}', cleaned_response)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            return {
                **state,
                "location": analysis.get("location"),
                "needs_weather": analysis.get("needs_weather", False),
                "needs_places": analysis.get("needs_places", False)
            }
            
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error analyzing query: {str(e)}",
                loggName=inspect.stack()[0]
            )
            # Fallback: assume user wants both weather and places for any mentioned location
            query_lower = state['query'].lower()
            location = None
            # Simple location extraction
            for word in state['query'].split():
                if len(word) > 3 and word[0].isupper():
                    location = word.rstrip('?,.')
                    break
            
            return {
                **state,
                "location": location,
                "needs_weather": True,
                "needs_places": True
            }
    
    async def weather_node(self, state: TourismState) -> TourismState:
        """Fetch weather information for the location"""
        if not state.get("location") or not state.get("needs_weather"):
            return state
        
        try:
            logs.define_logger(
                level=20,
                message=f"Fetching weather for: {state['location']}",
                loggName=inspect.stack()[0]
            )
            
            # Get coordinates
            coords = await self.geo_repo.get_coordinates(state["location"])
            if not coords:
                return {**state, "weather_info": "Location not found"}
            
            # Get weather
            weather = await self.weather_repo.get_current_weather(
                coords.lat, 
                coords.lon
            )
            
            if not weather:
                return {**state, "weather_info": "Weather data not available"}
            
            # Format weather info
            precip = weather.precipitation_probability if weather.precipitation_probability else 0
            weather_text = f"In {state['location']} it's currently {weather.temperature}°C with a {precip:.1f}% chance of rain."
            
            return {**state, "weather_info": weather_text}
            
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error fetching weather: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return {**state, "weather_info": f"Could not fetch weather: {str(e)}"}
    
    async def places_node(self, state: TourismState) -> TourismState:
        """Fetch tourist attractions for the location"""
        if not state.get("location") or not state.get("needs_places"):
            return state
        
        try:
            logs.define_logger(
                level=20,
                message=f"Fetching places for: {state['location']}",
                loggName=inspect.stack()[0]
            )
            
            # Get coordinates
            coords = await self.geo_repo.get_coordinates(state["location"])
            if not coords:
                return {**state, "places_info": []}
            
            # Get places
            places = await self.places_repo.get_tourist_attractions(
                coords.lat,
                coords.lon,
                radius=5000
            )
            
            place_names = [place["name"] for place in places[:5]]
            
            return {**state, "places_info": place_names}
            
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error fetching places: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return {**state, "places_info": []}
    
    async def synthesize_node(self, state: TourismState) -> TourismState:
        """Generate the final response using all gathered information"""
        try:
            logs.define_logger(
                level=20,
                message="Synthesizing final response",
                loggName=inspect.stack()[0]
            )
            
            # Build context for the AI
            context_parts = []
            
            # Add conversation history for context
            if state.get('conversation_history') and len(state['conversation_history']) > 0:
                context_parts.append("Previous conversation:")
                for msg in state['conversation_history'][-4:]:  # Last 4 messages
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')[:200]  # Limit length
                    context_parts.append(f"{role}: {content}")
                context_parts.append("")  # Empty line separator
            
            context_parts.append(f"Current query: {state['query']}")
            
            if state.get("location"):
                context_parts.append(f"Location: {state['location']}")
            
            if state.get("weather_info"):
                context_parts.append(f"Weather: {state['weather_info']}")
            
            if state.get("places_info") and len(state["places_info"]) > 0:
                places_list = "\n".join([f"- {place}" for place in state["places_info"]])
                context_parts.append(f"Top attractions:\n{places_list}")
            
            context = "\n\n".join(context_parts)
            
            # Determine if this is a follow-up query or initial query
            has_history = state.get('conversation_history') and len(state['conversation_history']) > 0
            has_weather = state.get("weather_info") is not None
            has_places = state.get("places_info") and len(state["places_info"]) > 0
            
            # Build a natural, adaptive prompt
            if has_history:
                # Follow-up conversation - be more conversational and brief
                prompt = f"""You are TravelMate, a friendly and helpful travel assistant having an ongoing conversation.

{context}

Respond naturally as if continuing a conversation. Keep it concise and conversational.

Guidelines:
- Reference previous context naturally if relevant
- If providing weather, mention it conversationally (e.g., "It's about 22°C with some rain expected")
- If listing places, integrate them naturally (e.g., "You might enjoy checking out [place1], [place2], and [place3]")
- Don't use rigid formatting or bullet points unless you have 4+ attractions
- Keep the tone warm but not overly enthusiastic
- End casually (e.g., "Let me know if you'd like more details!" or "Anything else you'd like to know?")

Be helpful but natural - like texting a knowledgeable friend."""
            else:
                # Initial query - provide more structured information
                if has_weather and has_places:
                    prompt = f"""You are TravelMate, a friendly travel assistant. This is the start of a new conversation.

{context}

Provide a helpful, structured response that covers both weather and attractions.

Structure your response like this:
1. Warm greeting mentioning the location
2. Weather information in a natural way (e.g., "The weather is looking nice - around 22°C with partly cloudy skies...")
3. Top attractions listed clearly (use simple formatting like numbered list or bullet points)
4. Friendly closing

Keep it informative but conversational. Use the attraction names provided without adding descriptions."""
                elif has_weather:
                    prompt = f"""You are TravelMate, a friendly travel assistant.

{context}

Provide weather information in a natural, conversational way. Be concise and friendly.
Include the temperature and conditions, then ask if they'd like to know about places to visit."""
                elif has_places:
                    prompt = f"""You are TravelMate, a friendly travel assistant.

{context}

Share the top attractions in a clear, friendly way. List them simply (numbered or bulleted).
Use only the attraction names provided. End with an offer to help with more information."""
                else:
                    prompt = f"""You are TravelMate, a friendly travel assistant.

{context}

Respond naturally to the query. Be helpful and conversational."""

            response = await ai_client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8 if has_history else 0.7
            )
            
            return {**state, "final_response": response.strip()}
            
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error synthesizing response: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return {**state, "final_response": "I apologize, but I encountered an error generating your response."}
    
    # ========== ROUTING LOGIC ==========
    
    def should_fetch_data(self, state: TourismState) -> Literal["fetch_data", "synthesize"]:
        """Determine if we need to fetch weather/places data"""
        if state.get("error"):
            return "synthesize"
        
        if state.get("needs_weather") or state.get("needs_places"):
            return "fetch_data"
        
        return "synthesize"
    
    # ========== GRAPH CONSTRUCTION ==========
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(TourismState)
        
        # Add nodes
        workflow.add_node("analyze", self.analyze_query_node)
        workflow.add_node("weather", self.weather_node)
        workflow.add_node("places", self.places_node)
        workflow.add_node("synthesize", self.synthesize_node)
        
        # Set entry point
        workflow.set_entry_point("analyze")
        
        # Add conditional routing after analysis
        workflow.add_conditional_edges(
            "analyze",
            self.should_fetch_data,
            {
                "fetch_data": "weather",  # Go to weather first
                "synthesize": "synthesize"  # Skip data fetching
            }
        )
        
        # Weather and Places can run in parallel conceptually,
        # but we chain them here for simplicity
        workflow.add_edge("weather", "places")
        workflow.add_edge("places", "synthesize")
        workflow.add_edge("synthesize", END)
        
        return workflow.compile()
    
    # ========== PUBLIC API ==========
    
    async def process_query(self, query: str, conversation_history: list[dict] = None) -> dict:
        """
        Process a tourism query through the LangGraph workflow
        
        Args:
            query: User's tourism question
            conversation_history: List of previous messages for context
            
        Returns:
            dict with location, weather_info, places_info, and final_response
        """
        try:
            # Initialize state
            initial_state: TourismState = {
                "query": query,
                "conversation_history": conversation_history or [],
                "location": None,
                "needs_weather": False,
                "needs_places": False,
                "weather_info": None,
                "places_info": None,
                "final_response": None,
                "error": None
            }
            
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state)
            
            # Return structured response
            return {
                "location": final_state.get("location") or "Unknown",
                "weather_info": final_state.get("weather_info"),
                "places_info": final_state.get("places_info") or [],
                "final_response": final_state.get("final_response") or "I couldn't process your request."
            }
            
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error in LangGraph workflow: {str(e)}",
                loggName=inspect.stack()[0]
            )
            raise


# Singleton instance
langgraph_tourism_agent = LangGraphTourismAgent()
