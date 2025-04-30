from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/blood_type_panels", tags=["blood_type_panels"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_blood_type_panel(
    blood_type_panel: schemas.BloodTypePanelCreate, db: Session = Depends(get_db)
):
    db_blood_type_panel = models.BloodTypePanel(**blood_type_panel.dict())
    db.add(db_blood_type_panel)
    db.commit()
    db.refresh(db_blood_type_panel)
    return db_blood_type_panel


@router.get("/")
def list_blood_type_panels(db: Session = Depends(get_db)):
    return db.query(models.BloodTypePanel).all()


@router.get("/{blood_type_panel_id}")
def get_blood_type_panel(blood_type_panel_id: int, db: Session = Depends(get_db)):
    blood_type_panel = (
        db.query(models.BloodTypePanel)
        .filter(models.BloodTypePanel.id == blood_type_panel_id)
        .first()
    )
    if not blood_type_panel:
        raise HTTPException(status_code=404, detail="Blood type panel not found")
    return blood_type_panel
