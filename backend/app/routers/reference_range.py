from datetime import datetime

from app import database
from app.models import ReferenceRange, ReferenceRangeHistory
from app.schemas import ReferenceRange as ReferenceRangeSchema
from app.schemas import ReferenceRangeCreate, ReferenceRangeUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reference_ranges", tags=["reference_ranges"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReferenceRangeSchema)
# Create a new reference range
# Operation: CREATE
# Description: Adds a new reference range to the database with versioning.
def create_reference_range(reference_range: ReferenceRangeCreate, db: Session = Depends(get_db)):
    db_reference_range = ReferenceRange(**reference_range.dict(), version=1)
    db.add(db_reference_range)
    db.commit()
    db.refresh(db_reference_range)
    return db_reference_range


@router.get("/", response_model=list[ReferenceRangeSchema])
# List all reference ranges
# Operation: READ (LIST)
# Description: Retrieves all reference ranges from the database.
def list_reference_ranges(db: Session = Depends(get_db)):
    return db.query(ReferenceRange).all()


@router.get("/{loinc_code}", response_model=ReferenceRangeSchema)
# Get a specific reference range by LOINC code
# Operation: READ (GET)
# Description: Retrieves a single reference range by its LOINC code.
def get_reference_range(loinc_code: str, db: Session = Depends(get_db)):
    reference_range = (
        db.query(ReferenceRange).filter(ReferenceRange.loinc_code == loinc_code).first()
    )
    if not reference_range:
        raise HTTPException(status_code=404, detail="Reference range not found")
    return reference_range


@router.put("/{loinc_code}", response_model=ReferenceRangeSchema)
# Update a specific reference range by LOINC code
# Operation: UPDATE
# Description: Updates a reference range and archives the previous state in the history table.
def update_reference_range(
    loinc_code: str,
    reference_range_in: ReferenceRangeUpdate,
    db: Session = Depends(get_db),
):
    db_reference_range = (
        db.query(ReferenceRange).filter(ReferenceRange.loinc_code == loinc_code).first()
    )
    if not db_reference_range:
        raise HTTPException(status_code=404, detail="Reference range not found")

    # Archive current state
    history = ReferenceRangeHistory(
        reference_range_loinc_code=db_reference_range.loinc_code,
        low=db_reference_range.low,
        high=db_reference_range.high,
        unit=db_reference_range.unit,
        version=db_reference_range.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in reference_range_in.dict(exclude_unset=True).items():
        setattr(db_reference_range, field, value)
    setattr(db_reference_range, "version", db_reference_range.version + 1)

    db.commit()
    db.refresh(db_reference_range)
    return db_reference_range


@router.delete("/{loinc_code}")
# Delete a specific reference range by LOINC code
# Operation: DELETE
# Description: Deletes a reference range and its associated history records.
def delete_reference_range(loinc_code: str, db: Session = Depends(get_db)):
    reference_range = (
        db.query(ReferenceRange).filter(ReferenceRange.loinc_code == loinc_code).first()
    )
    if not reference_range:
        raise HTTPException(status_code=404, detail="Reference range not found")

    # Delete from history table
    db.query(ReferenceRangeHistory).filter(
        ReferenceRangeHistory.reference_range_loinc_code == loinc_code
    ).delete()

    db.delete(reference_range)
    db.commit()
    return {"ok": True}
