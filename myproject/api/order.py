from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from myproject.database.db import SessionLocal
from myproject.database.models import Order
from myproject.database.schema import OrderInputSchema, OrderOutSchema

order_router = APIRouter(prefix="/order", tags=["ORDER"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_router.post("/", response_model=OrderOutSchema)
async def create_order(order: OrderInputSchema, db: Session = Depends(get_db)):
    order_db = Order(**order.dict())
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.get("/", response_model=List[OrderOutSchema])
async def list_order(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get("/{order_id}", response_model=OrderOutSchema)
async def detail_order(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()

    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")

    return order_db


@order_router.put("/{order_id}", response_model=dict)
async def update_order(order_id: int, order: OrderInputSchema, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()

    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order.dict().items():
        setattr(order_db, key, value)

    db.commit()
    db.refresh(order_db)

    return {"message": "Order updated successfully"}


@order_router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()

    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order_db)
    db.commit()

    return {"message": "Order deleted successfully"}