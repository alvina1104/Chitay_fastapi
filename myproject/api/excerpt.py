from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from myproject.database.db import SessionLocal
from myproject.database.models import Excerpt
from myproject.database.schema import ExcerptInputSchema, ExcerptOutSchema

excerpt_router = APIRouter(prefix="/excerpt", tags=["EXCERPT"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@excerpt_router.post("/", response_model=ExcerptOutSchema)
async def create_excerpt(excerpt: ExcerptInputSchema, db: Session = Depends(get_db)):
    excerpt_db = Excerpt(**excerpt.dict())
    db.add(excerpt_db)
    db.commit()
    db.refresh(excerpt_db)
    return excerpt_db


@excerpt_router.get("/", response_model=List[ExcerptOutSchema])
async def list_excerpt(db: Session = Depends(get_db)):
    return db.query(Excerpt).all()


@excerpt_router.get("/{excerpt_id}", response_model=ExcerptOutSchema)
async def detail_excerpt(excerpt_id: int, db: Session = Depends(get_db)):
    excerpt_db = db.query(Excerpt).filter(Excerpt.id == excerpt_id).first()

    if not excerpt_db:
        raise HTTPException(status_code=404, detail="Excerpt not found")

    return excerpt_db


@excerpt_router.put("/{excerpt_id}", response_model=dict)
async def update_excerpt(excerpt_id: int, excerpt: ExcerptInputSchema, db: Session = Depends(get_db)):
    excerpt_db = db.query(Excerpt).filter(Excerpt.id == excerpt_id).first()

    if not excerpt_db:
        raise HTTPException(status_code=404, detail="Excerpt not found")

    for key, value in excerpt.dict().items():
        setattr(excerpt_db, key, value)

    db.commit()
    db.refresh(excerpt_db)

    return {"message": "Excerpt updated successfully"}


@excerpt_router.delete("/{excerpt_id}", response_model=dict)
async def delete_excerpt(excerpt_id: int, db: Session = Depends(get_db)):
    excerpt_db = db.query(Excerpt).filter(Excerpt.id == excerpt_id).first()

    if not excerpt_db:
        raise HTTPException(status_code=404, detail="Excerpt not found")

    db.delete(excerpt_db)
    db.commit()

    return {"message": "Excerpt deleted successfully"}