from fastapi import APIRouter
from app.models.schemas import RegisterRequest
from app.services.user_service import save_github_username

router = APIRouter()

@router.post("/register")
async def register(body: RegisterRequest):
    await save_github_username(body.user_id,body.github_username)
    return{"success": True}