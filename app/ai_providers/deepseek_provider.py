import httpx
import logging
from app.core.config import settings
from app.ai_providers.base import AIProvider, AIResponse

logger = logging.getLogger(__name__)

class DeepSeekProvider(AIProvider):
    async def generate(
        self, 
        prompt: str, 
        *, 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1000, 
        **kwargs
    ) -> AIResponse:
        api_key = settings.DEEPSEEK_API_KEY
        if not api_key:
            raise ValueError("DeepSeek API key is missing. Configure DEEPSEEK_API_KEY inside your .env file.")

        url = "https://api.deepseek.com/v1/chat/completions"
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

                return AIResponse(
                    text=text,
                    model=model,
                    provider="deepseek",
                    raw_response=data,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens
                )
            else:
                logger.error(f"DeepSeek returned error: {resp.text}")
                raise RuntimeError(f"DeepSeek API error: {resp.text}")
