from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import TypeCatalog
from myproject.database.db import SessionLocal
from myproject.database.schema import TypeCatalogOutSchema, TypeCatalogInputSchema


type_catalog_router = APIRouter(prefix="/type_catalog", tags=["TYPE CATALOG"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@type_catalog_router.post('/',response_model=TypeCatalogOutSchema)
async def create_type_catalog(type_catalog: TypeCatalogInputSchema, db: Session = Depends(get_db)):
    type_catalog_db = TypeCatalog(**type_catalog.dict())
    db.add(type_catalog_db)
    db.commit()
    db.refresh(type_catalog_db)
    return type_catalog_db


@type_catalog_router.get('/', response_model=List[TypeCatalogOutSchema])
async def list_type_catalog(db: Session = Depends(get_db)):
    return db.query(TypeCatalog).all()


@type_catalog_router.get('/{type_catalog_id}', response_model=TypeCatalogOutSchema)
async def detail_hotel(type_catalog_id: int, db: Session = Depends(get_db)):
    type_catalog_db = db.query(TypeCatalog).filter(TypeCatalog.id == type_catalog_id).first()
    if not type_catalog_db:
        raise HTTPException(status_code=404, detail="TypeCatalog not found")
    return type_catalog_db


@type_catalog_router.put('/{type_catalog_id}', response_model=dict)
async def update_type_catalog(type_catalog_id: int, type_catalog_: TypeCatalogInputSchema,
                              db: Session = Depends(get_db)):
    type_catalog_db = db.query(TypeCatalog).filter(TypeCatalog.id == type_catalog_id).first()
    if not type_catalog_db:
        raise HTTPException(status_code=404, detail="TypeCatalog not found")

    for key, value in type_catalog_.dict().items():
        setattr(type_catalog_db, key, value)

    db.commit()
    db.refresh(type_catalog_db)
    return {"message": "Updated type_catalog successfully"}


@type_catalog_router.delete('/{type_catalog_id}', response_model=dict)
async def delete_type_catalog(type_catalog_id: int, db: Session = Depends(get_db)):
    type_catalog_db = db.query(TypeCatalog).filter(TypeCatalog.id == type_catalog_id).first()
    if not type_catalog_db:
        raise HTTPException(status_code=404, detail="TypeCatalog not found")

    db.delete(type_catalog_db)
    db.commit()
    return {"message": "Deleted type_catalog successfully"}



