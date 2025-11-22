from pydantic import BaseModel
from typing import List, Optional

class UserQuery(BaseModel):
    query: str

class AgentResponse(BaseModel):
    location: str
    weather_info: Optional[str] = None
    places_info: Optional[List[str]] = None
    final_response: str
