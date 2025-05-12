from datetime import datetime

from app import database
from app.models import LabAnalyteResult, LabAnalyteResultHistory
from app.schemas import LabAnalyteResult as LabAnalyteResultSchema
from app.schemas import LabAnalyteResultCreate, LabAnalyteResultUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/lab_analyte", tags=["Lab Analyte Result"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=LabAnalyteResultSchema)
# Create a new lab analyte result
# Operation: CREATE
# Description: Adds a new lab analyte result to the database with versioning.
def create_lab_analyte_result(lab_analyte: LabAnalyteResultCreate, db: Session = Depends(get_db)):
    db_lab_analyte = LabAnalyteResult(**lab_analyte.dict(), version=1)
    db.add(db_lab_analyte)
    db.commit()
    db.refresh(db_lab_analyte)
    return db_lab_analyte


@router.get("/all", response_model=list[LabAnalyteResultSchema])
# List all lab analyte results
# Operation: READ (LIST)
# Description: Retrieves all lab analyte results from the database.
def list_lab_analyte_results(db: Session = Depends(get_db)):
    return db.query(LabAnalyteResult).all()


@router.get("/{lab_analyte_result_id}", response_model=LabAnalyteResultSchema)
# Get a specific lab analyte result by ID
# Operation: READ (GET)
# Description: Retrieves a single lab analyte result by its ID.
def get_lab_analyte_result(lab_analyte_result_id: int, db: Session = Depends(get_db)):
    lab_analyte = (
        db.query(LabAnalyteResult).filter(LabAnalyteResult.id == lab_analyte_result_id).first()
    )
    if not lab_analyte:
        raise HTTPException(status_code=404, detail="Lab analyte result not found")
    return lab_analyte


@router.put("/update/{lab_analyte_result_id}", response_model=LabAnalyteResultSchema)
# Update a specific lab analyte result by ID
# Operation: UPDATE
# Description: Updates a lab analyte result and archives the previous state in the history table.
def update_lab_analyte_result(
    lab_analyte_result_id: int,
    lab_analyte_in: LabAnalyteResultUpdate,
    db: Session = Depends(get_db),
):
    db_lab_analyte = (
        db.query(LabAnalyteResult).filter(LabAnalyteResult.id == lab_analyte_result_id).first()
    )
    if not db_lab_analyte:
        raise HTTPException(status_code=404, detail="Lab analyte result not found")

    history = LabAnalyteResultHistory(
        lab_analyte_result_id=db_lab_analyte.id,
        lab_test_id=db_lab_analyte.lab_test_id,
        loinc_code=db_lab_analyte.loinc_code,
        value=db_lab_analyte.value,
        unit=db_lab_analyte.unit,
        reference_low=db_lab_analyte.reference_low,
        reference_high=db_lab_analyte.reference_high,
        interpretation=db_lab_analyte.interpretation,
        version=db_lab_analyte.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    for field, value in lab_analyte_in.dict(exclude_unset=True).items():
        setattr(db_lab_analyte, field, value)
    setattr(db_lab_analyte, "version", db_lab_analyte.version + 1)

    db.commit()
    db.refresh(db_lab_analyte)
    return db_lab_analyte


@router.delete("/delete/{lab_analyte_result_id}")
# Delete a specific lab analyte result by ID
# Operation: DELETE
# Description: Deletes a lab analyte result and its associated history records.
def delete_lab_analyte_result(lab_analyte_result_id: int, db: Session = Depends(get_db)):
    db_lab_analyte = (
        db.query(LabAnalyteResult).filter(LabAnalyteResult.id == lab_analyte_result_id).first()
    )
    if not db_lab_analyte:
        raise HTTPException(status_code=404, detail="Lab analyte result not found")

    db.query(LabAnalyteResultHistory).filter(
        LabAnalyteResultHistory.lab_analyte_result_id == lab_analyte_result_id
    ).delete()

    db.delete(db_lab_analyte)
    db.commit()
    return {"ok": True}
