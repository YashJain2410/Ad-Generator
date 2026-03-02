from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.session import get_db
from ..models.project import Project
from ..models.brand import Brand
from ..schemas.project import ProjectCreate, ProjectResponse
from ..core.dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brand = db.query(Brand).filter(
        Brand.id == project_data.brand_id,
        Brand.owner_id == current_user.id
    ).first()

    if not brand:
        raise HTTPException(status_code=403, detail="Not authorized for this brand")
    
    project = Project(
        brand_id = project_data.brand_id,
        platform_target = project_data.platform_target,
        design_brief = project_data.design_brief,
        sop_text = project_data.sop_text
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/brand/{brand_id}", response_model=List[ProjectResponse])
def get_projects_by_brand(
    brand_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brand = db.query(Brand).filter(
        Brand.id == brand_id,
        Brand.owner_id == current_user.id
    ).first()

    if not brand:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    projects = db.query(Project).filter(Project.brand_id == brand_id).all()
    return projects