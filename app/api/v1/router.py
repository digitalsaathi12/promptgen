from fastapi import APIRouter
from app.api.v1 import (
    # auth,
    generators,
    prompts,
    history,
    favorites,
    ai_chat,
    competitor_analysis,
    location_intelligence,
    models_router
)

api_router = APIRouter()

# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(generators.router, prefix="/generators", tags=["Dynamic Form Generators"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["Prompt Templates"])
api_router.include_router(history.router, prefix="/history", tags=["Prompt History"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
api_router.include_router(ai_chat.router, prefix="/ai-chat", tags=["AI Chat"])
api_router.include_router(competitor_analysis.router, prefix="/competitor-analysis", tags=["Competitor Analysis"])
api_router.include_router(location_intelligence.router, prefix="/location-intelligence", tags=["Location Intelligence"])
api_router.include_router(models_router.router, prefix="/models", tags=["AI Model Catalog"])
