from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.message_service import save_message
from app.services.cognee_service import remember_message

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    message_id = await save_message(body.user_id, body.message)
    await remember_message(body.user_id, body.message)
    return{"success": True, "message_id":message_id}
    