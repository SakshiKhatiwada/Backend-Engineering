from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel, Field, select

from app.db import get_session
from app.models import User
from app.utils import hash_password

router = APIRouter()

class UserRegister(SQLModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=3, max_length=20) # password validations here

@router.post("/user-register", status_code=201)
def register_user(data: UserRegister, session: Session = Depends(get_session)):
    username = data.username.strip().lower()
    password = data.password.strip().lower()
    
    existing = session.exec(
        select(User).where(User.username == username)
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="username already exists")
    
    # creating user
    user = User(
        username = username,
        password = hash_password(password)
    )
    
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Something went wrong"
        )
    return {"message":"user created successfully"}