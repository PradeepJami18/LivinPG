from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "role": db_user.role,
        "full_name": db_user.full_name
    }

@router.get("/residents", response_model=list[UserResponse])
def get_residents(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Validation
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    return db.query(User).filter(User.role == "resident").all()

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


from pydantic import BaseModel

class PasswordReset(BaseModel):
    email: str
    new_password: str

@router.put("/reset-password")
def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == data.email).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db_user.password = hash_password(data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}


