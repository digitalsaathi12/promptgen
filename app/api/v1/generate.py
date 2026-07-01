"""
Stateless AI Generator endpoints — no auth, no DB, no session.
Each endpoint takes structured input → builds an optimised prompt
→ calls Gemini → returns parsed JSON output.

Flow:
  Frontend POST → /api/v1/generate/<module> → GeminiProvider → JSON output → Frontend
"""

import json
import re
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional, List

from app.ai_providers.gemini_provider import GeminiProvider
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# ---------------------------------------------------------------------------
# Shared Gemini helper
# ---------------------------------------------------------------------------

gemini = GeminiProvider()

FLASH_LITE = "gemini-2.5-flash"   # fast / short content
FLASH      = "gemini-2.5-flash"                       # longer content

def _strip_fences(text: str) -> str:
    """Remove ```json ... ``` or ``` ... ``` wrappers Gemini sometimes adds."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text, flags=re.IGNORECASE)
    return text.strip()

async def _call_gemini(prompt: str, model: str, temperature: float = 0.8, max_tokens: int = 2000, **kwargs) -> str:
    """Call GeminiProvider and return raw text. Raises HTTPException on failure."""
    try:
        resp = await gemini.generate(
            prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        total_tokens = (resp.prompt_tokens or 0) + (resp.completion_tokens or 0)
        logger.info(f"[generate] model={model} prompt_tokens={resp.prompt_tokens} completion_tokens={resp.completion_tokens} total={total_tokens}")
        return resp.text
    except Exception as exc:
        logger.error(f"[generate] Gemini call failed: {exc}")
        raise HTTPException(status_code=502, detail={"message": "AI generation failed. Please retry.", "code": "GEMINI_ERROR"})

def _parse_json(raw: str, route_label: str) -> dict:
    """Strip fences and parse JSON. Raises HTTPException on parse failure."""
    cleaned = _strip_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error(f"[{route_label}] JSON parse failed. Raw text: {raw[:300]} | Error: {exc}")
        raise HTTPException(status_code=502, detail={"message": "AI returned an invalid format. Please retry.", "code": "PARSE_ERROR"})


# ---------------------------------------------------------------------------
# 1. HOOK GENERATOR
# ---------------------------------------------------------------------------

class HookInput(BaseModel):
    niche: str = Field(..., min_length=2, description="Content niche or industry")
    audience: str = Field(..., min_length=2, description="Target audience description")
    platform: Literal["Instagram", "YouTube", "Facebook", "LinkedIn"] = Field(..., description="Publishing platform")
    count: int = Field(default=10, ge=1, le=50, description="Number of hooks to generate")
    language: str = Field(default="English", description="Language for the hooks")
    hook_type: str = Field(default="Mixed", description="Hook framework type (Curiosity, Fear, Pain, etc.)")
    goal: str = Field(default="Stop Scroll", description="Scroll goal")
    length: str = Field(default="Medium", description="Hook length: Short, Medium, Long")
    cta: bool = Field(default=True, description="Include call-to-action at end")
    emojis: bool = Field(default=True, description="Include emojis in hooks")

def _build_hook_prompt(inp: HookInput) -> str:
    length_guide = {
        "Short": "under 8 words — punchy, one-liner",
        "Medium": "8–15 words — contextual but concise",
        "Long": "15–25 words — detailed story or vivid setup",
    }.get(inp.length, "8–15 words")

    hook_type_instruction = ""
    if inp.hook_type and inp.hook_type.lower() not in ("mixed", ""):
        hook_type_instruction = f"- FOCUS primarily on the '{inp.hook_type}' hook framework\n"
    else:
        hook_type_instruction = (
            "- Mix types evenly:\n"
            "  * pain — addresses a real frustration or problem\n"
            "  * curiosity — creates an irresistible information gap\n"
            "  * question — rhetorical or direct question that stops scrolling\n"
            "  * shock — surprising fact, contrarian or counter-intuitive claim\n"
            "  * story — opens a narrative the reader must finish\n"
            "  * future — paints a vivid transformation or future state\n"
        )

    emoji_rule = "- Use relevant emojis naturally in hooks" if inp.emojis else "- NO emojis"
    cta_rule = f"- Add a short CTA line (e.g. 'Link in bio', 'Save this') after each hook as a 'cta' field" if inp.cta else "- Do NOT include any CTA"
    language_instruction = f"- Write ALL hooks in {inp.language} language (strictly {inp.language} only, no other language)"

    return f"""You are a world-class viral content strategist creating scroll-stopping hooks for {inp.platform}.

