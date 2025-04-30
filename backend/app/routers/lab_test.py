from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/lab_tests", tags=["laboratory_tests"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_lab_test(lab_test: schemas.LabTestCreate, db: Session = Depends(get_db)):
    db_lab_test = models.LabTest(**lab_test.dict())
    db.add(db_lab_test)
    db.commit()
    db.refresh(db_lab_test)
    return db_lab_test


@router.get("/")
def list_lab_tests(db: Session = Depends(get_db)):
    return db.query(models.LabTest).all()


@router.get("/{lab_test_id}")
def get_lab_test(lab_test_id: int, db: Session = Depends(get_db)):
    lab_test = db.query(models.LabTest).filter(models.LabTest.id == lab_test_id).first()
    if not lab_test:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return lab_test


@router.delete("/{lab_test_id}")
def delete_lab_test(lab_test_id: int, db: Session = Depends(get_db)):
    lab_test = db.query(models.LabTest).filter(models.LabTest.id == lab_test_id).first()
    if not lab_test:
        raise HTTPException(status_code=404, detail="Lab test not found")
    db.delete(lab_test)
    db.commit()
    return {"message": "Lab test deleted successfully"}
