"""
Tourism Routes - API endpoints for the tourism chatbot
"""
from fastapi import APIRouter, HTTPException
from app.models.agent_models import UserQuery, AgentResponse
from app.services.langgraph_tourism import langgraph_tourism_agent
from app.core.logger import logs
import inspect

router = APIRouter(prefix="/api/tourism", tags=["Tourism"])

# Using LangGraph-based tourism agent
tourism_agent = langgraph_tourism_agent

@router.post("/chat", response_model=AgentResponse)
async def chat_with_tourism_agent(query: UserQuery):
    """
    Main endpoint for tourism chatbot using LangGraph
    
    Accepts a user query and returns:
    - Location information
    - Weather information (if requested)
    - Tourist attractions (if requested)
    - Natural language response
    
    Now powered by LangGraph for better orchestration and parallel execution
    """
    try:
        # Process query through LangGraph workflow
        result = await tourism_agent.process_query(query.query)
        
        return AgentResponse(
            location=result["location"],
            weather_info=result["weather_info"],
            places_info=result["places_info"],
            final_response=result["final_response"]
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
