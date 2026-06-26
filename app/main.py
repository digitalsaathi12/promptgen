import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine, async_session
from app.core.exceptions import register_exception_handlers
from app.seed import seed_all
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security import SecurityMiddleware
from app.middleware.logging import RequestLoggingMiddleware

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Startup lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up: Initializing database tables and models...")
    try:
        # Create all tables dynamically (robust fallback)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        # Seed initial prompt configs and templates
        async with async_session() as session:
            await seed_all(session)
        logger.info("Startup complete: database is ready.")
    except Exception as e:
        logger.error(f"Startup database initialization error: {e}")
        
    yield
    logger.info("Shutting down: database connections closing.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The Digital Saathi Prompt OS Backend API",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. Register Centralized Exceptions Handler
register_exception_handlers(app)

# 2. CORS configurations
origins = settings.CORS_ORIGINS
if isinstance(origins, str):
    origins = [origins]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Security Middlewares
app.add_middleware(SecurityMiddleware)

# 4. Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware)

# 5. Logging Middleware
app.add_middleware(RequestLoggingMiddleware)

# 6. Static Upload Directory mounts
static_upload_dir = os.path.join(os.getcwd(), "static")
os.makedirs(os.path.join(static_upload_dir, "uploads"), exist_ok=True)
app.mount("/static", StaticFiles(directory=static_upload_dir), name="static")

# Includeaggregated API router
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to The Digital Saathi Prompt OS API (डिजिटल साथी)",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs"
    }
