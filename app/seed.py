import os
import json
import asyncio
import logging
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core import security
from app.core.database import async_session, Base, engine
from app.models.user import User
from app.models.generator import Generator
from app.models.prompt_template import PromptTemplate
from app.models.ai_model import AIModel
from app.models.subscription import Subscription

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of modules to seed from configs
MODULE_SLUGS = [
    "instagram_reel",
    "script_generator",
    "hook_generator",
    "image_prompt",
    "seo_generator",
    "email_generator"
]

DEFAULT_AI_MODELS = [
    {"name": "llama3", "provider": "ollama", "is_local": True, "is_active": True, "default_for": "text"},
    {"name": "mistral", "provider": "ollama", "is_local": True, "is_active": True, "default_for": None},
    {"name": "gpt-4o-mini", "provider": "openai", "is_local": False, "is_active": True, "default_for": None},
    {"name": "gemini-pro", "provider": "gemini", "is_local": False, "is_active": True, "default_for": None},
    {"name": "claude-3-haiku", "provider": "anthropic", "is_local": False, "is_active": True, "default_for": None}
]

# Standard prompt bodies for Jinja rendering matching modules
TEMPLATE_BODIES = {
    "instagram_reel": (
        "Generate a 30-second script for an Instagram Reel. "
        "Highlight the business value of '{business_name}' in the industry '{industry}'. "
        "Create copy sections for Hook, Intro, Body, CTA, and Caption. "
        "Ensure the language style matches: '{language}' and tone matches: '{tone}'."
    ),
    "script_generator": (
        "Write a detailed video script about topic: '{topic}' for platform: '{platform}'. "
        "Structure sections clearly: Hook, Body Content, and ending with CTA: '{cta}'."
    ),
    "hook_generator": (
        "Generate exactly {count} viral hooks for topic: '{topic}'. "
        "The hooks must utilize style framework: '{hook_style}'. "
        "Output as a numbered list of hooks."
    ),
    "image_prompt": (
        "Translate the subject: '{subject}' into an artistic generative image prompt. "
        "Incorporate style details: '{style}', lighting setups: '{lighting}', "
        "and append the aspect ratio: '--ar {aspect_ratio}'."
    ),
    "seo_generator": (
        "Draft an SEO blog outline for topic: '{topic}' targeting focus keywords: '{keywords}'. "
        "Write the meta title, description, structure h1/h2 headings, and add keywords advice."
    ),
    "email_generator": (
        "Draft a sales cold email sent to '{recipient}' presenting the product offer: '{offer}'. "
        "Keep the email body tone: '{tone}' and locale preference: '{language}'."
    )
}

async def seed_all(db: AsyncSession):
    """Seeds generators, templates, models, and administrative users."""
    logger.info("Initializing seeder...")

    # 1. Seed AI model catalog
    for m_data in DEFAULT_AI_MODELS:
        q = select(AIModel).where(AIModel.name == m_data["name"])
        res = await db.execute(q)
        if not res.scalars().first():
            logger.info(f"Seeding AI model: {m_data['name']}")
            db.add(AIModel(**m_data))

    # 2. Seed Super Admin
    q_admin = select(User).where(User.email == "admin@digitalsaathi.com")
    res_admin = await db.execute(q_admin)
    admin = res_admin.scalars().first()
    if not admin:
        logger.info("Seeding Super Admin user...")
        hashed_pw = security.get_password_hash("admin123")
        admin = User(
            name="Super Admin",
            email="admin@digitalsaathi.com",
            password_hash=hashed_pw,
            language_pref="en",
            role="super_admin"
        )
        db.add(admin)
        await db.flush()

        # Enterprise subscription
        sub = Subscription(
            user_id=admin.id,
            plan="enterprise",
            status="active"
        )
        db.add(sub)
    else:
        logger.info("Super Admin user exists. Skipping user seed.")

    # 3. Seed Generator Form JSONs and Template objects
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for slug in MODULE_SLUGS:
        config_path = os.path.join(app_root, "app", "modules", slug, "config.json")
        if not os.path.exists(config_path):
            logger.warning(f"Config JSON not found at: {config_path}. Skipping.")
            continue
            
        with open(config_path, "r") as f:
            config_data = json.load(f)

        # Check if generator exists
        q_gen = select(Generator).where(Generator.id == slug)
        res_gen = await db.execute(q_gen)
        db_gen = res_gen.scalars().first()

        if not db_gen:
            logger.info(f"Seeding generator: {slug}")
            db_gen = Generator(
                id=slug,
                label=config_data.get("label", slug.capitalize()),
                config_json=config_data,
                template_key=config_data.get("template_key", f"{slug}_v1"),
                is_active=True
            )
            db.add(db_gen)

        # Check if template exists
        q_temp = select(PromptTemplate).where(PromptTemplate.generator_id == slug)
        res_temp = await db.execute(q_temp)
        db_temp = res_temp.scalars().first()

        if not db_temp:
            logger.info(f"Seeding prompt template for generator: {slug}")
            body_template = TEMPLATE_BODIES.get(slug, "Generate content using variables")
            db_temp = PromptTemplate(
                generator_id=slug,
                name=f"Standard {slug.capitalize()} Template",
                role_text=f"Expert {config_data.get('label', slug)} AI Writer",
                objective_text=f"Produce optimized outputs for {slug} marketing campaigns",
                constraints="Output raw text sections only. Follow the locale rules carefully.",
                body_template=body_template,
                version=1
            )
            db.add(db_temp)

    await db.commit()
    logger.info("Seeding completed successfully.")

async def main():
    # Setup tables if they do not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as session:
        await seed_all(session)

if __name__ == "__main__":
    asyncio.run(main())
