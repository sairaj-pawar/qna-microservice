from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..models.question import QuestionStatus


class QuestionCreate(BaseModel):
    question: str = Field(..., min_length=1, description="Question about the document")


class QuestionResponse(BaseModel):
    id: int
    document_id: int
    question: str
    answer: Optional[str] = None
    status: QuestionStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 