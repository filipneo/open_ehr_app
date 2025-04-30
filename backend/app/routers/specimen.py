from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/specimens", tags=["specimens"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_specimen(specimen: schemas.SpecimenCreate, db: Session = Depends(get_db)):
    db_specimen = models.Specimen(**specimen.dict())
    db.add(db_specimen)
    db.commit()
    db.refresh(db_specimen)
    return db_specimen


@router.get("/")
def list_specimens(db: Session = Depends(get_db)):
    return db.query(models.Specimen).all()


@router.get("/{specimen_id}")
def get_specimen(specimen_id: int, db: Session = Depends(get_db)):
    specimen = db.query(models.Specimen).filter(models.Specimen.id == specimen_id).first()
    if not specimen:
        raise HTTPException(status_code=404, detail="Specimen not found")
    return specimen
