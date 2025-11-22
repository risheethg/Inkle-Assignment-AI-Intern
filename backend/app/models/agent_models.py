from pydantic import BaseModel
from typing import List, Optional

class ConversationMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class UserQuery(BaseModel):
    query: str
    conversation_history: Optional[List[ConversationMessage]] = []

class AgentResponse(BaseModel):
    location: str
    weather_info: Optional[str] = None
    places_info: Optional[List[str]] = None
    final_response: str
    conversation_history: List[ConversationMessage]
