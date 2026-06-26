from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_phone(self, phone: str) -> Optional[User]:
        query = select(User).where(User.phone == phone)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_email_or_phone(self, email: Optional[str], phone: Optional[str]) -> Optional[User]:
        if not email and not phone:
            return None
        conditions = []
        if email:
            conditions.append(User.email == email)
        if phone:
            conditions.append(User.phone == phone)
            
        from sqlalchemy import or_
        query = select(User).where(or_(*conditions))
        result = await self.db.execute(query)
        return result.scalars().first()
