import httpx
import logging
from app.core.config import settings
from app.ai_providers.base import AIProvider, AIResponse

logger = logging.getLogger(__name__)

class OpenAIProvider(AIProvider):
    async def generate(
        self, 
        prompt: str, 
        *, 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1000, 
        **kwargs
    ) -> AIResponse:
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API key is missing. Configure OPENAI_API_KEY inside your .env file.")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
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
                text = data["choices"][0]["message"]["content"]
                prompt_tokens = data.get("usage", {}).get("prompt_tokens", 0)
                completion_tokens = data.get("usage", {}).get("completion_tokens", 0)
                
                # Approximate cost calculation for GPT-4o-mini
                cost = (prompt_tokens * 0.15 + completion_tokens * 0.60) / 1000000

                return AIResponse(
                    text=text,
                    model=model,
                    provider="openai",
                    raw_response=data,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    cost=cost
                )
            else:
                logger.error(f"OpenAI returned error: {resp.text}")
                raise RuntimeError(f"OpenAI API error: {resp.text}")
