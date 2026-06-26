import logging
from jinja2 import Template
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.prompt_template import PromptTemplate

logger = logging.getLogger(__name__)

# Standard structural Jinja2 prompt skeleton
DEFAULT_SKELETON = """Role: {{ role_text }}
Objective: {{ objective_text }}
Business Context: {{ business }}
Target Industry: {{ industry }}
Platform: {{ platform }}
Target Audience: {{ audience }}
Language/Locale: {{ language }}
Tone: {{ tone }}
Constraints:
{{ constraints }}

Specific Instructions:
{{ body_template }}

Expected Output Sections: {{ expected_output | join(", ") }}
"""

class PromptTemplateRenderer:
    def render_prompt(self, template_data: Dict[str, Any], variables: Dict[str, Any]) -> str:
        """Renders the final constructed prompt using a Jinja2 template skeleton."""
        # Clean constraints: can be list or string
        constraints_raw = template_data.get("constraints", "")
        if isinstance(constraints_raw, list):
            constraints_str = "\n".join(f"- {c}" for c in constraints_raw)
        else:
            constraints_str = constraints_raw

        # Output format sections
        output_sections = template_data.get("output_sections", ["response"])

        render_vars = {
            "role_text": template_data.get("role_text", "Expert AI assistant"),
            "objective_text": template_data.get("objective_text", "Generate high-quality business copy"),
            "business": variables.get("business", "Generic local company"),
            "industry": variables.get("industry", "SaaS"),
            "platform": variables.get("platform", "web"),
            "audience": variables.get("audience", "general public"),
            "language": variables.get("language", "English"),
            "tone": variables.get("tone", "Professional"),
            "constraints": constraints_str,
            "body_template": template_data.get("body_template", ""),
            "expected_output": output_sections
        }

        # Render custom template or default skeleton
        jinja_template = Template(DEFAULT_SKELETON)
        rendered_prompt = jinja_template.render(**render_vars)

        # Apply specific instructions prompt body interpolation too if any variables exist in it
        if "{{" in render_vars["body_template"]:
            body_template = Template(render_vars["body_template"])
            rendered_body = body_template.render(**variables)
            # Re-render with interpolated body
            render_vars["body_template"] = rendered_body
            rendered_prompt = jinja_template.render(**render_vars)

        return rendered_prompt

    async def get_template_by_generator(self, db: AsyncSession, generator_id: str) -> Optional[Dict[str, Any]]:
        """Queries the prompt_templates DB table for the active generator prompt schema."""
        try:
            query = select(PromptTemplate).where(PromptTemplate.generator_id == generator_id).order_by(PromptTemplate.version.desc())
            res = await db.execute(query)
            db_template = res.scalars().first()
            if db_template:
                return {
                    "role_text": db_template.role_text,
                    "objective_text": db_template.objective_text,
                    "constraints": db_template.constraints,
                    "body_template": db_template.body_template,
                    "version": db_template.version
                }
        except Exception as e:
            logger.error(f"Error fetching DB template: {e}")
        return None

template_renderer = PromptTemplateRenderer()
