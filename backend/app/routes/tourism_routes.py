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
    - Updated conversation history
    
    Now powered by LangGraph for better orchestration and parallel execution
    Session memory enabled for contextual conversations
    """
    try:
        # Convert conversation history to dict format
        history = [{"role": msg.role, "content": msg.content} 
                   for msg in query.conversation_history] if query.conversation_history else []
        
        # Process query through LangGraph workflow
        result = await tourism_agent.process_query(query.query, history)
        
        # Build updated conversation history
        updated_history = history.copy()
        updated_history.append({"role": "user", "content": query.query})
        updated_history.append({"role": "assistant", "content": result["final_response"]})
        
        # Convert back to ConversationMessage objects
        from app.models.agent_models import ConversationMessage
        conversation_messages = [ConversationMessage(**msg) for msg in updated_history]
        
        # Convert reasoning trace and suggestions
        from app.models.agent_models import ReasoningStep, ProactiveSuggestion
        reasoning_steps = [ReasoningStep(**step) for step in result.get("reasoning_trace", [])]
        suggestions = [ProactiveSuggestion(**sug) for sug in result.get("suggestions", [])]
        
        return AgentResponse(
            location=result["location"],
            weather_info=result["weather_info"],
            places_info=result["places_info"],
            final_response=result["final_response"],
            conversation_history=conversation_messages,
            reasoning_trace=reasoning_steps,
            suggestions=suggestions
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
