from typing import List, Optional
from pydantic import BaseModel, Field

class PromptGeneratorRequest(BaseModel):
    text: str = Field(..., description="Hindi or English instruction, e.g. 'Shoe brand ke liye ad banana hai'")

class PromptGeneratorResponse(BaseModel):
    chatgpt_prompt: str
    gemini_prompt: str
    claude_prompt: str

class ScriptGeneratorRequest(BaseModel):
    topic: str = Field(..., description="Topic of the script, e.g., 'Travel Agency'")
    platform: Optional[str] = Field("reels", description="reels, shorts, youtube, ads")

class ScriptGeneratorResponse(BaseModel):
    hook: str
    intro: str
    body: str
    cta: str

class ViralHooksRequest(BaseModel):
    topic: str = Field(..., description="Topic for viral hooks")

class ViralHooksResponse(BaseModel):
    hooks: List[str]

class ImagePromptRequest(BaseModel):
    text: str = Field(..., description="Image description, e.g. 'Leather Jacket Poster'")

class ImagePromptResponse(BaseModel):
    midjourney: str
    dalle: str
    leonardo: str
    stable_diffusion: str

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for image generation")
    provider: Optional[str] = Field("flux", description="flux, stability, openai")

class ImageGenerationResponse(BaseModel):
    image_url: str
