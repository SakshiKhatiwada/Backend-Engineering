from pydantic import BaseModel, EmailStr

class CustomerData(BaseModel):
    fullName: str
    email: EmailStr
    phone: str | None = None
    
class CustomerUpdate(BaseModel): # update maa optional hunxan, so we create separately
    fullName: str | None = None
    email: EmailStr | None = None
    phone: str | None = None