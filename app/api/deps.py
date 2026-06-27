from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import ALGORITHM
from app.models.user import User

from sqlalchemy import select

# Pointer to auth login for swagger docs (Commented out for internal access bypass)
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/auth/login"
# )

async def get_current_user(
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Bypassed authentication for internal deployment.
    Queries or auto-creates a default internal super admin user.
    """
    email = "internal-member@digitalsaathi.local"
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if user is None:
        user = User(
            name="Internal Member",
            email=email,
            password_hash="disabled",
            language_pref="en",
            role="super_admin"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Requires admin privileges."
        )
    return current_user

def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Requires super admin privileges."
        )
    return current_user
