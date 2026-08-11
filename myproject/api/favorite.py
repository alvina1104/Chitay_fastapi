from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from myproject.database.db import SessionLocal
from myproject.database.models import FavoriteItem
from myproject.database.schema import FavoriteItemInputSchema, FavoriteItemOutSchema

favorite_router = APIRouter(prefix="/favorite-item", tags=["FAVORITE ITEM"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@favorite_router.post("/", response_model=FavoriteItemOutSchema)
async def create_favorite_item(favorite: FavoriteItemInputSchema, db: Session = Depends(get_db)):
    favorite_db = FavoriteItem(**favorite.dict())
    db.add(favorite_db)
    db.commit()
    db.refresh(favorite_db)
    return favorite_db


@favorite_router.get("/", response_model=List[FavoriteItemOutSchema])
async def list_favorite_item(db: Session = Depends(get_db)):
    return db.query(FavoriteItem).all()


@favorite_router.get("/{favorite_id}", response_model=FavoriteItemOutSchema)
async def detail_favorite_item(favorite_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(FavoriteItem).filter(FavoriteItem.id == favorite_id).first()

    if not favorite_db:
        raise HTTPException(status_code=404, detail="Favorite item not found")

    return favorite_db


@favorite_router.put("/{favorite_id}", response_model=dict)
async def update_favorite_item(favorite_id: int, favorite: FavoriteItemInputSchema, db: Session = Depends(get_db)):
    favorite_db = db.query(FavoriteItem).filter(FavoriteItem.id == favorite_id).first()

    if not favorite_db:
        raise HTTPException(status_code=404, detail="Favorite item not found")

    for key, value in favorite.dict().items():
        setattr(favorite_db, key, value)

    db.commit()
    db.refresh(favorite_db)

    return {"message": "Favorite item updated successfully"}


@favorite_router.delete("/{favorite_id}", response_model=dict)
async def delete_favorite_item(favorite_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(FavoriteItem).filter(FavoriteItem.id == favorite_id).first()

    if not favorite_db:
        raise HTTPException(status_code=404, detail="Favorite item not found")

    db.delete(favorite_db)
    db.commit()

    return {"message": "Favorite item deleted successfully"}