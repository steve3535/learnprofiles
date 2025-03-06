from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.question import QuestionType


class QuestionBase(BaseModel):
    text: str
    category: str
    type: QuestionType
    options: Optional[str] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    text: Optional[str] = None
    category: Optional[str] = None
    type: Optional[QuestionType] = None


class QuestionInDBBase(QuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class Question(QuestionInDBBase):
    pass


class QuestionWithOptions(Question):
    parsed_options: Optional[List[Dict[str, Any]]] = None 