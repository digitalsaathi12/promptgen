import uuid
from typing import Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class AIModel(Base):
    __tablename__ = "ai_models"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False) # e.g. "llama3"
    provider: Mapped[str] = mapped_column(String(50), nullable=False) # ollama, openai, gemini, anthropic, deepseek, grok
    is_local: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    default_for: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # "text", "image", or null
