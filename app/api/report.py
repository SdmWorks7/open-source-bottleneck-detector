from fastapi import APIRouter
from fastapi import HTTPException
from app.services.report_service import get_report

router=APIRouter()

@router.get("/report/{id}")
async def report(id: int):
    repo= await get_report(id)
    if repo is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return repo 