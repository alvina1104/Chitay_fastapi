from myproject.database.models import Catalog
from myproject.database.schema import CatalogOutSchema, CatalogInputSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException, APIRouter


catalog_router = APIRouter(prefix="/catalog", tags=["CATALOG"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@catalog_router.post('/', response_model=CatalogOutSchema)
async def create_catalog(catalog: CatalogInputSchema, db: Session = Depends(get_db)):
    catalog_db = Catalog(**catalog.dict())
    db.add(catalog_db)
    db.commit()
    db.refresh(catalog_db)
    return catalog_db


@catalog_router.get('/', response_model=List[CatalogOutSchema])
async def list_catalog(db: Session = Depends(get_db)):
    return db.query(Catalog).all()


@catalog_router.get('/{catalog_id}', response_model=CatalogOutSchema)
async def detail_catalog(catalog_id: int, db: Session = Depends(get_db)):
    catalog_db = db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if not catalog_db:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return catalog_db


@catalog_router.put('/{catalog_id}', response_model=dict)
async  def update_catalog(catalog_id: int, catalog_: CatalogInputSchema, db: Session = Depends(get_db)):
    catalog_db = db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if not catalog_db:
        raise HTTPException(status_code=404, detail="Catalog not found")

    for catalog_key, catalog_value in catalog_.dict().items():
        setattr(catalog_db, catalog_key, catalog_value)

    db.commit()
    db.refresh(catalog_db)
    return {"message": "Catalog updated successfully"}


@catalog_router.delete('/{catalog_id}', response_model=dict)
async def delete_catalog(catalog_id: int, db: Session = Depends(get_db)):
    catalog_db = db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if not catalog_db:
        raise HTTPException(status_code=404, detail="Catalog not found")
    db.delete(catalog_db)
    db.commit()
    return {"message": "Catalog deleted successfully"}


