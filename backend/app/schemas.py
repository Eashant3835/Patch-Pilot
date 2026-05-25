from pydantic import BaseModel
from typing import Optional

class AgentRequest(BaseModel):
    task: str
    history: list
    file: Optional[str] = None