import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.optimization_layer import optimization_layer
from app.engine.templates import template_renderer

logger = logging.getLogger(__name__)

# Universal parameter default values
UNIVERSAL_DEFAULTS = {
    "business": "Generic Local Business",
    "industry": "Marketing and SaaS",
    "purpose": "Promote brand services",
    "audience": "general audience",
    "language": "English",
    "tone": "Professional",
    "platform": "generic",
    "output_format": "text",
    "creativity": "medium",
    "length": "medium",
    "experience_level": "intermediate",
    "ai_model": "auto"
}

class PromptConstructionEngine:
    def validate_fields(self, config: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validates payload fields against generator dynamic configurations schemas."""
        fields = config.get("fields", [])
        validated = {}

        for field in fields:
            name = field.get("name")
            required = field.get("required", False)
            field_type = field.get("type", "string")
            default_val = field.get("default")

            val = payload.get(name)

            # Check required
            if val is None or val == "":
                if required:
                    raise ValueError(f"Field '{name}' is required by '{config.get('label')}' form.")
                # Merge default
                val = default_val

            # Type checking and casting
            if val is not None:
                if field_type == "integer":
                    try:
                        val = int(val)
                    except ValueError:
                        raise ValueError(f"Field '{name}' must be an integer, got: {val}")
                elif field_type == "enum":
                    options = field.get("options", [])
                    if val not in options:
                        raise ValueError(f"Field '{name}' must be one of {options}. Got: {val}")

            validated[name] = val

        # Copy over universal params if provided in payload but not in form fields
        for param in UNIVERSAL_DEFAULTS:
            if param not in validated and param in payload:
                validated[param] = payload[param]

        return validated

    def merge_defaults(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Merges missing universal parameters to payload context."""
        context = UNIVERSAL_DEFAULTS.copy()
        context.update(payload)
        return context

    async def build(
        self, 
        db: Optional[AsyncSession], 
        generator_config: Dict[str, Any], 
        raw_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Processes the input payload through the construction pipeline.
        
        Returns:
            dict: {
                "constructed_prompt": str,
                "variables": dict,
                "ai_model": str
            }
        """
        generator_id = generator_config.get("id")

        # 1. Validate fields
        validated_payload = self.validate_fields(generator_config, raw_payload)

        # 2. Merge Universal Defaults
        context = self.merge_defaults(validated_payload)

        # 3. Apply normalizations and language optimizations
        optimized_context = optimization_layer.apply_optimizations(context)

        # 4. Fetch prompt templates from DB if session exists, else create default template dict
        template_data = None
        if db:
            template_data = await template_renderer.get_template_by_generator(db, generator_id)

        if not template_data:
            logger.info(f"Using default fallback prompt template mapping for '{generator_id}'")
            # Build simulated prompt template fields based on config
            template_data = {
                "role_text": f"Expert {generator_config.get('label', 'AI Assistant')}",
                "objective_text": f"Generate content matching the parameters below",
                "constraints": optimized_context.get("hidden_instructions", []),
                "body_template": (
                    f"Create content of type '{generator_id}' using topic context: "
                    f"'{optimized_context.get('purpose', 'the request')}'."
                ),
                "output_sections": generator_config.get("output_sections", ["response"])
            }

        # Render prompt text
        constructed_prompt = template_renderer.render_prompt(template_data, optimized_context)

        return {
            "constructed_prompt": constructed_prompt,
            "variables": optimized_context,
            "ai_model": optimized_context.get("ai_model", "auto")
        }

prompt_construction_engine = PromptConstructionEngine()
