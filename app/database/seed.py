import asyncio
import logging
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core import security
from app.core.database import async_session, Base, engine
from app.models.user import User
from app.models.subscription import Subscription
from app.models.prompt import Prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_PROMPTS = [
    {
        "title": "Hindi Social Media Copywriting",
        "category": "Marketing",
        "subcategory": "Social Media",
        "description": "Writes high converting ad copy in mixed Hindi-English (Hinglish) targeting Indian youth.",
        "prompt_text": "You are a creative copywriter. Write a social media post copy for a brand selling {product}. The tone should be casual, Hinglish, and very relatable. Highlight the key benefit: {benefit}. Use high converting hooks and hashtags.",
        "tags": "hinglish,ads,copywriting"
    },
    {
        "title": "SEO Blog Post Structure Creator",
        "category": "SEO",
        "subcategory": "Blogging",
        "description": "Generates complete blog outlines with target keyword clusters and header tags.",
        "prompt_text": "Write a detailed blog outline for the topic '{topic}'. Organize headers using H1, H2, and H3 tags. Include target keywords: {keywords} naturally. Provide a brief content summary for each section.",
        "tags": "seo,blog,outline"
    },
    {
        "title": "Indore Local Business Optimizer",
        "category": "Marketing",
        "subcategory": "Local Business",
        "description": "Helps local businesses in Indore rank on Google Maps and optimize local pages.",
        "prompt_text": "You are a local SEO consultant in Indore. Provide a step-by-step checklist to optimize the Google Business Profile for a '{business_type}' business. Recommend local keywords for Indore and near-me queries.",
        "tags": "indore,local-seo,gmb"
    },
    {
        "title": "YouTube Video Hook Script Maker",
        "category": "Content Writing",
        "subcategory": "Scripts",
        "description": "Generates 5 intense curiosity hooks for a YouTube video outline.",
        "prompt_text": "Create 5 video hooks for a YouTube video about '{topic}'. Use Curiosity, Pain points, Shock, or Story telling techniques. Keep each hook under 10 seconds of spoken dialogue.",
        "tags": "youtube,hooks,scripts"
    }
]

async def seed_data(db: AsyncSession):
    """Seeds the database with default prompts and a Super Admin user."""
    # 1. Seed Super Admin
    user_query = select(User).where(User.email == "admin@digitalsaathi.com")
    res = await db.execute(user_query)
    admin_user = res.scalars().first()

    if not admin_user:
        logger.info("Creating default Super Admin user: admin@digitalsaathi.com")
        hashed_password = security.get_password_hash("admin123")
        admin_user = User(
            name="Super Admin",
            email="admin@digitalsaathi.com",
            phone="+919999999999",
            password=hashed_password,
            role="super_admin",
            is_verified=True
        )
        db.add(admin_user)
        await db.flush()

        # Seed admin subscription
        sub = Subscription(
            user_id=admin_user.id,
            plan="enterprise",
            status="active",
            expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=3650) # 10 years
        )
        db.add(sub)
    else:
        logger.info("Super Admin user already exists. Skipping user seed.")

    # 2. Seed Prompts
    for p_data in DEFAULT_PROMPTS:
        prompt_query = select(Prompt).where(Prompt.title == p_data["title"])
        res_p = await db.execute(prompt_query)
        existing_prompt = res_p.scalars().first()

        if not existing_prompt:
            logger.info(f"Seeding default prompt: {p_data['title']}")
            prompt = Prompt(**p_data)
            db.add(prompt)
        else:
            logger.info(f"Prompt '{p_data['title']}' already exists. Skipping prompt seed.")

    await db.commit()
    logger.info("Database seeding completed successfully.")

async def main():
    async with engine.begin() as conn:
        # Create all tables dynamically if they do not exist
        # Useful for quick sqlite/development setup without alembic
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as session:
        await seed_data(session)

if __name__ == "__main__":
    asyncio.run(main())
