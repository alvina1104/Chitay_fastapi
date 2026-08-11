from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import Book
from myproject.database.db import SessionLocal
from myproject.database.schema import BookInputSchema, BookOutSchema


book_router = APIRouter(prefix="/book", tags=["BOOK CRUD"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@book_router.post('/', response_model=BookOutSchema)
async def create_book(book: BookInputSchema, db: Session = Depends(get_db)):
    book_db = Book(**book.dict())
    db.add(book_db)
    db.commit()
    db.refresh(book_db)
    return book_db

@book_router.get('/', response_model=List[BookOutSchema])
async def list_book(db: Session = Depends(get_db)):
    return db.query(Book).all()

@book_router.put('/{book_id}', response_model=dict)
async def update_book(book_id: int, book_data: BookInputSchema, db: Session = Depends(get_db)):
    book_db = db.query(Book).filter(Book.id == book_id).first()
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(book_db, key, value)
    db.commit()
    return {"message": "Updated successfully"}

@book_router.delete('/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_db = db.query(Book).filter(Book.id == book_id).first()
    db.delete(book_db); db.commit()
    return {"message": "Deleted"}