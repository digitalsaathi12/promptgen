from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class GeneratorOut(BaseModel):
    id: str
    label: str
    config_json: Dict[str, Any]
    template_key: str
    is_active: bool

    class Config:
        from_attributes = True

class GeneratorGenerateRequest(BaseModel):
    payload: Dict[str, Any] = {} # raw input fields
    model_name: Optional[str] = "auto"
    temperature: Optional[float] = 0.7

class GeneratorGenerateResponse(BaseModel):
    constructed_prompt: str
    ai_model: str
    output: Dict[str, Any] # output segments returned by the model
