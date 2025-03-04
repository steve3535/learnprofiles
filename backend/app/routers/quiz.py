from fastapi import APIRouter, Depends
from typing import List

router = APIRouter()

@router.get("/questions")
async def get_questions(session_id: int):
    """Récupère les questions du quiz"""

@router.post("/responses")
async def save_responses(session_id: int, responses: List[Response]):
    """Sauvegarde les réponses"""

@router.get("/results/{session_id}")
async def get_results(session_id: int):
    """Génère les résultats du quiz""" 