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
    query_type: str | None  # 'detailed_places', 'simple', or 'weather_focused'
    is_complex_query: bool  # Whether query requires multi-step planning
    execution_plan: list[str] | None  # Steps to execute autonomously
    weather_info: str | None
    places_info: list[str] | None
    travel_tips: str | None  # Additional travel tips for complex queries
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
- query_type: Classify the query as one of:
  * "detailed_places" - User asks about places/attractions/spots/things to do/visit (keywords: places, attractions, visit, spots, things to do, tourist, sights, landmarks)
  * "weather_focused" - ONLY if asking JUST about weather with no places mentioned
  * "simple" - Everything else (general questions, trip planning, casual queries)

IMPORTANT: If needs_places is true, query_type should be "detailed_places"

Examples:
{{"location": "Paris", "needs_weather": false, "needs_places": true, "query_type": "detailed_places"}}
{{"location": "Tokyo", "needs_weather": true, "needs_places": false, "query_type": "weather_focused"}}
{{"location": "London", "needs_weather": true, "needs_places": false, "query_type": "weather_focused"}}
{{"location": "Barcelona", "needs_weather": false, "needs_places": true, "query_type": "detailed_places"}}

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
            
            # Keyword-based detection for places queries
            query_lower = state['query'].lower()
            places_keywords = ['place', 'attraction', 'visit', 'spot', 'thing', 'see', 'do', 'tourist', 'sights', 'landmark']
            asking_for_places = any(keyword in query_lower for keyword in places_keywords)
            
            # Detect complex queries that need multi-step execution and structured itinerary format
            complex_keywords = ['plan', 'trip', 'weekend', 'itinerary', 'schedule', 'visit for', 'days in', 'day in', 'spend', 'vacation', 'travel to']
            multi_day_keywords = ['days', 'day', 'weekend', 'week']
            
            is_complex = any(keyword in query_lower for keyword in complex_keywords)
            has_duration = any(keyword in query_lower for keyword in multi_day_keywords)
            
            # Determine query type and format
            query_type = analysis.get("query_type", "simple")
            needs_places = analysis.get("needs_places", False) or asking_for_places
            
            # Complex queries with duration get multi-step format, simple place queries get detailed_places
            if is_complex and has_duration:
                query_type = "multi_step_itinerary"
            elif needs_places and not is_complex:
                query_type = "detailed_places"
            
            logs.define_logger(
                level=20,
                message=f"Analysis result - query: '{state['query']}', needs_places: {needs_places}, query_type: {query_type}, is_complex: {is_complex}",
                loggName=inspect.stack()[0]
            )
            
            return {
                **state,
                "location": analysis.get("location"),
                "needs_weather": analysis.get("needs_weather", False),
                "needs_places": needs_places,
                "query_type": query_type,
                "is_complex_query": is_complex,
                "execution_plan": None,
                "travel_tips": None
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
                "needs_places": True,
                "query_type": "simple",
                "is_complex_query": False,
                "execution_plan": None,
                "travel_tips": None
            }
    
    async def planning_node(self, state: TourismState) -> TourismState:
        """Generate autonomous execution plan for complex queries"""
        if not state.get("is_complex_query"):
            return state
        
        try:
            logs.define_logger(
                level=20,
                message=f"Creating execution plan for complex query: {state['query']}",
                loggName=inspect.stack()[0]
            )
            
            prompt = f"""You are a travel planning AI. The user asked: "{state['query']}"

Create a concise execution plan that breaks this down into autonomous steps.

Return a JSON object with:
- execution_plan: array of 3-4 specific steps (e.g., ["Check weather forecast", "Find top 5 attractions", "Suggest day-by-day itinerary"])
- travel_tips: brief travel tip for this destination (1-2 sentences)

Example: {{"execution_plan": ["Check weather", "Find attractions", "Create itinerary"], "travel_tips": "Book accommodations in advance during peak season."}}

Return ONLY the JSON, no other text."""

            response = await ai_client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            
            # Parse response
            cleaned_response = response.strip()
            if cleaned_response.startswith("```"):
                lines = cleaned_response.split("\n")
                cleaned_response = "\n".join([l for l in lines if not l.startswith("```")])
            
            plan_data = json.loads(cleaned_response.strip())
            
            logs.define_logger(
                level=20,
                message=f"Generated plan: {plan_data.get('execution_plan')}",
                loggName=inspect.stack()[0]
            )
            
            return {
                **state,
                "execution_plan": plan_data.get("execution_plan", []),
                "travel_tips": plan_data.get("travel_tips"),
                "needs_weather": True,  # Complex queries always need weather
                "needs_places": True     # And places
            }
            
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error creating plan: {str(e)}",
                loggName=inspect.stack()[0]
            )
            # Fallback plan
            return {
                **state,
                "execution_plan": ["Check weather", "Find top attractions", "Provide recommendations"],
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
                limit=5
            )
            
            # places is already a list of names
            place_names = places if isinstance(places, list) else []
            
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
            
            # Get query type and data availability
            query_type = state.get("query_type", "simple")
            has_weather = state.get("weather_info") is not None
            has_places = state.get("places_info") and len(state["places_info"]) > 0
            is_complex = state.get("is_complex_query", False)
            execution_plan = state.get("execution_plan")
            travel_tips = state.get("travel_tips")
            
            # Log for debugging
            logs.define_logger(
                level=20,
                message=f"Synthesize - query_type: {query_type}, is_complex: {is_complex}, has_places: {has_places}, has_weather: {has_weather}",
                loggName=inspect.stack()[0]
            )
            
            # Build response based on query type - dynamic format selection
            if query_type == "multi_step_itinerary" and execution_plan:
                # Multi-step execution format - structured itinerary planning
                plan_items = "\n".join([f"{i+1}. {step}" for i, step in enumerate(execution_plan)])
                places_list = "\n".join([f"- {place}" for place in state["places_info"]]) if state.get("places_info") else "- Exploring local attractions"
                
                prompt = f"""You are TravelMate, a professional travel itinerary planner.

User Query: {state['query']}

Available Information:
- Location: {state.get('location', 'Unknown')}
- Weather: {state.get('weather_info', 'Weather data unavailable')}
- Top Attractions:
{places_list}

Execution Steps:
{plan_items}

Travel Tips: {travel_tips or "Travel smart and enjoy your journey!"}

Create a STRUCTURED multi-day itinerary following this EXACT format:

---
**🌤️ WEATHER OVERVIEW**
{state.get('weather_info', 'Check local weather before departure')}

**📍 TOP ATTRACTIONS**
List the attractions as bullet points, each on its own line.

**📅 YOUR ITINERARY**

**Day 1: [Theme/Focus]**
- Morning: [Activity/Location]
- Afternoon: [Activity/Location]
- Evening: [Activity/Location]

**Day 2: [Theme/Focus]**
- Morning: [Activity/Location]
- Afternoon: [Activity/Location]
- Evening: [Activity/Location]

(Continue for all days mentioned in the query)

**💡 TRAVEL TIPS**
{travel_tips}

**✨ FINAL THOUGHTS**
Brief encouraging conclusion about their trip.
---

CRITICAL RULES:
1. Use clear section headers with emojis
2. Create day-by-day breakdown with specific times
3. Incorporate the provided attractions into daily activities
4. Keep each day balanced (morning, afternoon, evening)
5. Be specific about what to do when
6. Professional but warm tone
7. End with encouragement

Generate the complete structured itinerary now:"""

                temperature = 0.5
                
            elif query_type == "detailed_places" and has_places:
                # User explicitly asked for places - use structured format
                prompt = f"""You are TravelMate, an enthusiastic and helpful travel assistant.

{context}

The user specifically asked about places to visit. Generate a response following this EXACT structure:

Hello there! [Location] is a fantastic choice, you're going to have a wonderful time!

Let's get you up to speed:

**Weather:** [Weather description]

And speaking of exploring, [Location] has some great spots you might enjoy:

* **[Attraction Name 1]**
* **[Attraction Name 2]**
* **[Attraction Name 3]**
* **[Attraction Name 4]**
* **[Attraction Name 5]**

Enjoy your trip to [Location]! Let me know if you need anything else!

CRITICAL RULES - FOLLOW EXACTLY:
1. List ONLY attraction names - NO descriptions, NO explanations, NO details
2. Format: * **Name** (nothing else on that line)
3. Do NOT write about what they are or why they're good
4. Do NOT add any text after the attraction name
5. Just the name in bold with the asterisk bullet point

Example of CORRECT format:
* **Eiffel Tower**
* **Louvre Museum**

Example of WRONG format (DO NOT DO THIS):
* **Eiffel Tower** - it's incredible and a great way to warm up!

Remember: JUST THE NAMES, nothing more."""

                temperature = 0.3
                
            elif query_type == "weather_focused":
                # Weather-focused query - natural but informative
                prompt = f"""You are TravelMate, a friendly travel assistant.

{context}

The user is primarily interested in weather. Respond naturally and conversationally.

Guidelines:
- Focus on weather information, be specific about temperature and conditions
- Keep it concise and friendly
- If places are available, mention them briefly and casually
- End with a helpful offer (e.g., "Would you like to know about places to visit?")
- Natural language, no rigid formatting"""

                temperature = 0.8
                
            else:
                # Simple/casual query - fully natural conversation
                prompt = f"""You are TravelMate, a friendly travel assistant having a natural conversation.

{context}

Respond in a natural, conversational way - like chatting with a knowledgeable friend.

Guidelines:
- Be concise and casual
- If providing weather, mention it naturally (e.g., "It's around 22°C with some clouds")
- If listing places, weave them into conversation naturally (e.g., "You should check out the Eiffel Tower, Louvre, and Notre-Dame")
- No bullet points or rigid structure unless you have many items (5+)
- Keep it brief and friendly
- End casually

Just chat naturally - no formal formatting needed."""

                temperature = 0.8

            response = await ai_client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            
            logs.define_logger(
                level=20,
                message=f"AI response received - length: {len(response) if response else 0} chars",
                loggName=inspect.stack()[0]
            )
            
            if not response or not response.strip():
                logs.define_logger(
                    level=40,
                    message="AI returned empty response! Check API key and prompt.",
                    loggName=inspect.stack()[0]
                )
                return {**state, "final_response": "I apologize, but I couldn't generate a response. Please try again."}
            
            return {**state, "final_response": response.strip()}
            
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error synthesizing response: {str(e)}",
                loggName=inspect.stack()[0]
            )
            return {**state, "final_response": "I apologize, but I encountered an error generating your response."}
    
    # ========== ROUTING LOGIC ==========
    
    def route_after_analysis(self, state: TourismState) -> Literal["planning", "fetch_data", "synthesize"]:
        """Determine next step after query analysis"""
        if state.get("error"):
            return "synthesize"
        
        # Complex queries need multi-step planning
        if state.get("is_complex_query"):
            logs.define_logger(
                level=20,
                message="Routing to planning node for complex query",
                loggName=inspect.stack()[0]
            )
            return "planning"
        
        # Simple data queries fetch directly
        if state.get("needs_weather") or state.get("needs_places"):
            return "fetch_data"
        
        # General queries skip data fetching
        return "synthesize"
    
    # ========== GRAPH CONSTRUCTION ==========
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(TourismState)
        
        # Add nodes
        workflow.add_node("analyze", self.analyze_query_node)
        workflow.add_node("planning", self.planning_node)
        workflow.add_node("weather", self.weather_node)
        workflow.add_node("places", self.places_node)
        workflow.add_node("synthesize", self.synthesize_node)
        
        # Set entry point
        workflow.set_entry_point("analyze")
        
        # Add conditional routing after analysis - complex queries go through planning
        workflow.add_conditional_edges(
            "analyze",
            self.route_after_analysis,
            {
                "planning": "planning",  # Complex queries need multi-step planning
                "fetch_data": "weather",  # Simple queries fetch data directly
                "synthesize": "synthesize"  # General queries skip data fetching
            }
        )
        
        # After planning, fetch data
        workflow.add_edge("planning", "weather")
        
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
                "query_type": None,
                "weather_info": None,
                "places_info": None,
                "final_response": None,
                "error": None,
                "is_complex_query": False,
                "execution_plan": None,
                "travel_tips": None
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
