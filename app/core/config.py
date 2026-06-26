import os
from typing import List, Optional, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "The Digital Saathi"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # JWT Security
    JWT_SECRET: str = Field(default="saathi-super-secret-key-for-local-development-only-xyz")
    SECRET_KEY: str = Field(default="saathi-super-secret-key-for-local-development-only-xyz")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # DB Config
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/digitalsaathi")
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # Celery
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0")
    CELERY_TASK_ALWAYS_EAGER: bool = True

    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = "mock-google-client-id"

    # AI API Config
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    GROK_API_KEY: Optional[str] = None

    # Location APIs
    NOMINATIM_BASE_URL: str = Field(default="https://nominatim.openstreetmap.org")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # CORS Configuration
    CORS_ORIGINS: Union[str, List[str]] = Field(default="*")

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str) -> str:
        if not v:
            return "sqlite+aiosqlite:///./digitalsaathi.db"
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

settings = Settings()
# Guarantee JWT_SECRET matches SECRET_KEY for backward compatibility
if not settings.JWT_SECRET or settings.JWT_SECRET == "saathi-super-secret-key-for-local-development-only-xyz":
    if settings.SECRET_KEY != "saathi-super-secret-key-for-local-development-only-xyz":
        settings.JWT_SECRET = settings.SECRET_KEY