Generate exactly {inp.count} high-converting hooks for:

NICHE: {inp.niche}
TARGET AUDIENCE: {inp.audience}
PLATFORM: {inp.platform}
GOAL: {inp.goal}

REQUIREMENTS:
- Each hook length: {length_guide}
- Sound 100% native to {inp.platform}
{language_instruction}
{hook_type_instruction}{emoji_rule}
{cta_rule}

Respond ONLY with valid JSON — no markdown fences, no preamble:
{{
  "hooks": [
    {{ "type": "pain", "text": "...", "cta": "..." }},
    {{ "type": "curiosity", "text": "...", "cta": "..." }}
  ]
}}

Generate exactly {inp.count} hooks. Start the JSON object immediately."""

@router.post("/hooks")
async def generate_hooks(body: HookInput):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail={"message": "GEMINI_API_KEY is not configured on the server."})
    prompt = _build_hook_prompt(body)
    raw = await _call_gemini(prompt, model=FLASH_LITE, temperature=0.9, max_tokens=4000, responseMimeType="application/json")
    output = _parse_json(raw, "hooks")
    return {"output": output}


# ---------------------------------------------------------------------------
# 2. IMAGE PROMPT GENERATOR
# ---------------------------------------------------------------------------

class ImagePromptInput(BaseModel):
    business: str = Field(default="", description="Business name")
    industry: str = Field(default="", description="Industry")
    subject: str = Field(..., min_length=2, description="Visual subject or scene description")
    topic: str = Field(default="", description="Campaign topic")
    offer: str = Field(default="", description="Offer or campaign name")
    purpose: str = Field(default="Social Media", description="Image purpose (poster, banner, etc.)")
    style: str = Field(default="Cinematic", description="Visual style")
    engine: str = Field(default="FLUX", description="Render engine preset")
    aspect: str = Field(default="16:9", description="Aspect ratio")
    resolution: str = Field(default="4K", description="Output resolution")
    lighting: str = Field(default="Golden Hour", description="Lighting style")
    camera: str = Field(default="DSLR", description="Camera type")
    lens: str = Field(default="50mm", description="Lens focal length")
    color_theme: str = Field(default="", description="Color palette")
    background: str = Field(default="Gradient", description="Background style")
    negative: str = Field(default="lowres, blurry, watermark", description="Negative prompt elements")
    ref_style: str = Field(default="Commercial Safe", description="Reference style")
    high_detail: bool = Field(default=True, description="Enable high detail")
    ultra_quality: bool = Field(default=True, description="Enable ultra quality boosters")

def _build_image_prompt(inp: ImagePromptInput) -> str:
    quality_flags = []
    if inp.ultra_quality:
        quality_flags.append("ultra-detailed, 8K, hyperrealistic, sharp focus, award-winning photography")
    if inp.high_detail:
        quality_flags.append("intricate details, fine textures, depth of field")
    quality_str = ", ".join(quality_flags) if quality_flags else "high quality"

    context_parts = []
    if inp.business:
        context_parts.append(f"Business: {inp.business}")
    if inp.industry:
        context_parts.append(f"Industry: {inp.industry}")
    if inp.topic:
        context_parts.append(f"Campaign Topic: {inp.topic}")
    if inp.offer:
        context_parts.append(f"Offer: {inp.offer}")
    context_str = "\n".join(context_parts)

    return f"""You are a world-class AI image prompt engineer specializing in commercial advertising and brand photography.

Generate a complete, production-ready image prompt for:

SUBJECT: {inp.subject}
PURPOSE: {inp.purpose}
{context_str}

TECHNICAL SPECIFICATIONS:
- Visual Style: {inp.style}
- Target Engine: {inp.engine}
- Aspect Ratio: {inp.aspect}
- Resolution: {inp.resolution}
- Lighting: {inp.lighting}
- Camera: {inp.camera}
- Lens: {inp.lens}mm
- Color Theme: {inp.color_theme if inp.color_theme else "Natural, on-brand tones"}
- Background: {inp.background}
- Reference Style: {inp.ref_style}
- Quality Boosters: {quality_str}

DELIVERABLES:
1. image_prompt — A rich, dense, technically precise prompt optimized for {inp.engine}. Include subject details, environment, lighting, camera settings, and mood. Keep under 250 words.
2. negative_prompt — Include: {inp.negative}, plus style-specific exclusions (if photorealistic: no cartoon; if artistic: no photo noise).
3. suggested_tool — Exactly ONE of: "Midjourney", "DALL-E", or "Stable Diffusion" based on the style ({inp.style} and engine {inp.engine}).

