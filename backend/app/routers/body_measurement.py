from datetime import datetime

from app import database
from app.models import BodyMeasurement, BodyMeasurementHistory
from app.schemas import BodyMeasurement as BodyMeasurementSchema
from app.schemas import BodyMeasurementCreate, BodyMeasurementUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/body_measurement", tags=["Body Measurement"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=BodyMeasurementSchema)
# Create a new body measurement
# Operation: CREATE
# Description: Adds a new body measurement to the database with versioning.
def create_body_measurement(body_measurement: BodyMeasurementCreate, db: Session = Depends(get_db)):
    db_body_measurement = BodyMeasurement(**body_measurement.dict(), version=1)
    db.add(db_body_measurement)
    db.commit()
    db.refresh(db_body_measurement)
    return db_body_measurement


@router.get("/all", response_model=list[BodyMeasurementSchema])
# List all body measurements
# Operation: READ (LIST)
# Description: Retrieves all body measurements from the database.
def list_body_measurements(db: Session = Depends(get_db)):
    return db.query(BodyMeasurement).all()


@router.get("/{body_measurement_id}", response_model=BodyMeasurementSchema)
# Get a specific body measurement by ID
# Operation: READ (GET)
# Description: Retrieves a single body measurement by its ID.
def get_body_measurement(body_measurement_id: int, db: Session = Depends(get_db)):
    body_measurement = (
        db.query(BodyMeasurement).filter(BodyMeasurement.id == body_measurement_id).first()
    )
    if not body_measurement:
        raise HTTPException(status_code=404, detail="Body measurement not found")
    return body_measurement


@router.put("/update/{body_measurement_id}", response_model=BodyMeasurementSchema)
# Update a specific body measurement by ID
# Operation: UPDATE
# Description: Updates a body measurement and archives the previous state in the history table.
def update_body_measurement(
    body_measurement_id: int,
    body_measurement_in: BodyMeasurementUpdate,
    db: Session = Depends(get_db),
):
    db_body_measurement = (
        db.query(BodyMeasurement).filter(BodyMeasurement.id == body_measurement_id).first()
    )
    if not db_body_measurement:
        raise HTTPException(status_code=404, detail="Body measurement not found")

    # Archive current state
    history = BodyMeasurementHistory(
        body_measurement_id=db_body_measurement.id,
        patient_id=db_body_measurement.patient_id,
        record_time=db_body_measurement.record_time,
        value=db_body_measurement.value,
        unit=db_body_measurement.unit,
        snomed_code=db_body_measurement.snomed_code,
        version=db_body_measurement.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in body_measurement_in.dict(exclude_unset=True).items():
        setattr(db_body_measurement, field, value)
    setattr(db_body_measurement, "version", db_body_measurement.version + 1)

    db.commit()
    db.refresh(db_body_measurement)
    return db_body_measurement


@router.delete("/delete/{body_measurement_id}")
# Delete a specific body measurement by ID
# Operation: DELETE
# Description: Deletes a body measurement and its associated history records.
def delete_body_measurement(body_measurement_id: int, db: Session = Depends(get_db)):
    body_measurement = (
        db.query(BodyMeasurement).filter(BodyMeasurement.id == body_measurement_id).first()
    )
    if not body_measurement:
        raise HTTPException(status_code=404, detail="Body measurement not found")

    # Delete from history table
    db.query(BodyMeasurementHistory).filter(
        BodyMeasurementHistory.body_measurement_id == body_measurement_id
    ).delete()

    db.delete(body_measurement)
    db.commit()
    return {"ok": True}
