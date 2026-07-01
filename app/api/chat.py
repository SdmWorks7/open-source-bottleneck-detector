from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.message_service import save_message
from app.services.memory_service import save_memories, extract_memories

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    message_id = await save_message(body.user_id, body.message)
    memories = extract_memories(body.message)
    await save_memories(body.user_id, memories)
    return{"success": True, "message_id":message_id}
    