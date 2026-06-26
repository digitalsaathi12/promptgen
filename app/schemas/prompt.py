import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator

class PromptCreate(BaseModel):
    title: str
    category: str
    subcategory: str
    description: Optional[str] = None
    prompt_text: str
    tags: Optional[str] = "" # Comma-separated tags, e.g. "marketing,seo"

class PromptOut(BaseModel):
    id: int
    title: str
    category: str
    subcategory: str
    description: Optional[str] = None
    prompt_text: str
    tags: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

    # Helper properties to convert tags between list and string
    @property
    def tags_list(self) -> List[str]:
        return [t.strip() for t in self.tags.split(",") if t.strip()]

class PromptUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    prompt_text: Optional[str] = None
    tags: Optional[str] = None
