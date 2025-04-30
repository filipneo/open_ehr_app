from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/body_measurements", tags=["body_measurements"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_body_measurement(
    body_measurement: schemas.BodyMeasurementCreate, db: Session = Depends(get_db)
):
    db_body_measurement = models.BodyMeasurement(**body_measurement.dict())
    db.add(db_body_measurement)
    db.commit()
    db.refresh(db_body_measurement)
    return db_body_measurement


@router.get("/")
def list_body_measurements(db: Session = Depends(get_db)):
    return db.query(models.BodyMeasurement).all()


@router.get("/{body_measurement_id}")
def get_body_measurement(body_measurement_id: int, db: Session = Depends(get_db)):
    body_measurement = (
        db.query(models.BodyMeasurement)
        .filter(models.BodyMeasurement.id == body_measurement_id)
        .first()
    )
    if not body_measurement:
        raise HTTPException(status_code=404, detail="Body measurement not found")
    return body_measurement


@router.delete("/{body_measurement_id}")
def delete_body_measurement(body_measurement_id: int, db: Session = Depends(get_db)):
    body_measurement = (
        db.query(models.BodyMeasurement)
        .filter(models.BodyMeasurement.id == body_measurement_id)
        .first()
    )
    if not body_measurement:
        raise HTTPException(status_code=404, detail="Body measurement not found")
    db.delete(body_measurement)
    db.commit()
    return {"message": "Body measurement deleted successfully"}
