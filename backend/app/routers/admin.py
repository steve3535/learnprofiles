from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_data():
    """Données pour le dashboard admin"""

@router.post("/questions")
async def manage_questions(question: Question):
    """Gestion des questions (ajout/modification)"""

@router.get("/reports")
async def get_reports(session_id: int = None):
    """Génération des rapports""" 