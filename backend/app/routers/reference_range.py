from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reference_ranges", tags=["reference_ranges"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_reference_range(
    reference_range: schemas.ReferenceRangeCreate, db: Session = Depends(get_db)
):
    db_reference_range = models.ReferenceRange(**reference_range.dict())
    db.add(db_reference_range)
    db.commit()
    db.refresh(db_reference_range)
    return db_reference_range


@router.get("/")
def list_reference_ranges(db: Session = Depends(get_db)):
    return db.query(models.ReferenceRange).all()


@router.get("/{loinc_code}")
def get_reference_range(loinc_code: str, db: Session = Depends(get_db)):
    reference_range = (
        db.query(models.ReferenceRange)
        .filter(models.ReferenceRange.loinc_code == loinc_code)
        .first()
    )
    if not reference_range:
        raise HTTPException(status_code=404, detail="Reference range not found")
    return reference_range
