from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.question import Question
from app.schemas.question import Question as QuestionSchema, QuestionWithOptions
import json

router = APIRouter(prefix="/questions")


@router.get("/", response_model=List[QuestionWithOptions])
def get_questions(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    category: str = None,
) -> Any:
    """
    Get all questions, optionally filtered by category.
    """
    query = db.query(Question)
    if category:
        query = query.filter(Question.category == category)
    
    questions = query.all()
    
    # Parse options for multiple choice questions
    result = []
    for q in questions:
        q_dict = QuestionSchema.from_orm(q).dict()
        if q.options:
            try:
                q_dict["parsed_options"] = json.loads(q.options)
            except json.JSONDecodeError:
                q_dict["parsed_options"] = []
        result.append(QuestionWithOptions(**q_dict))
    
    return result


@router.get("/categories", response_model=List[str])
def get_categories(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get all unique question categories.
    """
    categories = db.query(Question.category).distinct().all()
    return [category[0] for category in categories]


@router.get("/{question_id}", response_model=QuestionWithOptions)
def get_question(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    question_id: int,
) -> Any:
    """
    Get a specific question by ID.
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    q_dict = QuestionSchema.from_orm(question).dict()
    if question.options:
        try:
            q_dict["parsed_options"] = json.loads(question.options)
        except json.JSONDecodeError:
            q_dict["parsed_options"] = []
    
    return QuestionWithOptions(**q_dict) 