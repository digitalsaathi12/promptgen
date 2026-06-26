import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_user
from app.core import security
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.auth import Token, UserRegister, UserLogin, TokenRefreshRequest
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    """Registers a new user and configures a default subscription plan."""
    # Check if email is registered
    query = select(User).where(User.email == user_in.email)
    res = await db.execute(query)
    if res.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # Create new user record
    hashed_pw = security.get_password_hash(user_in.password)
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hashed_pw,
        language_pref=user_in.language_pref or "en",
        role="user"
    )
    db.add(user)
    await db.flush() # Populate ID

    # Seed Free tier subscription
    sub = Subscription(
        user_id=user.id,
        plan="free",
        status="active",
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=365)
    )
    db.add(sub)
    await db.commit()

    return user

@router.post("/login", response_model=Token)
async def login(login_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """Verifies credentials and returns access + refresh JWTs."""
    query = select(User).where(User.email == login_in.email)
    res = await db.execute(query)
    user = res.scalars().first()

    if not user or not security.verify_password(login_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password."
        )

    return Token(
        access_token=security.create_access_token(user.id),
        refresh_token=security.create_refresh_token(user.id)
    )

@router.post("/refresh", response_model=Token)
async def refresh(refresh_in: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    """Refreshes tokens using a valid refresh token claim."""
    try:
        payload = security.decode_token(refresh_in.refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token type.")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return Token(
        access_token=security.create_access_token(user.id),
        refresh_token=security.create_refresh_token(user.id)
    )

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """Retrieves the active user profile."""
    return current_user

@router.put("/me", response_model=UserOut)
async def update_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Updates language preference or display details."""
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password_hash"] = security.get_password_hash(update_data["password"])
        del update_data["password"]

    for key, val in update_data.items():
        setattr(current_user, key, val)

    db.add(current_user)
    await db.commit()
    return current_user
