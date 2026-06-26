import datetime
from pydantic import BaseModel

class SavedResultCreate(BaseModel):
    title: str
    content: str
    type: str # e.g. "prompt", "script", "hook", "analysis"

class SavedResultOut(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    type: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
