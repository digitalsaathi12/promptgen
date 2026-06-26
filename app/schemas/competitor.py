from typing import List, Dict, Optional
from pydantic import BaseModel, Field, HttpUrl

class CompetitorAnalysisRequest(BaseModel):
    website: str = Field(..., description="Website URL, e.g. 'example.com' or 'https://example.com'")

class MetaTagsModel(BaseModel):
    title: str
    description: str

class CompetitorAnalysisResponse(BaseModel):
    seo_score: str
    keywords: List[str]
    meta_tags: MetaTagsModel
    social_presence: List[str]
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
