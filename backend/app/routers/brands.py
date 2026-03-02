from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.session import get_db
from ..models.brand import Brand
from ..schemas.brand import BrandCreate, BrandResponse
from ..core.dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.post("/", response_model=BrandResponse)
def create_brand(
    brand_data: BrandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brand = Brand(
        owner_id = current_user.id,
        name = brand_data.name,
        brand_tone = brand_data.brand_tone,
        target_audience = brand_data.target_audience,
        brand_guidelines_json = brand_data.brand_guidelines_json
    )

    db.add(brand)
    db.commit()
    db.refresh(brand)

    return brand


@router.get("/", response_model=List[BrandResponse])
def get_my_brands(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brands = db.query(Brand).filter(Brand.owner_id == current_user.id).all()
    return brands