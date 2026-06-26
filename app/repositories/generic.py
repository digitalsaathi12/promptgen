from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from app.repositories.base import BaseRepository
from app.models.subscription import Subscription
from app.models.prompt import Prompt
from app.models.generated_content import GeneratedContent
from app.models.saved_result import SavedResult
from app.models.location_search import LocationSearch
from app.models.competitor_report import CompetitorReport
from app.models.image import Image

class SubscriptionRepository(BaseRepository[Subscription]):
    def __init__(self, db: AsyncSession):
        super().__init__(Subscription, db)

    async def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
        query = select(Subscription).where(Subscription.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()


class PromptRepository(BaseRepository[Prompt]):
    def __init__(self, db: AsyncSession):
        super().__init__(Prompt, db)

    async def search(self, q: str, category: Optional[str] = None, subcategory: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Prompt]:
        query = select(Prompt)
        conditions = []
        if q:
            conditions.append(or_(
                Prompt.title.ilike(f"%{q}%"),
                Prompt.description.ilike(f"%{q}%"),
                Prompt.prompt_text.ilike(f"%{q}%"),
                Prompt.tags.ilike(f"%{q}%")
            ))
        if category:
            conditions.append(Prompt.category == category)
        if subcategory:
            conditions.append(Prompt.subcategory == subcategory)

        if conditions:
            query = query.where(*conditions)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_categories(self) -> List[str]:
        query = select(Prompt.category).distinct()
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_subcategories(self, category: str) -> List[str]:
        query = select(Prompt.subcategory).where(Prompt.category == category).distinct()
        result = await self.db.execute(query)
        return list(result.scalars().all())


class GeneratedContentRepository(BaseRepository[GeneratedContent]):
    def __init__(self, db: AsyncSession):
        super().__init__(GeneratedContent, db)

    async def get_user_history(self, user_id: int, content_type: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[GeneratedContent]:
        query = select(GeneratedContent).where(GeneratedContent.user_id == user_id)
        if content_type:
            query = query.where(GeneratedContent.type == content_type)
        query = query.order_by(GeneratedContent.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def clear_user_history(self, user_id: int) -> None:
        from sqlalchemy import delete
        query = delete(GeneratedContent).where(GeneratedContent.user_id == user_id)
        await self.db.execute(query)


class SavedResultRepository(BaseRepository[SavedResult]):
    def __init__(self, db: AsyncSession):
        super().__init__(SavedResult, db)

    async def get_user_saved(self, user_id: int, result_type: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[SavedResult]:
        query = select(SavedResult).where(SavedResult.user_id == user_id)
        if result_type:
            query = query.where(SavedResult.type == result_type)
        query = query.order_by(SavedResult.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class LocationSearchRepository(BaseRepository[LocationSearch]):
    def __init__(self, db: AsyncSession):
        super().__init__(LocationSearch, db)

    async def get_user_history(self, user_id: int, limit: int = 100) -> List[LocationSearch]:
        query = select(LocationSearch).where(LocationSearch.user_id == user_id).order_by(LocationSearch.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class CompetitorReportRepository(BaseRepository[CompetitorReport]):
    def __init__(self, db: AsyncSession):
        super().__init__(CompetitorReport, db)

    async def get_user_reports(self, user_id: int, limit: int = 100) -> List[CompetitorReport]:
        query = select(CompetitorReport).where(CompetitorReport.user_id == user_id).order_by(CompetitorReport.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class ImageRepository(BaseRepository[Image]):
    def __init__(self, db: AsyncSession):
        super().__init__(Image, db)

    async def get_user_images(self, user_id: int, limit: int = 100) -> List[Image]:
        query = select(Image).where(Image.user_id == user_id).order_by(Image.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
