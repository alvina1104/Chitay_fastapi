from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import BookImage
from myproject.database.db import SessionLocal
from myproject.database.schema import BookImageOutSchema,BookImageInputSchema

book_image_router = APIRouter(prefix="/book_image", tags=["BOOK IMAGE"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@book_image_router.post('/', response_model=BookImageOutSchema)
async def create_image(book_image: BookImageInputSchema, db: Session = Depends(get_db)):
    book_image_db = BookImage(**book_image.dict())
    db.add(book_image_db)
    db.commit()
    db.refresh(book_image_db)
    return book_image_db


@book_image_router.get('/', response_model=List[BookImageOutSchema])
async def list_image(db: Session = Depends(get_db)):
    return db.query(BookImage).all()


@book_image_router.get('/{subcatalog_id}', response_model=BookImageOutSchema)
async def detail_image(subcatalog_id: int, db: Session = Depends(get_db)):
    book_image_db = db.query(BookImage).filter(BookImage.subcatalog_id == subcatalog_id).all()
    if not book_image_db:
        raise HTTPException(status_code=404, detail="Not Found")
    return book_image_db


@book_image_router.put('/{subcatalog_id}', response_model=dict)
async def update_image(book_image_id: int, book_image_: BookImageInputSchema,
                       db: Session = Depends(get_db)):
    book_image_db = db.query(BookImage).filter(BookImage.id == book_image_id).first()
    if not book_image_db:
        raise HTTPException(status_code=404, detail="Not Found")
    for key, value in book_image_.dict().items():
        setattr(book_image_db, key, value)

    db.commit()
    db.refresh(book_image_db)
    return {"message": "success"}


@book_image_router.delete('/{subcatalog_id}', response_model=dict)
async  def delete_image(book_image_id: int, db: Session = Depends(get_db)):
    book_image_db = db.query(BookImage).filter(BookImage.id == book_image_id).first()
    if not book_image_db:
        raise HTTPException(status_code=404, detail="Not Found")
    db.delete(book_image_db)
    db.commit()
    return {"message": "success deleted"}
