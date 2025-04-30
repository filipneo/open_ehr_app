from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/lab_analytes", tags=["lab_analytes"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_lab_analyte(lab_analyte: schemas.LabAnalyteResultCreate, db: Session = Depends(get_db)):
    db_lab_analyte = models.LabAnalyteResult(**lab_analyte.dict())
    db.add(db_lab_analyte)
    db.commit()
    db.refresh(db_lab_analyte)
    return db_lab_analyte


@router.get("/")
def list_lab_analytes(db: Session = Depends(get_db)):
    return db.query(models.LabAnalyteResult).all()


@router.get("/{lab_analyte_id}")
def get_lab_analyte(lab_analyte_id: int, db: Session = Depends(get_db)):
    lab_analyte = (
        db.query(models.LabAnalyteResult)
        .filter(models.LabAnalyteResult.id == lab_analyte_id)
        .first()
    )
    if not lab_analyte:
        raise HTTPException(status_code=404, detail="Lab analyte result not found")
    return lab_analyte
