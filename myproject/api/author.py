from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import Author
from myproject.database.db import SessionLocal
from myproject.database.schema import AuthorOutSchema, AuthorInputSchema

author_router = APIRouter(prefix="/author", tags=["AUTHOR CRUD"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@author_router.post('/', response_model=AuthorOutSchema)
async def create_author(author: AuthorInputSchema, db: Session = Depends(get_db)):
    author_db = Author(**author.dict())
    db.add(author_db)
    db.commit()
    db.refresh(author_db)
    return author_db

@author_router.get('/', response_model=List[AuthorOutSchema])
async def list_author(db: Session = Depends(get_db)):
    return db.query(Author).all()

@author_router.get('/{author_id}', response_model=AuthorOutSchema)
async def detail_author(author_id: int, db: Session = Depends(get_db)):
    author_db = db.query(Author).filter(Author.id == author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")
    return author_db

@author_router.put('/{author_id}', response_model=dict)
async def update_author(author_id: int, author_: AuthorInputSchema,
                        db: Session = Depends(get_db)):
    author_db = db.query(Author).filter(Author.id == author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")


    for author_key, author_value in author_.dict(exclude_unset=True).items():
        setattr(author_db, author_key, author_value)

    db.commit()
    db.refresh(author_db)
    return {"message": "Updated author successfully"}

@author_router.delete('/{author_id}', response_model=dict)
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    author_db = db.query(Author).filter(Author.id == author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author_db)
    db.commit()
    return {"message": "Deleted author successfully"}
