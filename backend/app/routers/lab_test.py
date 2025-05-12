from datetime import datetime

from app import database
from app.models import LabTest, LabTestHistory
from app.schemas import LabTest as LabTestSchema
from app.schemas import LabTestCreate, LabTestUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/lab_tests", tags=["laboratory_tests"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=LabTestSchema)
# Create a new lab test
# Operation: CREATE
# Description: Adds a new lab test to the database with versioning.
def create_lab_test(lab_test: LabTestCreate, db: Session = Depends(get_db)):
    db_lab_test = LabTest(**lab_test.dict(), version=1)
    db.add(db_lab_test)
    db.commit()
    db.refresh(db_lab_test)
    return db_lab_test


@router.get("/", response_model=list[LabTestSchema])
# List all lab tests
# Operation: READ (LIST)
# Description: Retrieves all lab tests from the database.
def list_lab_tests(db: Session = Depends(get_db)):
    return db.query(LabTest).all()


@router.get("/{lab_test_id}", response_model=LabTestSchema)
# Get a specific lab test by ID
# Operation: READ (GET)
# Description: Retrieves a single lab test by its ID.
def get_lab_test(lab_test_id: int, db: Session = Depends(get_db)):
    lab_test = db.query(LabTest).filter(LabTest.id == lab_test_id).first()
    if not lab_test:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return lab_test


@router.put("/{lab_test_id}", response_model=LabTestSchema)
# Update a specific lab test by ID
# Operation: UPDATE
# Description: Updates a lab test and archives the previous state in the history table.
def update_lab_test(
    lab_test_id: int,
    lab_test_in: LabTestUpdate,
    db: Session = Depends(get_db),
):
    db_lab_test = db.query(LabTest).filter(LabTest.id == lab_test_id).first()
    if not db_lab_test:
        raise HTTPException(status_code=404, detail="Lab test not found")

    # Archive current state
    history = LabTestHistory(
        lab_test_id=db_lab_test.id,
        composition_id=db_lab_test.composition_id,
        specimen_id=db_lab_test.specimen_id,
        loinc_code=db_lab_test.loinc_code,
        version=db_lab_test.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in lab_test_in.dict(exclude_unset=True).items():
        setattr(db_lab_test, field, value)
    setattr(db_lab_test, "version", db_lab_test.version + 1)

    db.commit()
    db.refresh(db_lab_test)
    return db_lab_test


@router.delete("/{lab_test_id}")
# Delete a specific lab test by ID
# Operation: DELETE
# Description: Deletes a lab test and its associated history records.
def delete_lab_test(lab_test_id: int, db: Session = Depends(get_db)):
    db_lab_test = db.query(LabTest).filter(LabTest.id == lab_test_id).first()
    if not db_lab_test:
        raise HTTPException(status_code=404, detail="Lab test not found")

    # Delete from history table
    db.query(LabTestHistory).filter(LabTestHistory.lab_test_id == lab_test_id).delete()

    db.delete(db_lab_test)
    db.commit()
    return {"ok": True}