Respond ONLY with valid JSON — no markdown fences, no preamble:
{{
  "image_prompt": "...",
  "negative_prompt": "...",
  "suggested_tool": "Midjourney"
}}

Start the JSON object immediately."""

@router.post("/image-prompt")
async def generate_image_prompt(body: ImagePromptInput):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail={"message": "GEMINI_API_KEY is not configured on the server."})
    prompt = _build_image_prompt(body)
    raw = await _call_gemini(prompt, model=FLASH_LITE, temperature=0.8, max_tokens=2000, responseMimeType="application/json")
    output = _parse_json(raw, "image-prompt")
    return {"output": output}


# ---------------------------------------------------------------------------
# 3. VIDEO SCRIPT GENERATOR
# ---------------------------------------------------------------------------

class VideoScriptInput(BaseModel):
    business: str = Field(..., min_length=2, description="Business name")
    industry: str = Field(default="", description="Industry / niche")
    platform: str = Field(default="Instagram Reel", description="Publishing platform")
    duration: str = Field(default="30 sec", description="Video duration label")
    duration_seconds: int = Field(default=30, ge=15, le=600, description="Duration in seconds")
    style: str = Field(default="Educational", description="Video content style")
    hook_type: str = Field(default="Pain Point", description="Hook framework")
    audience: str = Field(default="General", description="Target audience")
    language: str = Field(default="English", description="Script language")
    tone: str = Field(default="Conversational", description="Tone of voice")
    cta_style: str = Field(default="Strong", description="CTA style")
    visual_style: str = Field(default="Talking Head", description="Visual/shooting style")
    include_breakdown: bool = Field(default=True, description="Include shot/scene breakdown")
    include_angles: bool = Field(default=True, description="Include camera angles")
    include_shot_list: bool = Field(default=True, description="Include shot list")
    include_vo_script: bool = Field(default=True, description="Include voiceover script")
    include_caption: bool = Field(default=True, description="Include social caption")
    include_hashtags: bool = Field(default=True, description="Include hashtags")
    include_thumbnail: bool = Field(default=True, description="Include thumbnail concept")
    include_youtube_desc: bool = Field(default=False, description="Include YouTube description")

def _build_video_script_prompt(inp: VideoScriptInput) -> str:
    words_per_second = 2.5
    approx_words = int(inp.duration_seconds * words_per_second)

    optional_sections = []
    if inp.include_breakdown:
        optional_sections.append('- scene_breakdown: Array of scenes with [SCENE N], timing, action description, and b-roll note')
    if inp.include_angles:
        optional_sections.append('- camera_angles: Array of recommended camera shot types for each key moment')
    if inp.include_shot_list:
        optional_sections.append('- shot_list: A numbered production shot list (e.g. "1. Wide establishing — gym exterior, morning light")')
    if inp.include_caption:
        optional_sections.append('- social_caption: A ready-to-post caption with strong opening line and soft CTA')
    if inp.include_hashtags:
        optional_sections.append('- hashtags: 15–20 niche-specific hashtags as a single string')
    if inp.include_thumbnail:
        optional_sections.append('- thumbnail_concept: One-line description of the ideal thumbnail image')
    if inp.include_youtube_desc:
        optional_sections.append('- youtube_description: Full YouTube video description with timestamps, keywords, and links section')

    optional_str = "\n".join(optional_sections)

    return f"""You are an expert video script writer specialising in viral {inp.platform} content for {inp.industry} businesses.

Write a complete, production-ready {inp.duration} video script for:

BUSINESS: {inp.business}
INDUSTRY: {inp.industry}
PLATFORM: {inp.platform}
DURATION: {inp.duration_seconds} seconds (~{approx_words} spoken words)
STYLE: {inp.style}
HOOK TYPE: {inp.hook_type}
TARGET AUDIENCE: {inp.audience}
LANGUAGE: {inp.language} — write all spoken lines in {inp.language}
TONE: {inp.tone}
CTA STYLE: {inp.cta_style}
VISUAL FORMAT: {inp.visual_style}

