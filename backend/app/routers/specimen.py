from datetime import datetime

from app import database
from app.models import Specimen, SpecimenHistory
from app.schemas import Specimen as SpecimenSchema
from app.schemas import SpecimenCreate, SpecimenUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/specimens", tags=["specimens"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SpecimenSchema)
# Create a new specimen
# Operation: CREATE
# Description: Adds a new specimen to the database with versioning.
def create_specimen(specimen: SpecimenCreate, db: Session = Depends(get_db)):
    db_specimen = Specimen(**specimen.dict(), version=1)
    db.add(db_specimen)
    db.commit()
    db.refresh(db_specimen)
    return db_specimen


@router.get("/", response_model=list[SpecimenSchema])
# List all specimens
# Operation: READ (LIST)
# Description: Retrieves all specimens from the database.
def list_specimens(db: Session = Depends(get_db)):
    return db.query(Specimen).all()


@router.get("/{specimen_id}", response_model=SpecimenSchema)
# Get a specific specimen by ID
# Operation: READ (GET)
# Description: Retrieves a single specimen by its ID.
def get_specimen(specimen_id: int, db: Session = Depends(get_db)):
    specimen = db.query(Specimen).filter(Specimen.id == specimen_id).first()
    if not specimen:
        raise HTTPException(status_code=404, detail="Specimen not found")
    return specimen


@router.put("/{specimen_id}", response_model=SpecimenSchema)
# Update a specific specimen by ID
# Operation: UPDATE
# Description: Updates a specimen and archives the previous state in the history table.
def update_specimen(
    specimen_id: int,
    specimen_in: SpecimenUpdate,
    db: Session = Depends(get_db),
):
    db_specimen = db.query(Specimen).filter(Specimen.id == specimen_id).first()
    if not db_specimen:
        raise HTTPException(status_code=404, detail="Specimen not found")

    # Archive current state
    history = SpecimenHistory(
        specimen_id=db_specimen.id,
        specimen_type=db_specimen.specimen_type,
        collection_time=db_specimen.collection_time,
        snomed_code=db_specimen.snomed_code,
        description=db_specimen.description,
        version=db_specimen.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in specimen_in.dict(exclude_unset=True).items():
        setattr(db_specimen, field, value)
    setattr(db_specimen, "version", db_specimen.version + 1)

    db.commit()
    db.refresh(db_specimen)
    return db_specimen


@router.delete("/{specimen_id}")
# Delete a specific specimen by ID
# Operation: DELETE
# Description: Deletes a specimen and its associated history records.
def delete_specimen(specimen_id: int, db: Session = Depends(get_db)):
    db_specimen = db.query(Specimen).filter(Specimen.id == specimen_id).first()
    if not db_specimen:
        raise HTTPException(status_code=404, detail="Specimen not found")

    # Delete from history table
    db.query(SpecimenHistory).filter(SpecimenHistory.specimen_id == specimen_id).delete()

    db.delete(db_specimen)
    db.commit()
    return {"ok": True}
