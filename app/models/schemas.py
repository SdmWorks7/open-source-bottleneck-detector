from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    success: bool
    message_id: int

class RegisterRequest(BaseModel):
    user_id: int
    github_username: str

class AnalyzeRequest(BaseModel):
    user_id: int