REQUIRED OUTPUT FIELDS:
- hook: First 3-5 seconds. {inp.hook_type}-style pattern-interrupt opening. Must stop scroll immediately.
- script: Full body spoken dialogue in {inp.language}. Include [SECTION] headers, [0:00] timing cues, (B-roll suggestions), CAPS for emphasis. Must fit {inp.duration_seconds}s.
- cta: Final {inp.cta_style} call-to-action. Specific, actionable.
{optional_str}

Respond ONLY with valid JSON — no markdown fences, no preamble:
{{
  "hook": "...",
  "script": "...",
  "cta": "...",
  "scene_breakdown": [],
  "camera_angles": [],
  "shot_list": [],
  "social_caption": "...",
  "hashtags": "...",
  "thumbnail_concept": "...",
  "youtube_description": "..."
}}

Only include fields that were requested in REQUIRED OUTPUT FIELDS. Start the JSON object immediately."""

@router.post("/video-script")
async def generate_video_script(body: VideoScriptInput):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail={"message": "GEMINI_API_KEY is not configured on the server."})
    prompt = _build_video_script_prompt(body)
    raw = await _call_gemini(prompt, model=FLASH, temperature=0.8, max_tokens=4000, responseMimeType="application/json")
    output = _parse_json(raw, "video-script")
    return {"output": output}


# ---------------------------------------------------------------------------
# 4. CONTENT WRITER
# ---------------------------------------------------------------------------

class ContentWriterInput(BaseModel):
    business: str = Field(..., min_length=2, description="Business name or description")
    industry: str = Field(default="", description="Industry or niche")
    goal: str = Field(..., min_length=2, description="Marketing goal or campaign objective")
    format: Literal["caption", "ad", "blog"] = Field(..., description="Output content format")
    language: str = Field(default="English", description="Output language")
    tone: str = Field(default="Professional", description="Tone of voice")
    audience: str = Field(default="General audience", description="Target audience")
    platform: str = Field(default="Instagram", description="Publishing platform")
    offer: str = Field(default="", description="Specific offer or product")
    include_emojis: bool = Field(default=True, description="Include emojis in output")
    include_hashtags: bool = Field(default=True, description="Include hashtags")

def _build_content_writer_prompt(inp: ContentWriterInput) -> str:
    emoji_rule = "Include relevant emojis naturally" if inp.include_emojis else "No emojis"
    hashtag_rule = f"Include 10-15 niche hashtags at the end" if inp.include_hashtags else "No hashtags"
    offer_str = f"OFFER/PRODUCT: {inp.offer}" if inp.offer else ""

    if inp.format == "caption":
        output_spec = f"""Generate 5 unique {inp.platform} captions. Each should:
- Have a strong opening line with psychological pull
- Be written in {inp.language} language with a {inp.tone} tone
- Target: {inp.audience}
- {emoji_rule}
- {hashtag_rule}
- Vary in style: professional, conversational, storytelling, punchy, emotional

Output JSON shape:
{{
  "captions": ["caption 1", "caption 2", "caption 3", "caption 4", "caption 5"]
}}"""
    elif inp.format == "ad":
        output_spec = f"""Write a high-converting paid ad copy set for {inp.platform}. Include:
- headline: Short, punchy, benefit-first (max 8 words). Language: {inp.language}.
- primary_text: Main ad body in {inp.language}. {inp.tone} tone targeting {inp.audience}. 2-3 short paragraphs. Lead with pain/desire, introduce solution, build credibility. Max 125 words.
- cta: The button/link text (2-5 words). Specific, not generic. Language: {inp.language}.
- {emoji_rule}

Output JSON shape:
{{
  "headline": "...",
  "primary_text": "...",
  "cta": "..."
}}"""
    else:  # blog
        output_spec = f"""Write a full SEO-optimised blog article in {inp.language}. Include:
- title: SEO-optimised H1 title with primary keyword for {inp.industry}
- meta_description: 150-160 character meta description. Include keyword, benefit, CTA.
- body: Full article in markdown. Tone: {inp.tone}. Target reader: {inp.audience}. Include:
  * H2 and H3 subheadings
  * Introduction that hooks immediately
  * 3-5 main sections with actionable insights
  * Conclusion with summary and CTA pointing to the offer
  * Minimum 700 words

Output JSON shape:
{{
  "title": "...",
  "meta_description": "...",
  "body": "..."
}}"""

    return f"""You are a senior copywriter and content strategist. You write copy that converts, not just reads well.

Create {inp.format} content for the following brief:

BUSINESS: {inp.business}
INDUSTRY: {inp.industry}
CAMPAIGN GOAL: {inp.goal}
PLATFORM: {inp.platform}
{offer_str}
FORMAT: {inp.format}

