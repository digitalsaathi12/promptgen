import json
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.generated_content import GeneratedContent
from app.models.image import Image
from app.repositories.generic import GeneratedContentRepository, ImageRepository
from app.services.ai_orchestrator import ai_orchestrator
from app.schemas.ai import (
    PromptGeneratorRequest,
    PromptGeneratorResponse,
    ScriptGeneratorRequest,
    ScriptGeneratorResponse,
    ViralHooksRequest,
    ViralHooksResponse,
    ImagePromptRequest,
    ImagePromptResponse,
    ImageGenerationRequest,
    ImageGenerationResponse
)

router = APIRouter()

@router.post("/prompt-generator", response_model=PromptGeneratorResponse)
async def generate_prompt(
    req: PromptGeneratorRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Converts a Hindi or English text description into optimized prompts for ChatGPT, Gemini, and Claude."""
    payload = {"text": req.text}
    result = await ai_orchestrator.route_request("prompt", payload)

    # Save to user history
    history_repo = GeneratedContentRepository(db)
    history_item = GeneratedContent(
        user_id=current_user.id,
        input=req.text,
        output=json.dumps(result),
        type="prompt_gen",
        provider="orchestrator"
    )
    await history_repo.create(history_item)

    return result

@router.post("/script-generator", response_model=ScriptGeneratorResponse)
async def generate_script(
    req: ScriptGeneratorRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generates visual scripts with visual hooks, introductions, script body, and CTA sections."""
    payload = {"topic": req.topic, "platform": req.platform}
    result = await ai_orchestrator.route_request("script", payload)

    # Save to history
    history_repo = GeneratedContentRepository(db)
    history_item = GeneratedContent(
        user_id=current_user.id,
        input=json.dumps(payload),
        output=json.dumps(result),
        type="script",
        provider="openai"
    )
    await history_repo.create(history_item)

    return result

@router.post("/viral-hooks", response_model=ViralHooksResponse)
async def generate_viral_hooks(
    req: ViralHooksRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generates a collection of 10 viral hook ideas categorized by types (Shock, Pain, Story)."""
    payload = {"topic": req.topic}
    hooks = await ai_orchestrator.route_request("viral-hooks", payload)
    if isinstance(hooks, dict) and "hooks" in hooks:
        hooks = hooks["hooks"]
    elif not isinstance(hooks, list):
        # Fallback if route returned simple list or nested list dict
        hooks = list(hooks)

    result = {"hooks": hooks}
    
    # Save to history
    history_repo = GeneratedContentRepository(db)
    history_item = GeneratedContent(
        user_id=current_user.id,
        input=req.topic,
        output=json.dumps(result),
        type="hook",
        provider="openai"
    )
    await history_repo.create(history_item)

    return result

@router.post("/image-prompt", response_model=ImagePromptResponse)
async def generate_image_prompt(
    req: ImagePromptRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Translates generic text concepts into precise prompt keywords for Midjourney, DALL-E, and Stable Diffusion."""
    payload = {"text": req.text}
    result = await ai_orchestrator.route_request("image-prompt", payload)

    # Save to history
    history_repo = GeneratedContentRepository(db)
    history_item = GeneratedContent(
        user_id=current_user.id,
        input=req.text,
        output=json.dumps(result),
        type="image_prompt",
        provider="openai"
    )
    await history_repo.create(history_item)

    return result

@router.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(
    req: ImageGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Triggers image generation via AI providers (Flux, Stability, OpenAI) and returns the public link URL."""
    payload = {"prompt": req.prompt, "provider": req.provider}
    result = await ai_orchestrator.route_request("image", payload)
    img_url = result.get("image_url", "")

    # Save image URL record to database images table
    image_repo = ImageRepository(db)
    image_item = Image(
        user_id=current_user.id,
        prompt=req.prompt,
        image_url=img_url
    )
    await image_repo.create(image_item)

    # Save to user history logs too
    history_repo = GeneratedContentRepository(db)
    history_item = GeneratedContent(
        user_id=current_user.id,
        input=req.prompt,
        output=json.dumps({"image_url": img_url}),
        type="image_gen",
        provider=req.provider
    )
    await history_repo.create(history_item)

    return {"image_url": img_url}
