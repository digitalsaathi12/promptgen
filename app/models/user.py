import uuid
import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    language_pref: Mapped[str] = mapped_column(String(10), default="en", nullable=False) # en, hi, hinglish
    role: Mapped[str] = mapped_column(String(50), default="user", nullable=False) # user, admin, super_admin
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False
    )

    # Relationships
    subscription: Mapped[Optional["Subscription"]] = relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")
    prompt_histories: Mapped[list["PromptHistory"]] = relationship("PromptHistory", back_populates="user", cascade="all, delete-orphan")
    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    competitor_reports: Mapped[list["CompetitorReport"]] = relationship("CompetitorReport", back_populates="user", cascade="all, delete-orphan")
    location_searches: Mapped[list["LocationSearch"]] = relationship("LocationSearch", back_populates="user", cascade="all, delete-orphan")
