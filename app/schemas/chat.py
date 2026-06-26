from typing import List, Optional
from pydantic import BaseModel, Field

class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="User chat message content")
    provider: Optional[str] = Field("gpt", description="gpt, gemini, claude, ollama")

class ChatMessageResponse(BaseModel):
    response: str

class ChatMessageHistoryItem(BaseModel):
    role: str # user, assistant
    content: str
