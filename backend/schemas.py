from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        orm_mode = True

class SavingsAccountCreate(BaseModel):
    full_name: str
    dob: str
    address: str

class CurrentAccountCreate(BaseModel):
    full_name: str
    dob: str
    address: str

from pydantic import BaseModel

class LoanCreate(BaseModel):
    user_id: int
    loan_type: str
    amount: float
    tenure_months: int
    interest_rate: float