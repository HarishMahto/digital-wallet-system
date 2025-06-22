from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
from models import Product, User, Transaction
from pydantic import BaseModel

router = APIRouter()

class ProductRequest(BaseModel):
    name: str
    price: float
    description: str

@router.post("/product", status_code=201)
def add_product(req: ProductRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = Product(**req.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"id": product.id, "message": "Product added"}

@router.get("/product")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [{"id": p.id, "name": p.name, "price": p.price, "description": p.description} for p in products]

class BuyRequest(BaseModel):
    product_id: int

@router.post("/buy")
def buy_product(req: BuyRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=req.product_id).first()
    if not product or user.balance < product.price:
        raise HTTPException(status_code=400, detail="Insufficient balance or invalid product")
    user.balance -= product.price
    db.add(Transaction(user_id=user.id, kind="debit", amt=product.price, updated_bal=user.balance))
    db.commit()
    return {"message": "Product purchased", "balance": user.balance}