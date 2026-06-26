import asyncio
import pytest
from typing import Generator, AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import Base, get_db
from app.core import security
from app.models.user import User
from app.models.subscription import Subscription
from app.seed import seed_all

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=test_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def seeded_db(db_session: AsyncSession) -> AsyncSession:
    """Pre-populates the database with prompt templates and configurations."""
    await seed_all(db_session)
    return db_session

@pytest.fixture
async def client(seeded_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield seeded_db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(seeded_db: AsyncSession) -> User:
    """Creates a regular test user in database."""
    hashed_pw = security.get_password_hash("password123")
    user = User(
        name="Test User",
        email="testuser@example.com",
        password_hash=hashed_pw,
        language_pref="en",
        role="user"
    )
    seeded_db.add(user)
    await seeded_db.flush()

    sub = Subscription(
        user_id=user.id,
        plan="free",
        status="active"
    )
    seeded_db.add(sub)
    await seeded_db.flush()
    return user

@pytest.fixture
def user_token(test_user: User) -> str:
    return security.create_access_token(test_user.id)

@pytest.fixture
def user_headers(user_token: str) -> dict:
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture
async def test_admin(seeded_db: AsyncSession) -> User:
    hashed_pw = security.get_password_hash("adminpassword")
    admin = User(
        name="Test Admin",
        email="admin@example.com",
        password_hash=hashed_pw,
        language_pref="en",
        role="admin"
    )
    seeded_db.add(admin)
    await seeded_db.flush()
    return admin

@pytest.fixture
def admin_token(test_admin: User) -> str:
    return security.create_access_token(test_admin.id)

@pytest.fixture
def admin_headers(admin_token: str) -> dict:
    return {"Authorization": f"Bearer {admin_token}"}
