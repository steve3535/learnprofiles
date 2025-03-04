from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Float, Boolean
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
    access_code = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    subcategory = Column(String)
    question_type = Column(Enum('likert', 'multiple_choice', 'boolean', 'ranking'))
    content = Column(String)
    options = Column(JSON)  # Pour les choix multiples/ranking
    weight = Column(Float)
    order = Column(Integer)

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('quiz_sessions.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer = Column(JSON)  # Stocke la réponse dans un format flexible
    score = Column(Float) 