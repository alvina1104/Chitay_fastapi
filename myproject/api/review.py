from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from myproject.database.db import SessionLocal
from myproject.database.models import Review
from myproject.database.schema import ReviewInputSchema, ReviewOutSchema

review_router = APIRouter(prefix="/review", tags=["REVIEW"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post("/", response_model=ReviewOutSchema)
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.get("/", response_model=List[ReviewOutSchema])
async def list_review(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get("/{review_id}", response_model=ReviewOutSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()

    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")

    return review_db


@review_router.put("/{review_id}", response_model=dict)
async def update_review(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()

    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")

    for key, value in review.dict().items():
        setattr(review_db, key, value)

    db.commit()
    db.refresh(review_db)

    return {"message": "Review updated successfully"}


@review_router.delete("/{review_id}", response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()

    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review_db)
    db.commit()

    return {"message": "Review deleted successfully"}