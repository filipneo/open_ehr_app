from datetime import datetime

from app import database
from app.models import (
    BloodTypePanel,
    BodyMeasurement,
    CBCPanel,
    Composition,
    LabAnalyteResult,
    LabTest,
    Patient,
    PatientHistory,
    Specimen,
)
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


@router.get("/{patient_id}/full")
# Get a patient with all associated data
# Operation: READ (GET)
# Description: Retrieves a single patient by ID including all compositions, lab tests, specimens, and measurements.
def get_patient_full(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    compositions = db.query(Composition).filter(Composition.patient_id == patient.id).all()

    full_data = {
        "id": patient.id,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "sex": patient.sex,
        "identifier": patient.identifier,
        "version": patient.version,
        "compositions": [],
        "body_measurements": [],
    }

    for comp in compositions:
        lab_tests = db.query(LabTest).filter(LabTest.composition_id == comp.id).all()
        lab_test_data = []

        for test in lab_tests:
            specimen = db.query(Specimen).filter(Specimen.id == test.specimen_id).first()
            analytes = (
                db.query(LabAnalyteResult).filter(LabAnalyteResult.lab_test_id == test.id).all()
            )
            cbc_panel = db.query(CBCPanel).filter(CBCPanel.lab_test_id == test.id).first()
            blood_type_panel = (
                db.query(BloodTypePanel).filter(BloodTypePanel.lab_test_id == test.id).first()
            )

            lab_test_data.append(
                {
                    "id": test.id,
                    "loinc_code": test.loinc_code,
                    "version": test.version,
                    "specimen": {
                        "id": specimen.id,
                        "type": specimen.specimen_type,
                        "collection_time": specimen.collection_time,
                        "snomed_code": specimen.snomed_code,
                        "description": specimen.description,
                        "version": specimen.version,
                    }
                    if specimen
                    else None,
                    "analytes": [
                        {
                            "id": a.id,
                            "loinc_code": a.loinc_code,
                            "value": a.value,
                            "unit": a.unit,
                            "reference_low": a.reference_low,
                            "reference_high": a.reference_high,
                            "interpretation": a.interpretation,
                            "version": a.version,
                        }
                        for a in analytes
                    ],
                    "cbc_panel": {
                        "id": cbc_panel.id,
                        "hemoglobin_id": cbc_panel.hemoglobin_id,
                        "white_cell_id": cbc_panel.white_cell_id,
                        "platelet_id": cbc_panel.platelet_id,
                        "version": cbc_panel.version,
                    }
                    if cbc_panel
                    else None,
                    "blood_type_panel": {
                        "id": blood_type_panel.id,
                        "abo_id": blood_type_panel.abo_id,
                        "rh_id": blood_type_panel.rh_id,
                        "version": blood_type_panel.version,
                    }
                    if blood_type_panel
                    else None,
                }
            )

        full_data["compositions"].append(
            {
                "id": comp.id,
                "start_time": comp.start_time,
                "version": comp.version,
                "lab_tests": lab_test_data,
            }
        )

    measurements = db.query(BodyMeasurement).filter(BodyMeasurement.patient_id == patient.id).all()
    full_data["body_measurements"] = [
        {
            "id": m.id,
            "record_time": m.record_time,
            "value": m.value,
            "unit": m.unit,
            "snomed_code": m.snomed_code,
            "version": m.version,
        }
        for m in measurements
    ]

    return full_data
