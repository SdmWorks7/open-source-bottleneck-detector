from fastapi import APIRouter
from app.services.analysis_service import run_analysis
from app.models.schemas import AnalyzeRequest

router=APIRouter()

@router.post("/analyze")
async def analyze(body: AnalyzeRequest):
    return await run_analysis(body.user_id)