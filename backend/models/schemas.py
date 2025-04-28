from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    context_used: List[str]
    tokens_used: int

class UsageLog(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    prompt: str
    response: str
    tokens_used: int

    class Config:
        from_attributes = True
