from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.response import Response
from app.models.question import Question
from app.schemas.response import ResponseCreate, Response as ResponseSchema, ResponseWithQuestion

router = APIRouter(prefix="/responses")


@router.post("/", response_model=ResponseSchema)
def create_response(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    response_in: ResponseCreate,
) -> Any:
    """
    Create a new response to a question.
    """
    # Check if question exists
    question = db.query(Question).filter(Question.id == response_in.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if user already answered this question
    existing_response = db.query(Response).filter(
        Response.user_id == current_user.id,
        Response.question_id == response_in.question_id
    ).first()
    
    if existing_response:
        # Update existing response
        existing_response.answer_text = response_in.answer_text
        existing_response.answer_value = response_in.answer_value
        db.commit()
        db.refresh(existing_response)
        return existing_response
    
    # Create new response
    db_response = Response(
        user_id=current_user.id,
        question_id=response_in.question_id,
        answer_text=response_in.answer_text,
        answer_value=response_in.answer_value,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    return db_response


@router.get("/", response_model=List[ResponseWithQuestion])
def get_user_responses(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get all responses for the current user.
    """
    responses = db.query(Response).filter(Response.user_id == current_user.id).all()
    
    # Load questions for each response
    result = []
    for response in responses:
        question = db.query(Question).filter(Question.id == response.question_id).first()
        response_dict = ResponseSchema.from_orm(response).dict()
        response_dict["question"] = question
        result.append(ResponseWithQuestion(**response_dict))
    
    return result


@router.get("/scores", response_model=dict)
def get_user_scores(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Calculate scores by category for the current user.
    """
    # Get all user responses
    responses = db.query(Response).filter(Response.user_id == current_user.id).all()
    
    # Group responses by category
    categories = {}
    for response in responses:
        question = db.query(Question).filter(Question.id == response.question_id).first()
        if not question:
            continue
        
        if question.category not in categories:
            categories[question.category] = {
                "total": 0,
                "count": 0,
                "score": 0
            }
        
        # Add to category score based on question type
        if question.type == "multiple_choice" or question.type == "gauge":
            if response.answer_value is not None:
                categories[question.category]["total"] += response.answer_value
                categories[question.category]["count"] += 1
    
    # Calculate average score for each category
    for category in categories:
        if categories[category]["count"] > 0:
            categories[category]["score"] = round(
                categories[category]["total"] / categories[category]["count"], 2
            )
    
    return categories 