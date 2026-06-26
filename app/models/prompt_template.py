import uuid
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    generator_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("generators.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role_text: Mapped[str] = mapped_column(Text, nullable=False)
    objective_text: Mapped[str] = mapped_column(Text, nullable=False)
    constraints: Mapped[str] = mapped_column(Text, default="", nullable=False) # raw constraints or newline split
    body_template: Mapped[str] = mapped_column(Text, nullable=False) # Jinja2 prompt layout
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    generator: Mapped[Optional["Generator"]] = relationship("Generator", back_populates="prompt_templates")
