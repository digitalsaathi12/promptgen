import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

logger = logging.getLogger(__name__)

# Base declarative class for all models
class Base(DeclarativeBase):
    pass

# Choose database engine URL based on connection status or configuration
db_url = settings.DATABASE_URL
if "postgresql" in db_url and settings.ENVIRONMENT == "development":
    # Let's verify we have a fallback or try-catch for local execution
    logger.info("Configuring PostgreSQL async engine.")
else:
    logger.info("Configuring SQLite database fallback.")

# Create the async engine
try:
    engine = create_async_engine(
        db_url,
        future=True,
        echo=False,
        # Pool size and max overflow are not supported by SQLite
        **(
            {"pool_size": 20, "max_overflow": 10}
            if "postgresql" in db_url
            else {}
        )
    )
except Exception as e:
    logger.error(f"Failed to create async engine for {db_url}: {e}. Falling back to SQLite.")
    db_url = "sqlite+aiosqlite:///./digitalsaathi.db"
    engine = create_async_engine(db_url, future=True, echo=False)

# Sessionmaker for async sessions
async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection helper to yield database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