{output_spec}

Respond ONLY with valid JSON — no markdown fences, no preamble, no explanation outside the JSON.
Start the JSON object immediately."""

@router.post("/content-writer")
async def generate_content(body: ContentWriterInput):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail={"message": "GEMINI_API_KEY is not configured on the server."})
    model = FLASH if body.format == "blog" else FLASH_LITE
    prompt = _build_content_writer_prompt(body)
    raw = await _call_gemini(prompt, model=model, temperature=0.8, max_tokens=4000 if body.format == "blog" else 2500, responseMimeType="application/json")
    output = _parse_json(raw, "content-writer")
    return {"output": output}


# ---------------------------------------------------------------------------
# 5. AI CHAT
# ---------------------------------------------------------------------------

class ChatMessageHistoryItem(BaseModel):
    role: Literal["user", "ai"]
    text: str

class ChatInput(BaseModel):
    message: str = Field(..., description="User's chat message")
    history: Optional[List[ChatMessageHistoryItem]] = Field(default=None, description="Conversation history")

def _build_chat_prompt(inp: ChatInput) -> str:
    system_instruction = (
        "You are Digital Saathi (डिजिटल साथी), the official expert AI copilot for 'The Digital Saathi' platform.\n\n"
        "Your mission is to help users generate marketing copy, campaigns, or guide them on how to get the best out of the platform tools.\n\n"
        "Here are the specific tools built into The Digital Saathi app that you can suggest or help users with:\n"
        "1. Viral Hooks Generator: Generates 20 scroll-stopping hooks for Instagram, YouTube, Facebook, or LinkedIn based on a niche and target audience.\n"
        "2. Video Script Generator: Creates a complete production script with hooks, spoken copy, CTAs, visual scene descriptions, and camera angles for any duration.\n"
        "3. Image Prompt Generator: Crafts highly detailed Midjourney, DALL-E, or Stable Diffusion prompts along with negative prompts.\n"
        "4. Local Leads Finder: Finds local business listings, phone numbers, ratings, and competitors in any Indian city.\n"
        "5. Prompt Generator (AI Brief Engine): Generates highly optimized system prompts using brand inputs like Business Name, Industry, and Platform.\n\n"
        "Tone and Behavior Guidelines:\n"
        "- Be highly professional, actionable, and encouraging.\n"
        "- When asked for scripts, hooks, or image prompts, always output a draft immediately, and gently remind them they can use the dedicated generator tab in the sidebar for structured, production-ready exports.\n"
        "- Language Flexibility: You understand all languages perfectly (English, Hindi, Hinglish, Tamil, Telugu, Spanish, etc.). Always match the script and language style the user uses. If the user writes in Hinglish (Hindi written in English alphabet), reply in Hinglish. If they write in Devanagari Hindi, reply in Devanagari Hindi. If they write in English, reply in English."
    )
    
    context = ""
    if inp.history:
        context = "Conversation history:\n"
        # Only take the last 10 turns to avoid token limit issues
        for msg in inp.history[-10:]:
            role_name = "User" if msg.role == "user" else "Digital Saathi"
            context += f"{role_name}: {msg.text}\n"
        context += "\n"
        
    return f"{system_instruction}\n\n{context}User: {inp.message}\nDigital Saathi:"

@router.post("/chat")
async def generate_chat(body: ChatInput):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail={"message": "GEMINI_API_KEY is not configured on the server."})
    prompt = _build_chat_prompt(body)
    raw = await _call_gemini(prompt, model=FLASH_LITE, temperature=0.7, max_tokens=1500)
    return {"output": raw}


# ---------------------------------------------------------------------------
# 6. PROMPT GENERATOR
# ---------------------------------------------------------------------------

class PromptGeneratorInput(BaseModel):
    business: str = Field(..., description="Business name")
    industry: str = Field(..., description="Industry")
    sub_industry: Optional[str] = Field(default="", description="Sub-industry")
    description: Optional[str] = Field(default="", description="Business description")
    category: str = Field(..., description="Prompt category")
    prompt_type: str = Field(..., description="Type of prompt to generate")
    audience: str = Field(..., description="Target audience")
    age_group: Optional[str] = Field(default="", description="Age group")
    location: Optional[str] = Field(default="", description="Location")
    language: str = Field(default="English", description="Target language")
    gender: Optional[str] = Field(default="All Genders", description="Gender demographic")
    pain_points: Optional[str] = Field(default="", description="Audience pain points")
    goal: str = Field(..., description="Marketing goal")
    offer: str = Field(..., description="Product offer/details")
    platform: str = Field(..., description="Publishing platform")
    tone: str = Field(default="Professional", description="Tone style")
    depth: str = Field(default="Advanced", description="Depth preset")
    model: str = Field(default="Gemini", description="Target AI model")
    length: str = Field(default="Medium", description="Output length")
    creativity: int = Field(default=7, description="Creativity level 1-10")
    cta: bool = Field(default=True, description="Include call to action")
    hashtags: bool = Field(default=True, description="Include hashtags")
    emojis: bool = Field(default=True, description="Include emojis")
    seo_keywords: bool = Field(default=True, description="Enable SEO keyword optimization")
    competitor: bool = Field(default=True, description="Enable competitor analysis angle")
    multiple_versions: bool = Field(default=False, description="Generate multiple versions")
    variations_count: int = Field(default=3, description="Number of variations")

def _build_prompt_generator_prompt(inp: PromptGeneratorInput) -> str:
    emoji_str = "Include relevant emojis naturally" if inp.emojis else "Strictly NO emojis"
    cta_str = "Include a compelling, specific call-to-action (CTA)" if inp.cta else "Do NOT include any CTA"
    hashtag_str = "Include trending and contextual hashtags" if inp.hashtags else "Strictly NO hashtags"
    seo_str = "Identify and optimize for relevant SEO keywords based on the industry" if inp.seo_keywords else "No specific SEO keyword emphasis"
    competitor_str = "Acknowledge and differentiate from common competitor angles" if inp.competitor else "No competitor positioning required"
    var_str = f"Include {inp.variations_count} distinct alternative drafts" if inp.multiple_versions else "Provide one master draft"

    return f"""You are a master AI Prompt Engineer specializing in advanced prompt design, meta-prompting, and custom system instructions.

