from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Generator(Base):
    __tablename__ = "generators"

    id: Mapped[str] = mapped_column(String(50), primary_key=True) # e.g. "instagram_reel"
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    config_json: Mapped[dict] = mapped_column(JSON, nullable=False) # Dynamic form JSON schema
    template_key: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    prompt_templates: Mapped[list["PromptTemplate"]] = relationship("PromptTemplate", back_populates="generator", cascade="all, delete-orphan")
    prompt_histories: Mapped[list["PromptHistory"]] = relationship("PromptHistory", back_populates="generator", cascade="all, delete-orphan")
