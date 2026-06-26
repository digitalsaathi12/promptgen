from typing import Optional
from pydantic import BaseModel

class AIModelCreate(BaseModel):
    name: str
    provider: str
    is_local: Optional[bool] = False
    is_active: Optional[bool] = True
    default_for: Optional[str] = None # "text", "image", etc.

class AIModelOut(BaseModel):
    id: str
    name: str
    provider: str
    is_local: bool
    is_active: bool
    default_for: Optional[str] = None

    class Config:
        from_attributes = True
