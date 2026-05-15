from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import SubCatalog
from myproject.database.schema import SubCatalogOutSchema,SubCatalogInputSchema
from myproject.database.db import SessionLocal


subcatalog_router = APIRouter(prefix='/subcatalog', tags=['SUBCATALOG'])

async def grt_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@subcatalog_router.post('/', response_model=SubCatalogOutSchema)
async def create_subcatalog(subcatalog: SubCatalogInputSchema, db: Session = Depends(grt_db)):
    subcatalog_db = SubCatalog(**subcatalog.dict())
    db.add(subcatalog_db)
    db.commit()
    db.refresh(subcatalog_db)
    return subcatalog_db


@subcatalog_router.get('/', response_model=List[SubCatalogOutSchema])
async def list_subcatalog(db: Session = Depends(grt_db)):
    return db.query(SubCatalog).all()


@subcatalog_router.get('/{subcatalog_id}', response_model=SubCatalogOutSchema)
async def detail_subcatalog(subcatalog_id: int, db: Session = Depends(grt_db)):
    subcatalog_db = db.query(SubCatalog).filter(SubCatalog.id == subcatalog_id).first()
    if not subcatalog_db:
        raise HTTPException(status_code=404, detail="Subcatalog not found")
    return subcatalog_db


@subcatalog_router.put('/{subcatalog_id', response_model=dict)
async def update_subcatalog(subcatalog_id: int,subcatalog_: SubCatalogInputSchema,
                            db: Session = Depends(grt_db)):
    subcatalog_db = db.query(SubCatalog).filter(SubCatalog.id == subcatalog_id).first()
    if not subcatalog_db:
        raise HTTPException(status_code=404, detail="Subcatalog not found")

    for subcatalog_key, subcatalog_value in subcatalog_.dict().items():
        setattr(subcatalog_db, subcatalog_key, subcatalog_value)

    db.commit()
    db.refresh(subcatalog_db)
    return {"message": "Subcatalog updated successfully"}


@subcatalog_router.delete('/{subcatalog_id}', response_model=dict)
async def delete_subcatalog(subcatalog_id: int, db: Session = Depends(grt_db)):
    subcatalog_db = db.query(SubCatalog).filter(SubCatalog.id == subcatalog_id).first()
    if not subcatalog_db:
        raise HTTPException(status_code=404, detail="Subcatalog not found")
    db.delete(subcatalog_db)
    db.commit()
    return {"message": "Subcatalog deleted successfully"}
