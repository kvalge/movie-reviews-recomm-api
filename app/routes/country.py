from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.country import CountryService
from app.schemas.country import CountryOut

router = APIRouter(prefix="/api/countries", tags=["Countries"])


@router.get("/", response_model=List[CountryOut])
def get_all_countries(db: Session = Depends(get_db)):
    country_service = CountryService(db)
    return country_service.get_all_countries()


@router.get("/{country_id}", response_model=CountryOut)
def get_country(country_id: int, db: Session = Depends(get_db)):
    country_service = CountryService(db)
    country = country_service.get_country_by_id(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country 