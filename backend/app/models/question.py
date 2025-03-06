from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class QuestionType(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_ENDED = "open_ended"
    GAUGE = "gauge"


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    category = Column(String, nullable=False, index=True)
    type = Column(Enum(QuestionType), nullable=False)
    options = Column(Text, nullable=True)  # JSON string for multiple choice options
    min_value = Column(Integer, nullable=True)  # For gauge questions
    max_value = Column(Integer, nullable=True)  # For gauge questions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 