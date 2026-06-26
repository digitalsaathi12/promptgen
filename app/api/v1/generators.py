import json
import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.generator import Generator
from app.models.prompt_history import PromptHistory
from app.engine.prompt_builder import prompt_construction_engine
from app.ai_providers import router as ai_router
from app.schemas.generator import GeneratorOut, GeneratorGenerateRequest, GeneratorGenerateResponse

logger = logging.getLogger(__name__)

router = APIRouter()

def parse_output_sections(text: str, expected_sections: List[str]) -> Dict[str, Any]:
    """Tries parsing LLM output text into structured segments mapped to expected keys."""
    text_clean = text.strip()
    
    # 1. Check if LLM returned standard JSON block
    if text_clean.startswith("{") or "```json" in text_clean:
        try:
            # Strip markdown block wrappers if present
            cleaned = text_clean
            if "```" in cleaned:
                lines = cleaned.splitlines()
                # Find start and end indexes
                start = -1
                end = -1
                for idx, line in enumerate(lines):
                    if line.startswith("```json") or (line.startswith("```") and start == -1):
                        start = idx
                    elif line.startswith("```") and start != -1:
                        end = idx
                        break
                if start != -1 and end != -1:
                    cleaned = "\n".join(lines[start+1:end])
            
            parsed = json.loads(cleaned)
            # Ensure all expected sections exist
            output = {}
            for sec in expected_sections:
                output[sec] = parsed.get(sec, parsed.get(sec.lower(), parsed.get(sec.capitalize(), "")))
            
            # If we successfully parsed most sections, return it
            if any(output.values()):
                return output
        except Exception as e:
            logger.warning(f"Failed to parse output text as direct JSON: {e}")

    # 2. Fallback: Parse via structural regex headers, e.g. "Hook:", "[Body]"
    output = {}
    remaining_text = text
    for idx, sec in enumerate(expected_sections):
        # Look for headers like "SecName:" or "SecName"
        pattern = rf"(?i)(?:^|\n)(?:\[?{sec}\]?\s*:?)\s*\n?"
        import re
        splits = re.split(pattern, remaining_text, maxsplit=1)
        if len(splits) == 2:
            if idx > 0:
                # Save previous section content
                prev_sec = expected_sections[idx-1]
                output[prev_sec] = splits[0].strip()
            remaining_text = splits[1]
        else:
            # Try plain text splits or placeholder
            output[sec] = ""

    # Assign remaining text to the last section
    if expected_sections:
        last_sec = expected_sections[-1]
        output[last_sec] = remaining_text.strip()

    # Verify if all sections are empty (header parsing failed completely)
    if not any(output.values()):
        # Split text into equal parts or dump full text to the first section
        output = {sec: "" for sec in expected_sections}
        if expected_sections:
            output[expected_sections[0]] = text

    return output

@router.get("/", response_model=List[GeneratorOut])
async def list_generators(db: AsyncSession = Depends(get_db)):
    """Retrieves all active dynamic form generator configurations."""
    query = select(Generator).where(Generator.is_active == True)
    res = await db.execute(query)
    return list(res.scalars().all())

@router.get("/{generator_id}", response_model=GeneratorOut)
async def get_generator(generator_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieves a single dynamic form generator configuration schema."""
    db_gen = await db.get(Generator, generator_id)
    if not db_gen:
        raise HTTPException(
            status_code=404,
            detail=f"Generator form template '{generator_id}' not found."
        )
    return db_gen

@router.post("/{generator_id}/generate", response_model=GeneratorGenerateResponse)
async def generate_content(
    generator_id: str,
    req: GeneratorGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validates raw input fields, builds prompt, routes execution, parses sections, and logs history."""
    # 1. Fetch form config
    db_gen = await db.get(Generator, generator_id)
    if not db_gen:
        raise HTTPException(status_code=404, detail="Generator form template not found.")

    # 2. Build prompt context using Prompt Construction Engine
    try:
        build_result = await prompt_construction_engine.build(
            db=db,
            generator_config=db_gen.config_json,
            raw_payload=req.payload
        )
    except ValueError as val_err:
        raise HTTPException(status_code=422, detail=str(val_err))
    
    constructed_prompt = build_result["constructed_prompt"]
    variables = build_result["variables"]
    target_model = req.model_name if req.model_name != "auto" else build_result["ai_model"]

    # 3. Route prompt to AI Provider router
    try:
        ai_resp = await ai_router.route(
            prompt=constructed_prompt,
            model_name=target_model,
            temperature=req.temperature
        )
    except Exception as e:
        logger.error(f"Router execution failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to generate content: {str(e)}"
        )

    # 4. Parse response text into expected output sections
    expected_sections = db_gen.config_json.get("output_sections", ["response"])
    parsed_output = parse_output_sections(ai_resp.text, expected_sections)

    # 5. Persist to PromptHistory logs
    history_item = PromptHistory(
        user_id=current_user.id,
        generator_id=db_gen.id,
        input_payload=req.payload,
        constructed_prompt=constructed_prompt,
        ai_model_used=ai_resp.model,
        output=parsed_output
    )
    db.add(history_item)
    await db.flush() # Flush to populate UUID ID

    return GeneratorGenerateResponse(
        constructed_prompt=constructed_prompt,
        ai_model=ai_resp.model,
        output=parsed_output
    )
