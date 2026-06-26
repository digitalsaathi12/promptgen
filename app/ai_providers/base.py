from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class AIResponse(BaseModel):
    text: str
    model: str
    provider: str
    raw_response: Optional[Dict[str, Any]] = None
    prompt_tokens: Optional[int] = 0
    completion_tokens: Optional[int] = 0
    cost: Optional[float] = 0.0

class AIProvider(ABC):
    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        *, 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1000, 
        **kwargs
    ) -> AIResponse:
        """Sends a text prompt to the LLM model and returns structured AIResponse."""
        pass
