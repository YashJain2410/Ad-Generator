import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models.asset import Asset
from ..models.project import Project
from ..models.brand import Brand
from ..schemas.asset import AssetResponse
from ..core.dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/assets", tags=["Assets"])

UPLOAD_DIR = "uploads"

@router.post("/upload", response_model=AssetResponse)
def upload_asset(
    project_id: str = Form(...),
    asset_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    brand = db.query(Brand).filter(
        Brand.id == project.brand_id,
        Brand.owner_id == current_user.id
    ).first()

    if not brand:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Create project folder
    project_folder = os.path.join(UPLOAD_DIR, str(project_id))
    os.makedirs(project_folder, exist_ok=True)

    # Save file
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(project_folder, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save to DB
    asset = Asset(
        project_id = project_id,
        type = asset_type,
        file_url = file_path
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset