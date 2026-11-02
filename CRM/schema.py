from pydantic import EmailStr
from sqlmodel import SQLModel, Field
class CustomerData(SQLModel):
    fullName: str
    email: EmailStr
    phone: str | None = None
    
class CustomerUpdate(SQLModel): # update maa optional hunxan, so we create separately
    fullName: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    
class Customers(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fullName: str = Field(index=True)
    email: EmailStr = Field(index=True)
    phone: str = Field(index=True) #index=True, search garna milxa esbata
    
class CustomerTableUpdate(SQLModel, table=True): # update maa optional hunxan, so we create separately
    id: int | None = Field(default=None, primary_key=True)
    fullName: str | None = Field(default=None, index=True)
    email: EmailStr | None = Field(default=None, index=True)
    phone: str | None = Field(default=None, index=True)