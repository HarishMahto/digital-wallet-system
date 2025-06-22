from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
from models import Transaction

router = APIRouter()

@router.get("/stmt")
def get_statement(user = Depends(get_current_user), db: Session = Depends(get_db)):
    txns = db.query(Transaction).filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()
    return [
        {
            "kind": t.kind,
            "amt": t.amt,
            "updated_bal": t.updated_bal,
            "timestamp": t.timestamp.isoformat()
        }
        for t in txns
    ]