import datetime
from sqlalchemy import Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class GeneratedContent(Base):
    __tablename__ = "generated_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    input: Mapped[str] = mapped_column(Text, nullable=False) # Serialized input query or prompt
    output: Mapped[str] = mapped_column(Text, nullable=False) # Serialized output content
    type: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # e.g. "prompt_gen", "script", "hook", "image_prompt", "chat"
    provider: Mapped[str] = mapped_column(String(50), nullable=True) # e.g. "openai", "gemini", "claude", "ollama"
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="generated_contents")
