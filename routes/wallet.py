from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
from models import User, Transaction
from pydantic import BaseModel
from currency import convert_currency

router = APIRouter()

class FundRequest(BaseModel):
    amt: float

@router.post("/fund")
def fund_wallet(req: FundRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.amt <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    user.balance += req.amt
    db.add(Transaction(user_id=user.id, kind="credit", amt=req.amt, updated_bal=user.balance))
    db.commit()
    return {"balance": user.balance}

class PayRequest(BaseModel):
    to: str
    amt: float

@router.post("/pay")
def pay_user(req: PayRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.amt <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")
    recipient = db.query(User).filter_by(username=req.to).first()
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient not found")
    if user.balance < req.amt:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    user.balance -= req.amt
    recipient.balance += req.amt
    db.add_all([
        Transaction(user_id=user.id, kind="debit", amt=req.amt, updated_bal=user.balance),
        Transaction(user_id=recipient.id, kind="credit", amt=req.amt, updated_bal=recipient.balance)
    ])
    db.commit()
    return {"balance": user.balance}

@router.get("/bal")
def get_balance(currency: str = "INR", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bal = user.balance
    if currency != "INR":
        converted, rate = convert_currency(bal, "INR", currency)
        return {"balance": converted, "currency": currency, "rate": rate}
    return {"balance": bal, "currency": "INR"}