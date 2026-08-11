from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from myproject.database.db import SessionLocal
from myproject.database.models import OrderItem
from myproject.database.schema import OrderItemInputSchema, OrderItemOutSchema

order_item_router = APIRouter(prefix="/order-item", tags=["ORDER ITEM"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_item_router.post("/", response_model=OrderItemOutSchema)
async def create_order_item(order_item: OrderItemInputSchema, db: Session = Depends(get_db)):
    order_item_db = OrderItem(**order_item.dict())
    db.add(order_item_db)
    db.commit()
    db.refresh(order_item_db)
    return order_item_db


@order_item_router.get("/", response_model=List[OrderItemOutSchema])
async def list_order_item(db: Session = Depends(get_db)):
    return db.query(OrderItem).all()


@order_item_router.get("/{order_item_id}", response_model=OrderItemOutSchema)
async def detail_order_item(order_item_id: int, db: Session = Depends(get_db)):
    order_item_db = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    if not order_item_db:
        raise HTTPException(status_code=404, detail="Order item not found")

    return order_item_db


@order_item_router.put("/{order_item_id}", response_model=dict)
async def update_order_item(order_item_id: int, order_item: OrderItemInputSchema, db: Session = Depends(get_db)):
    order_item_db = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    if not order_item_db:
        raise HTTPException(status_code=404, detail="Order item not found")

    for key, value in order_item.dict().items():
        setattr(order_item_db, key, value)

    db.commit()
    db.refresh(order_item_db)

    return {"message": "Order item updated successfully"}


@order_item_router.delete("/{order_item_id}", response_model=dict)
async def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    order_item_db = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    if not order_item_db:
        raise HTTPException(status_code=404, detail="Order item not found")

    db.delete(order_item_db)
    db.commit()

    return {"message": "Order item deleted successfully"}