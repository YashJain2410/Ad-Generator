from pydantic import BaseModel
from typing import Optional, Dict, Any


class AssetResponse(BaseModel):
    id: str
    project_id: str
    type: str
    file_url: str

    class Config:
        from_attributes = True