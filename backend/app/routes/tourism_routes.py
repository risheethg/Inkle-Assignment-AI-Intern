"""
Tourism Routes - API endpoints for the tourism chatbot
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.agent_models import UserQuery, AgentResponse
from app.services.langgraph_tourism import langgraph_tourism_agent
from app.core.logger import logs
import inspect
import json
import asyncio

router = APIRouter(prefix="/api/tourism", tags=["Tourism"])

# Using LangGraph-based tourism agent
tourism_agent = langgraph_tourism_agent

@router.post("/chat/stream")
async def chat_with_streaming(query: UserQuery):
    """
    Streaming endpoint that sends real-time reasoning updates via SSE
    """
    async def event_generator():
        try:
            # Convert conversation history
            history = [{"role": msg.role, "content": msg.content} 
                       for msg in query.conversation_history] if query.conversation_history else []
            
            # Create a queue to receive reasoning updates
            reasoning_queue = asyncio.Queue()
            
            # Process query with streaming callback
            async def reasoning_callback(step):
                await reasoning_queue.put(step)
            
            # Start processing in background
            process_task = asyncio.create_task(
                tourism_agent.process_query_streaming(
                    query.query, 
                    history,
                    reasoning_callback
                )
            )
            
            # Stream reasoning steps as they come
            while not process_task.done() or not reasoning_queue.empty():
                try:
                    step = await asyncio.wait_for(reasoning_queue.get(), timeout=0.1)
                    yield f"data: {json.dumps({'type': 'reasoning', 'data': step})}\n\n"
                except asyncio.TimeoutError:
                    continue
            
            # Get final result
            result = await process_task
            
            # Build conversation history
            updated_history = history.copy()
            updated_history.append({"role": "user", "content": query.query})
            updated_history.append({"role": "assistant", "content": result["final_response"]})
            
            # Send final response
            final_data = {
                'type': 'complete',
                'data': {
                    'location': result["location"],
                    'weather_info': result.get("weather_info"),
                    'places_info': result.get("places_info", []),
                    'final_response': result["final_response"],
                    'suggestions': result.get("suggestions", []),
                    'conversation_history': updated_history
                }
            }
            yield f"data: {json.dumps(final_data)}\n\n"
            
        except Exception as e:
            error_data = {'type': 'error', 'message': str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

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
