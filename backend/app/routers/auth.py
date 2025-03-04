from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserSignup(BaseModel):
    email: EmailStr

@router.post("/signup")
async def signup(user_data: UserSignup):
    """Inscription d'un nouvel étudiant"""
    # Logique d'inscription et envoi du code d'accès par email

@router.post("/login")
async def login(access_code: str):
    """Login avec le code d'accès""" 