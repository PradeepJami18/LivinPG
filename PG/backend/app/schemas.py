from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str
    role: str = "resident"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class ComplaintCreate(BaseModel):
    category: str
    description: str

class ComplaintResponse(BaseModel):
    id: int
    category: str
    description: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
class FoodMenuCreate(BaseModel):
    day: str
    breakfast: str
    lunch: str
    dinner: str

class PaymentCreate(BaseModel):
    amount: int
    transaction_id: str

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    amount: int
    transaction_id: str
    status: str
    created_at: datetime
    
    class Config:
        orm_mode = True
