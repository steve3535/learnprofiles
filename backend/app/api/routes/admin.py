from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.api.dependencies import get_db, get_current_admin_user
from app.models.user import User
from app.models.question import Question, QuestionType
from app.models.response import Response
from app.schemas.question import QuestionCreate, QuestionUpdate, Question as QuestionSchema
from app.schemas.user import User as UserSchema
from app.schemas.response import Response as ResponseSchema

router = APIRouter(prefix="/admin")


@router.get("/users", response_model=List[UserSchema])
def get_users(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all users (admin only).
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/questions", response_model=QuestionSchema)
def create_question(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    question_in: QuestionCreate,
) -> Any:
    """
    Create a new question (admin only).
    """
    # Validate options for multiple choice questions
    if question_in.type == QuestionType.MULTIPLE_CHOICE and not question_in.options:
        raise HTTPException(
            status_code=400,
            detail="Multiple choice questions must have options"
        )
    
    # Validate min/max for gauge questions
    if question_in.type == QuestionType.GAUGE:
        if question_in.min_value is None or question_in.max_value is None:
            raise HTTPException(
                status_code=400,
                detail="Gauge questions must have min and max values"
            )
        if question_in.min_value >= question_in.max_value:
            raise HTTPException(
                status_code=400,
                detail="Min value must be less than max value"
            )
    
    # Create question
    db_question = Question(
        text=question_in.text,
        category=question_in.category,
        type=question_in.type,
        options=question_in.options,
        min_value=question_in.min_value,
        max_value=question_in.max_value,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return db_question


@router.put("/questions/{question_id}", response_model=QuestionSchema)
def update_question(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    question_id: int,
    question_in: QuestionUpdate,
) -> Any:
    """
    Update a question (admin only).
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Update fields if provided
    update_data = question_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    
    return question


@router.delete("/questions/{question_id}", response_model=QuestionSchema)
def delete_question(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    question_id: int,
) -> Any:
    """
    Delete a question (admin only).
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Delete associated responses
    db.query(Response).filter(Response.question_id == question_id).delete()
    
    # Delete question
    db.delete(question)
    db.commit()
    
    return question


@router.get("/dashboard", response_model=dict)
def get_dashboard_data(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Get dashboard data with user statistics (admin only).
    """
    # Count total users
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    # Count total questions by category
    categories = db.query(Question.category, db.func.count(Question.id)).group_by(Question.category).all()
    category_counts = {category: count for category, count in categories}
    
    # Get average scores by category
    from sqlalchemy import func
    
    category_scores = {}
    for category in category_counts.keys():
        # Get questions in this category
        category_questions = db.query(Question).filter(Question.category == category).all()
        question_ids = [q.id for q in category_questions]
        
        if not question_ids:
            continue
        
        # Calculate average score for this category across all users
        avg_score = db.query(
            func.avg(Response.answer_value)
        ).filter(
            Response.question_id.in_(question_ids),
            Response.answer_value.isnot(None)
        ).scalar()
        
        if avg_score is not None:
            category_scores[category] = round(float(avg_score), 2)
        else:
            category_scores[category] = 0
    
    # Get recent responses
    recent_responses = db.query(Response).order_by(Response.created_at.desc()).limit(10).all()
    recent_response_data = []
    
    for response in recent_responses:
        user = db.query(User).filter(User.id == response.user_id).first()
        question = db.query(Question).filter(Question.id == response.question_id).first()
        
        if user and question:
            recent_response_data.append({
                "user_email": user.email,
                "question_category": question.category,
                "question_type": question.type,
                "answer_value": response.answer_value,
                "created_at": response.created_at
            })
    
    return {
        "user_stats": {
            "total": total_users,
            "active": active_users
        },
        "question_stats": category_counts,
        "category_scores": category_scores,
        "recent_responses": recent_response_data
    }


@router.post("/users/{user_id}/make-admin", response_model=UserSchema)
def make_user_admin(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    user_id: int,
) -> Any:
    """
    Make a user an admin (admin only).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = True
    db.commit()
    db.refresh(user)
    
    return user 