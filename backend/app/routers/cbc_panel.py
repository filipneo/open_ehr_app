from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cbc_panels", tags=["cbc_panels"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_cbc_panel(cbc_panel: schemas.CBCPanelCreate, db: Session = Depends(get_db)):
    db_cbc_panel = models.CBCPanel(**cbc_panel.dict())
    db.add(db_cbc_panel)
    db.commit()
    db.refresh(db_cbc_panel)
    return db_cbc_panel


@router.get("/")
def list_cbc_panels(db: Session = Depends(get_db)):
    return db.query(models.CBCPanel).all()


@router.get("/{cbc_panel_id}")
def get_cbc_panel(cbc_panel_id: int, db: Session = Depends(get_db)):
    cbc_panel = db.query(models.CBCPanel).filter(models.CBCPanel.id == cbc_panel_id).first()
    if not cbc_panel:
        raise HTTPException(status_code=404, detail="CBC panel not found")
    return cbc_panel
