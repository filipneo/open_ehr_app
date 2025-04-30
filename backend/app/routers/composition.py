from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/compositions", tags=["compositions"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_composition(composition: schemas.CompositionCreate, db: Session = Depends(get_db)):
    db_composition = models.Composition(**composition.dict())
    db.add(db_composition)
    db.commit()
    db.refresh(db_composition)
    return db_composition


@router.get("/")
def list_compositions(db: Session = Depends(get_db)):
    return db.query(models.Composition).all()


@router.get("/{composition_id}")
def get_composition(composition_id: int, db: Session = Depends(get_db)):
    composition = (
        db.query(models.Composition).filter(models.Composition.id == composition_id).first()
    )
    if not composition:
        raise HTTPException(status_code=404, detail="Composition not found")
    return composition


@router.delete("/{composition_id}")
def delete_composition(composition_id: int, db: Session = Depends(get_db)):
    composition = (
        db.query(models.Composition).filter(models.Composition.id == composition_id).first()
    )
    if not composition:
        raise HTTPException(status_code=404, detail="Composition not found")
    db.delete(composition)
    db.commit()
    return {"message": "Composition deleted successfully"}
