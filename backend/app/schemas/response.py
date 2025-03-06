from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResponseBase(BaseModel):
    question_id: int
    answer_text: Optional[str] = None
    answer_value: Optional[int] = None


class ResponseCreate(ResponseBase):
    pass


class ResponseUpdate(ResponseBase):
    question_id: Optional[int] = None


class ResponseInDBBase(ResponseBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class Response(ResponseInDBBase):
    pass


class ResponseWithQuestion(Response):
    question: "Question"

# Avoid circular imports
from app.schemas.question import Question
ResponseWithQuestion.update_forward_refs() 