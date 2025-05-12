from datetime import datetime

from app import database
from app.models import Patient, PatientHistory
from app.schemas import Patient as PatientSchema
from app.schemas import PatientCreate, PatientUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/patient", tags=["Patient"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=PatientSchema)
# Create a new patient
# Operation: CREATE
# Description: Adds a new patient to the database with versioning.
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(**patient_in.dict(), version=1)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/all", response_model=list[PatientSchema])
# List all patients
# Operation: READ (LIST)
# Description: Retrieves all patients from the database.
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()


@router.get("/{patient_id}", response_model=PatientSchema)
# Get a specific patient by ID
# Operation: READ (GET)
# Description: Retrieves a single patient by its ID.
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/update/{patient_id}", response_model=PatientSchema)
# Update a specific patient by ID
# Operation: UPDATE
# Description: Updates a patient and archives the previous state in the history table.
def update_patient(patient_id: int, patient_in: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Archive current state
    history = PatientHistory(
        patient_id=patient.id,
        first_name=patient.first_name,
        last_name=patient.last_name,
        sex=patient.sex,
        identifier=patient.identifier,
        version=patient.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in patient_in.dict().items():
        setattr(patient, field, value)
    setattr(patient, "version", patient.version + 1)

    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/delete/{patient_id}")
# Delete a specific patient by ID
# Operation: DELETE
# Description: Deletes a patient and its associated history records.
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Delete from history table
    db.query(PatientHistory).filter(PatientHistory.patient_id == patient_id).delete()

    # Delete from main table
    db.delete(patient)
    db.commit()
    return {"ok": True}
