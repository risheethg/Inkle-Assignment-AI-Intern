"""
Tourism Routes - API endpoints for the tourism chatbot
"""
from fastapi import APIRouter, HTTPException
from app.models.agent_models import UserQuery, AgentResponse
from app.services.tourism_agent import TourismAgent
from app.core.logger import logs
import inspect

router = APIRouter(prefix="/api/tourism", tags=["Tourism"])

# Initialize tourism agent
tourism_agent = TourismAgent()

@router.post("/chat", response_model=AgentResponse)
async def chat_with_tourism_agent(query: UserQuery):
    """
    Main endpoint for tourism chatbot
    
    Accepts a user query and returns:
    - Location information
    - Weather information (if requested)
    - Tourist attractions (if requested)
    - Natural language response
    """
    try:
        # Process query through tourism agent
        final_response = await tourism_agent.process_query(query.query)
        
        # Get analysis for response structure
        analysis = await tourism_agent.analyze_query(query.query)
        place_name = analysis.get("place", "Unknown")
        
        # Gather structured data
        weather_info = None
        places_info = None
        
        if analysis.get("wants_weather"):
            weather_info = await tourism_agent.weather_agent.get_weather_info(place_name)
        
        if analysis.get("wants_places"):
            places = await tourism_agent.places_agent.get_tourist_places(place_name)
            places_info = places
        
        return AgentResponse(
            location=place_name,
            weather_info=weather_info,
            places_info=places_info,
            final_response=final_response
        )
    
    except Exception as e:
        logs.define_logger(
            level=40,
            message=f"Error in chat endpoint: {str(e)}",
            loggName=inspect.stack()[0]
        )
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again."
        )

@router.get("/health", tags=["Health"])
async def health_check():
    """Check if the tourism service is running"""
    return {
        "status": "healthy",
        "service": "Tourism AI Agent",
        "agents": {
            "parent": tourism_agent.name,
            "weather": tourism_agent.weather_agent.name,
            "places": tourism_agent.places_agent.name
        }
    }
