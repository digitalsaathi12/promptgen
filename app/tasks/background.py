import asyncio
import logging
from app.core.celery_app import celery_app
from app.services.competitor_service import competitor_service
from app.services.image_providers import image_gen_service

logger = logging.getLogger(__name__)

def run_async(coro):
    """Helper to run async coroutines in a synchronous celery environment."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@celery_app.task(name="app.tasks.background.analyze_competitor_task")
def analyze_competitor_task(website_url: str) -> dict:
    """Asynchronously performs website crawling and SEO ranking analysis."""
    logger.info(f"Starting async competitor analysis for: {website_url}")
    report = run_async(competitor_service.analyze_website(website_url))
    logger.info(f"Finished async competitor analysis for: {website_url}")
    return report

@celery_app.task(name="app.tasks.background.generate_image_task")
def generate_image_task(prompt: str, provider: str) -> str:
    """Asynchronously triggers image creation models and uploads result to bucket."""
    logger.info(f"Starting async image generation task for prompt: '{prompt}' via {provider}")
    img_url = run_async(image_gen_service.generate_image(prompt, provider))
    logger.info(f"Finished async image generation task. URL: {img_url}")
    return img_url
