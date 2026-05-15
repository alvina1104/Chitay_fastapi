from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import Address
from myproject.database.db import SessionLocal
from myproject.database.schema import AddressOutSchema, AddressInputSchema

address_router = APIRouter(prefix="/address", tags=["ADDRESS CRUD"])

# DB dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@address_router.post('/', response_model=AddressOutSchema)
async def create_address(address: AddressInputSchema, db: Session = Depends(get_db)):
    address_db = Address(**address.dict())
    db.add(address_db)
    db.commit()
    db.refresh(address_db)
    return address_db

@address_router.get('/', response_model=List[AddressOutSchema])
async def list_address(db: Session = Depends(get_db)):
    return db.query(Address).all()

@address_router.get('/{address_id}', response_model=AddressOutSchema)
async def detail_address(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(status_code=404, detail="Address not found")
    return address_db

@address_router.put('/{address_id}', response_model=dict)
async def update_address(address_id: int, address_data: AddressInputSchema,
                         db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(status_code=404, detail="Address not found")

    # Схемадан маалыматтарды алып, моделди жаңылоо
    for key, value in address_data.dict(exclude_unset=True).items():
        setattr(address_db, key, value)

    db.commit()
    db.refresh(address_db)
    return {"message": "Updated address successfully"}

@address_router.delete('/{address_id}', response_model=dict)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(address_db)
    db.commit()
    return {"message": "Deleted address successfully"}