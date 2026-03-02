from uuid import UUID
from pydantic import BaseModel
from typing import Optional, Dict, Any

class BrandCreate(BaseModel):
    name: str
    brand_tone: Optional[str] = None
    target_audience: Optional[str] = None
    brand_guidelines_json: Optional[Dict[str, Any]] = None

class BrandResponse(BaseModel):
    id: UUID
    name: str
    brand_tone: Optional[str]
    target_audience: Optional[str]

    class Config:
        from_attributes = True