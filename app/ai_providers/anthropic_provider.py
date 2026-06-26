import httpx
import logging
from app.core.config import settings
from app.ai_providers.base import AIProvider, AIResponse

logger = logging.getLogger(__name__)

class AnthropicProvider(AIProvider):
    async def generate(
        self, 
        prompt: str, 
        *, 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1000, 
        **kwargs
    ) -> AIResponse:
        api_key = settings.ANTHROPIC_API_KEY
        if not api_key:
            raise ValueError("Anthropic API key is missing. Configure ANTHROPIC_API_KEY inside your .env file.")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=payload, timeout=25.0)
            if resp.status_code == 200:
                data = resp.json()
                text = data["content"][0]["text"]
                prompt_tokens = data.get("usage", {}).get("input_tokens", 0)
                completion_tokens = data.get("usage", {}).get("output_tokens", 0)

                return AIResponse(
                    text=text,
                    model=model,
                    provider="anthropic",
                    raw_response=data,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens
                )
            else:
                logger.error(f"Anthropic returned error status {resp.status_code}: {resp.text}")
                raise RuntimeError(f"Anthropic API error: {resp.text}")
