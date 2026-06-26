import httpx
import logging
from app.core.config import settings
from app.ai_providers.base import AIProvider, AIResponse

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    async def generate(
        self, 
        prompt: str, 
        *, 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1000, 
        **kwargs
    ) -> AIResponse:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("Gemini API key is missing. Configure GEMINI_API_KEY inside your .env file.")

        # Default model if simple name provided
        actual_model = model if "/" in model else f"models/{model}"
        url = f"https://generativelanguage.googleapis.com/v1beta/{actual_model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, timeout=25.0)
            if resp.status_code == 200:
                data = resp.json()
                try:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    raise RuntimeError(f"Unexpected response format from Gemini: {data}")
                
                return AIResponse(
                    text=text,
                    model=model,
                    provider="gemini",
                    raw_response=data
                )
            else:
                logger.error(f"Gemini returned error status {resp.status_code}: {resp.text}")
                raise RuntimeError(f"Gemini API error: {resp.text}")