Generate a highly optimized prompt kit for:

BUSINESS: {inp.business}
INDUSTRY: {inp.industry} / {inp.sub_industry}
BUSINESS DESCRIPTION: {inp.description}
CATEGORY: {inp.category}
PROMPT TYPE: {inp.prompt_type}
GOAL: {inp.goal}
OFFER: {inp.offer}
PLATFORM: {inp.platform}

AUDIENCE PARAMETERS:
- Target Audience: {inp.audience}
- Age Group: {inp.age_group}
- Gender: {inp.gender}
- Location: {inp.location}
- Main Pain Points: {inp.pain_points}

OUTPUT & WRITING CONSTRAINTS:
- Language: {inp.language}
- Tone of Voice: {inp.tone}
- Depth Level: {inp.depth} (Strategy Depth)
- Target LLM Model: {inp.model}
- Expected Length: {inp.length}
- Creativity Level: {inp.creativity}/10 (higher means more out-of-the-box ideas)
- Constraints: {emoji_str}, {cta_str}, {hashtag_str}.
- Focuses: {seo_str}. {competitor_str}.
- Variations: {var_str}.

DELIVERABLES:
1. expert_prompt — A comprehensive, master-level system prompt or role-play instruction sheet (e.g. "Act as a...") designed to be entered as system guidelines in {inp.model} or Claude. It must clearly outline the role, context, goal, audience pain points, tone, constraints, and structural breakdown of the output.
2. optimized_prompt — A shorter, copy-paste prompt that can be used directly in any standard chat window for a fast, high-quality response.
3. gemini_prompt — A prompt optimized specifically for Gemini's capabilities, utilizing structured XML-like tags (e.g., <context>, <instructions>, <audience>, <constraints>) to guide the model.
4. explanation — A breakdown of the prompt design strategy, pointing out which elements target which pain points/goals, and instructions on how the user should customize it.

Respond ONLY with valid JSON — no markdown fences, no preamble, no explanation outside the JSON:
{{
  "expert_prompt": "...",
  "optimized_prompt": "...",
  "gemini_prompt": "...",
  "explanation": "..."
}}

Start the JSON object immediately."""

@router.post("/prompt")
async def generate_prompt(body: PromptGeneratorInput):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail={"message": "GEMINI_API_KEY is not configured on the server."})
    prompt = _build_prompt_generator_prompt(body)
    raw = await _call_gemini(prompt, model=FLASH, temperature=0.8, max_tokens=3500, responseMimeType="application/json")
    output = _parse_json(raw, "prompt")
    return {"output": output}


