import logging
from typing import Dict, Any, List
from app.services.ai_providers import ai_service
from app.services.image_providers import image_gen_service
from app.services.maps_service import maps_service
from app.services.competitor_service import competitor_service

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self):
        self.ai = ai_service
        self.image = image_gen_service
        self.maps = maps_service
        self.competitor = competitor_service

    async def route_request(self, engine_type: str, payload: Dict[str, Any]) -> Any:
        """Central AI Router that directs requests to specific underlying engines.
        
        Args:
            engine_type (str): one of "prompt", "script", "image", "location", "competitor", "chat".
            payload (dict): request parameters required by the targeted engine.
        """
        engine_type = engine_type.lower()
        logger.info(f"Routing request to Engine: {engine_type.upper()}")

        if engine_type in ["prompt", "prompt-generator"]:
            # Prompt Engine
            text_input = payload.get("text", "")
            return await self.ai.generate_prompt(text_input)

        elif engine_type in ["script", "script-generator"]:
            # Script Engine
            topic = payload.get("topic", "")
            platform = payload.get("platform", "reels")
            return await self.ai.generate_script(topic, platform)

        elif engine_type in ["viral-hooks", "hooks"]:
            # Script Engine (Viral Hook Generator)
            topic = payload.get("topic", "")
            return await self.ai.generate_viral_hooks(topic)

        elif engine_type in ["image-prompt", "image_prompt"]:
            # Image Engine (Image Prompt Generator)
            text_input = payload.get("text", "")
            return await self.ai.generate_image_prompts(text_input)

        elif engine_type in ["image", "generate-image"]:
            # Image Engine (Image Generator)
            prompt = payload.get("prompt", "")
            provider = payload.get("provider", "flux")
            image_url = await self.image.generate_image(prompt, provider)
            return {"image_url": image_url}

        elif engine_type == "location":
            # Location Engine
            query = payload.get("query", "")
            return await self.maps.search_location(query)

        elif engine_type == "competitor":
            # Analysis Engine
            website = payload.get("website", "")
            return await self.competitor.analyze_website(website)

        elif engine_type == "chat":
            # Chat Engine
            message = payload.get("message", "")
            provider = payload.get("provider", "gpt")
            history = payload.get("history", [])
            response_text = await self.ai.chat_message(message, provider, history)
            return {"response": response_text}

        else:
            raise ValueError(f"Unknown engine type routing request: {engine_type}")

ai_orchestrator = AIOrchestrator()
