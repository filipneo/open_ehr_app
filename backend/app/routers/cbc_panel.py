from datetime import datetime

from app import database
from app.models import CBCPanel, CBCPanelHistory
from app.schemas import CBCPanel as CBCPanelSchema
from app.schemas import CBCPanelCreate, CBCPanelUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cbc_panels", tags=["cbc_panels"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CBCPanelSchema)
# Create a new CBC panel
# Operation: CREATE
# Description: Adds a new CBC panel to the database with versioning.
def create_cbc_panel(cbc_panel: CBCPanelCreate, db: Session = Depends(get_db)):
    db_cbc_panel = CBCPanel(**cbc_panel.dict(), version=1)
    db.add(db_cbc_panel)
    db.commit()
    db.refresh(db_cbc_panel)
    return db_cbc_panel


@router.get("/", response_model=list[CBCPanelSchema])
# List all CBC panels
# Operation: READ (LIST)
# Description: Retrieves all CBC panels from the database.
def list_cbc_panels(db: Session = Depends(get_db)):
    return db.query(CBCPanel).all()


@router.get("/{cbc_panel_id}", response_model=CBCPanelSchema)
# Get a specific CBC panel by ID
# Operation: READ (GET)
# Description: Retrieves a single CBC panel by its ID.
def get_cbc_panel(cbc_panel_id: int, db: Session = Depends(get_db)):
    cbc_panel = db.query(CBCPanel).filter(CBCPanel.id == cbc_panel_id).first()
    if not cbc_panel:
        raise HTTPException(status_code=404, detail="CBC panel not found")
    return cbc_panel


@router.put("/{cbc_panel_id}", response_model=CBCPanelSchema)
# Update a specific CBC panel by ID
# Operation: UPDATE
# Description: Updates a CBC panel and archives the previous state in the history table.
def update_cbc_panel(
    cbc_panel_id: int,
    cbc_panel_in: CBCPanelUpdate,
    db: Session = Depends(get_db),
):
    db_cbc_panel = db.query(CBCPanel).filter(CBCPanel.id == cbc_panel_id).first()
    if not db_cbc_panel:
        raise HTTPException(status_code=404, detail="CBC panel not found")

    # Archive current state
    history = CBCPanelHistory(
        cbc_panel_id=db_cbc_panel.id,
        lab_test_id=db_cbc_panel.lab_test_id,
        hemoglobin_id=db_cbc_panel.hemoglobin_id,
        white_cell_id=db_cbc_panel.white_cell_id,
        platelet_id=db_cbc_panel.platelet_id,
        version=db_cbc_panel.version,
        updated_at=datetime.utcnow(),
    )
    db.add(history)

    # Apply update
    for field, value in cbc_panel_in.dict(exclude_unset=True).items():
        setattr(db_cbc_panel, field, value)
    setattr(db_cbc_panel, "version", db_cbc_panel.version + 1)

    db.commit()
    db.refresh(db_cbc_panel)
    return db_cbc_panel


@router.delete("/{cbc_panel_id}")
# Delete a specific CBC panel by ID
# Operation: DELETE
# Description: Deletes a CBC panel and its associated history records.
def delete_cbc_panel(cbc_panel_id: int, db: Session = Depends(get_db)):
    db_cbc_panel = db.query(CBCPanel).filter(CBCPanel.id == cbc_panel_id).first()
    if not db_cbc_panel:
        raise HTTPException(status_code=404, detail="CBC panel not found")

    # Delete from history table
    db.query(CBCPanelHistory).filter(CBCPanelHistory.cbc_panel_id == cbc_panel_id).delete()

    db.delete(db_cbc_panel)
    db.commit()
    return {"ok": True}
