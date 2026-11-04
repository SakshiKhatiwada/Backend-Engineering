from pwdlib import PasswordHash
# from app.models import User
from datetime import datetime, timezone, timedelta
import jwt

SIGNATURE_KEY = "XYZ123" #TODO - Load from .env
TOKEN_EXPIRY_TIME = 10

password_hash = PasswordHash.recommended()

def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)
    
    
def check_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(user_id: int)-> str:
    now = datetime.now(timezone.utc)
    
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_EXPIRY_TIME)
        }
    
    token = jwt.encode(
        payload,
        SIGNATURE_KEY,
        algorithm="HS256"
    )
    
    return token