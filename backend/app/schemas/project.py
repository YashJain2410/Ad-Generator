from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):
    brand_id: str
    platform_target: str
    design_brief: Optional[str] = None
    sop_text: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    brand_id: str
    platform_target: str
    status: str

    class Config:
        from_attributes = True