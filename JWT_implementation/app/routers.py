from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel, Field, select

from app.db import get_session
from app.models import User
from app.utils import hash_password, check_password, create_access_token
from app.dependencies import get_current_user

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

# Login API (Public API)

class UserLogin(SQLModel):
    username: str
    password: str
    
@router.post("/login")
def user_login(data: UserLogin, session: Session = Depends(get_session)):
    username = data.username.strip().lower() # sanitization or normalization
    
    user = session.exec(
        select(User).where(User.username == username)
        ).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Bad Request, Incorrect username")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Permission Denied. Your account is deactivated. Contact Admin.")
    
    # check password
    if not check_password(plain_password=data.password, hashed_password= user.password):
        raise HTTPException(status_code=401, detail="Bad Request: Incorrect password")
    
    # Logged in successfully
    # Return access token (jwt token)
    token = create_access_token(user.id)
    
    return {"access_token": token}


@router.get("/profile", status_code=200)
def user_profile(current_user: User = Depends(get_current_user)):
    return current_user.model_dump(exclude="password")