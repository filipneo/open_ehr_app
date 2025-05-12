from datetime import datetime

from app import database
from app.models import BloodTypePanel, BloodTypePanelHistory
from app.schemas import BloodTypePanel as BloodTypePanelSchema
from app.schemas import BloodTypePanelCreate, BloodTypePanelUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/blood_type_panel", tags=["blood_type_panel"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=BloodTypePanelSchema)
# Create a new blood type panel
# Operation: CREATE
# Description: Adds a new blood type panel to the database with versioning.
def create_blood_type_panel(blood_type_panel: BloodTypePanelCreate, db: Session = Depends(get_db)):
    db_blood_type_panel = BloodTypePanel(**blood_type_panel.dict(), version=1)
    db.add(db_blood_type_panel)
    db.commit()
    db.refresh(db_blood_type_panel)
    return db_blood_type_panel


@router.get("/all", response_model=list[BloodTypePanelSchema])
# List all blood type panels
# Operation: READ (LIST)
# Description: Retrieves all blood type panels from the database.
def list_blood_type_panels(db: Session = Depends(get_db)):
    return db.query(BloodTypePanel).all()


@router.get("/{blood_type_panel_id}", response_model=BloodTypePanelSchema)
# Get a specific blood type panel by ID
# Operation: READ (GET)
# Description: Retrieves a single blood type panel by its ID.
def get_blood_type_panel(blood_type_panel_id: int, db: Session = Depends(get_db)):
    blood_type_panel = (
        db.query(BloodTypePanel).filter(BloodTypePanel.id == blood_type_panel_id).first()
    )
    if not blood_type_panel:
        raise HTTPException(status_code=404, detail="Blood type panel not found")
    return blood_type_panel


@router.put("/{blood_type_panel_id}", response_model=BloodTypePanelSchema)
# Update a specific blood type panel by ID
# Operation: UPDATE
# Description: Updates a blood type panel and archives the previous state in the history table.
def update_blood_type_panel(
    blood_type_panel_id: int,
    blood_type_panel_in: BloodTypePanelUpdate,
    db: Session = Depends(get_db),
):
    db_blood_type_panel = (
        db.query(BloodTypePanel).filter(BloodTypePanel.id == blood_type_panel_id).first()
    )
    if not db_blood_type_panel:
        raise HTTPException(status_code=404, detail="Blood type panel not found")

    # Archive current state
    history = BloodTypePanelHistory(
        blood_type_panel_id=db_blood_type_panel.id,
        lab_test_id=db_blood_type_panel.lab_test_id,
        abo_id=db_blood_type_panel.abo_id,
        rh_id=db_blood_type_panel.rh_id,
        version=db_blood_type_panel.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in blood_type_panel_in.dict(exclude_unset=True).items():
        setattr(db_blood_type_panel, field, value)
    setattr(db_blood_type_panel, "version", db_blood_type_panel.version + 1)

    db.commit()
    db.refresh(db_blood_type_panel)
    return db_blood_type_panel


@router.delete("/{blood_type_panel_id}")
# Delete a specific blood type panel by ID
# Operation: DELETE
# Description: Deletes a blood type panel and its associated history records.
def delete_blood_type_panel(blood_type_panel_id: int, db: Session = Depends(get_db)):
    blood_type_panel = (
        db.query(BloodTypePanel).filter(BloodTypePanel.id == blood_type_panel_id).first()
    )
    if not blood_type_panel:
        raise HTTPException(status_code=404, detail="Blood type panel not found")

    # Delete from history table
    db.query(BloodTypePanelHistory).filter(
        BloodTypePanelHistory.blood_type_panel_id == blood_type_panel_id
    ).delete()

    db.delete(blood_type_panel)
    db.commit()
    return {"ok": True}
