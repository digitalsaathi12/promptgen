import asyncio
import logging
from typing import Dict, Any, List, Union
from app.ai_providers.base import AIProvider, AIResponse
from app.ai_providers.ollama_provider import OllamaProvider
from app.ai_providers.openai_provider import OpenAIProvider
from app.ai_providers.gemini_provider import GeminiProvider
from app.ai_providers.anthropic_provider import AnthropicProvider
from app.ai_providers.deepseek_provider import DeepSeekProvider
from app.ai_providers.grok_provider import GrokProvider
from app.core.config import settings

logger = logging.getLogger(__name__)

# Instantiate providers
providers: Dict[str, AIProvider] = {
    "ollama": OllamaProvider(),
    "openai": OpenAIProvider(),
    "gemini": GeminiProvider(),
    "anthropic": AnthropicProvider(),
    "deepseek": DeepSeekProvider(),
    "grok": GrokProvider()
}

def resolve_provider(model_name: str) -> str:
    """Detects provider type based on the requested model name."""
    m = model_name.lower()
    if m.startswith("gpt-") or m.startswith("text-davinci") or m.startswith("dall-"):
        return "openai"
    elif m.startswith("gemini-"):
        return "gemini"
    elif m.startswith("claude-"):
        return "anthropic"
    elif m.startswith("deepseek-"):
        return "deepseek"
    elif m.startswith("grok-"):
        return "grok"
    else:
        return "ollama"

async def route(
    prompt: str, 
    model_name: str = "auto", 
    temperature: float = 0.7, 
    max_tokens: int = 1000, 
    **kwargs
) -> AIResponse:
    """Routes the prompt generation to the appropriate provider."""
    # Resolve auto to local Ollama default model
    if model_name == "auto":
        model_name = "llama3"

    provider_name = resolve_provider(model_name)
    provider = providers.get(provider_name, providers["ollama"])

    # Fallback checks: if paid provider is selected but API key is missing, redirect to Ollama
    fallback_needed = False
    if provider_name == "openai" and not settings.OPENAI_API_KEY:
        fallback_needed = True
    elif provider_name == "gemini" and not settings.GEMINI_API_KEY:
        fallback_needed = True
    elif provider_name == "anthropic" and not settings.ANTHROPIC_API_KEY:
        fallback_needed = True
    elif provider_name == "deepseek" and not settings.DEEPSEEK_API_KEY:
        fallback_needed = True
    elif provider_name == "grok" and not settings.GROK_API_KEY:
        fallback_needed = True

    if fallback_needed:
        logger.warning(
            f"API key missing for provider '{provider_name}'. "
            f"Falling back from '{model_name}' to local Ollama Llama3."
        )
        provider = providers["ollama"]
        model_name = "llama3"

    logger.info(f"Routing request to provider: {provider.__class__.__name__} (Model: {model_name})")
    return await provider.generate(
        prompt, 
        model=model_name, 
        temperature=temperature, 
        max_tokens=max_tokens, 
        **kwargs
    )

async def route_multiple(
    prompt: str, 
    model_names: List[str], 
    temperature: float = 0.7, 
    max_tokens: int = 1000, 
    **kwargs
) -> Dict[str, Union[AIResponse, str]]:
    """Executes fan-out prompting across 2+ models in parallel, returning dictionary mapped by model."""
    tasks = [
        route(prompt, model_name=m, temperature=temperature, max_tokens=max_tokens, **kwargs)
        for m in model_names
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    output_comparison = {}
    for idx, model in enumerate(model_names):
        res = results[idx]
        if isinstance(res, Exception):
            logger.error(f"Model comparison error for '{model}': {res}")
            # Format exception as response string
            output_comparison[model] = AIResponse(
                text=f"Failed to generate using {model}: {str(res)}",
                model=model,
                provider=resolve_provider(model)
            )
        else:
            output_comparison[model] = res
            
    return output_comparison
