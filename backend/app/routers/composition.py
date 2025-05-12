from datetime import datetime

from app import database
from app.models import Composition, CompositionHistory
from app.schemas import Composition as CompositionSchema
from app.schemas import CompositionCreate, CompositionUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/compositions", tags=["compositions"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CompositionSchema)
# Create a new composition
# Operation: CREATE
# Description: Adds a new composition to the database with versioning.
def create_composition(composition: CompositionCreate, db: Session = Depends(get_db)):
    db_composition = Composition(**composition.dict(), version=1)
    db.add(db_composition)
    db.commit()
    db.refresh(db_composition)
    return db_composition


@router.get("/", response_model=list[CompositionSchema])
# List all compositions
# Operation: READ (LIST)
# Description: Retrieves all compositions from the database.
def list_compositions(db: Session = Depends(get_db)):
    return db.query(Composition).all()


@router.get("/{composition_id}", response_model=CompositionSchema)
# Get a specific composition by ID
# Operation: READ (GET)
# Description: Retrieves a single composition by its ID.
def get_composition(composition_id: int, db: Session = Depends(get_db)):
    composition = db.query(Composition).filter(Composition.id == composition_id).first()
    if not composition:
        raise HTTPException(status_code=404, detail="Composition not found")
    return composition


@router.put("/{composition_id}", response_model=CompositionSchema)
# Update a specific composition by ID
# Operation: UPDATE
# Description: Updates a composition and archives the previous state in the history table.
def update_composition(
    composition_id: int,
    composition_in: CompositionUpdate,
    db: Session = Depends(get_db),
):
    db_composition = db.query(Composition).filter(Composition.id == composition_id).first()
    if not db_composition:
        raise HTTPException(status_code=404, detail="Composition not found")

    # Archive current state
    history = CompositionHistory(
        composition_id=db_composition.id,
        patient_id=db_composition.patient_id,
        start_time=db_composition.start_time,
        version=db_composition.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in composition_in.dict(exclude_unset=True).items():
        setattr(db_composition, field, value)
    setattr(db_composition, "version", db_composition.version + 1)

    db.commit()
    db.refresh(db_composition)
    return db_composition


@router.delete("/{composition_id}")
# Delete a specific composition by ID
# Operation: DELETE
# Description: Deletes a composition and its associated history records.
def delete_composition(composition_id: int, db: Session = Depends(get_db)):
    db_composition = db.query(Composition).filter(Composition.id == composition_id).first()
    if not db_composition:
        raise HTTPException(status_code=404, detail="Composition not found")

    # Delete from history table
    db.query(CompositionHistory).filter(
        CompositionHistory.composition_id == composition_id
    ).delete()

    db.delete(db_composition)
    db.commit()
    return {"ok": True}
