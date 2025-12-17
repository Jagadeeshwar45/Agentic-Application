from pydantic import BaseModel
from typing import Optional, List, Literal

class AgentRequest(BaseModel):
    user_query: str
    file_content: Optional[str] = None  
    file_type: Optional[str] = None     
    history: List[dict] = []

class AgentResponse(BaseModel):
    response_text: str
    action_taken: str
    needs_clarification: bool = False