from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from myproject.database.db import SessionLocal
from myproject.database.models import CartItem
from myproject.database.schema import CartItemInputSchema, CartItemOutSchema

cart_item_router = APIRouter(prefix="/cart-item", tags=["CART ITEM"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cart_item_router.post("/", response_model=CartItemOutSchema)
async def create_cart_item(cart_item: CartItemInputSchema, db: Session = Depends(get_db)):
    cart_item_db = CartItem(**cart_item.dict())
    db.add(cart_item_db)
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db


@cart_item_router.get("/", response_model=List[CartItemOutSchema])
async def list_cart_item(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


@cart_item_router.get("/{cart_item_id}", response_model=CartItemOutSchema)
async def detail_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return cart_item_db


@cart_item_router.put("/{cart_item_id}", response_model=dict)
async def update_cart_item(cart_item_id: int, cart_item: CartItemInputSchema, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Cart item not found")

    for key, value in cart_item.dict().items():
        setattr(cart_item_db, key, value)

    db.commit()
    db.refresh(cart_item_db)

    return {"message": "Cart item updated successfully"}


@cart_item_router.delete("/{cart_item_id}", response_model=dict)
async def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item_db)
    db.commit()

    return {"message": "Cart item deleted successfully"}