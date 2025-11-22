from pydantic import BaseModel
from typing import List, Optional

class ConversationMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class UserQuery(BaseModel):
    query: str
    conversation_history: Optional[List[ConversationMessage]] = []

class ReasoningStep(BaseModel):
    agent: str  # Name of the agent/node
    action: str  # What it's doing
    reason: str  # Why it's doing this
    timestamp: Optional[str] = None

class ProactiveSuggestion(BaseModel):
    text: str
    query: str  # The query to send if user clicks this suggestion

class AgentResponse(BaseModel):
    location: str
    weather_info: Optional[str] = None
    places_info: Optional[List[str]] = None
    final_response: str
    conversation_history: List[ConversationMessage]
    reasoning_trace: Optional[List[ReasoningStep]] = []
    suggestions: Optional[List[ProactiveSuggestion]] = []
