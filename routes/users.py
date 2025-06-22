from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
import bcrypt
from pydantic import BaseModel

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register", status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=req.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()
    user = User(username=req.username, password=hashed_pw)
    db.add(user)
    db.commit()
    return {"message": "User created"}