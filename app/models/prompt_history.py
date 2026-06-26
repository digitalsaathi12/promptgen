import uuid
import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class PromptHistory(Base):
    __tablename__ = "prompt_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    generator_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("generators.id", ondelete="SET NULL"), nullable=True)
    input_payload: Mapped[dict] = mapped_column(JSON, nullable=False) # raw form values
    constructed_prompt: Mapped[str] = mapped_column(Text, nullable=False) # fully compiled prompt
    ai_model_used: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "llama3" or "gpt-4"
    output: Mapped[dict] = mapped_column(JSON, nullable=False) # multi-section prompt outputs
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="prompt_histories")
    generator: Mapped[Optional["Generator"]] = relationship("Generator", back_populates="prompt_histories")
    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="prompt_history", cascade="all, delete-orphan")
