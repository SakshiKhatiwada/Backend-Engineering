from app.db import get_session
from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.utils import SIGNATURE_KEY
from app.models import User
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token,
            SIGNATURE_KEY,
            algorithms=["HS256"],
            options={"require": ["sub", "exp"]}
        )
        
        user_id = int(payload["sub"])
    except(InvalidTokenError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Bad Request: Invalid Header or expired tokan")
    
    user = session.get(User, user_id)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Bad Request, Account Disabled.")
    
    return user