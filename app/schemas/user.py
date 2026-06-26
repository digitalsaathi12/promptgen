import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    language_pref: str
    role: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    language_pref: Optional[str] = None
    password: Optional[str] = None
