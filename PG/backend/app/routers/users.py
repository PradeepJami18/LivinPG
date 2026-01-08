from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Complaint, Payment, Notification
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
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
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
    except HTTPException:
        raise 
    except Exception as e:
        print(f"LOGIN CRASH: {e}")
        raise HTTPException(status_code=500, detail=f"Login Crash: {str(e)}")

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/residents", response_model=list[UserResponse])
def get_residents(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Validation
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    return db.query(User).filter(User.role == "resident").all()





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

@router.post("/leave")
def leave_pg(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "resident":
        raise HTTPException(status_code=403, detail="Only residents can leave PG")

    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.status = "Notice"
    db.commit()

    # Create Notification for Admins
    try:
        admins = db.query(User).filter(User.role == "admin").all()
        for admin in admins:
            new_notif = Notification(
                user_id=admin.id,
                title="Resident Leaving",
                message=f"Resident {user.full_name} has requested to leave (Notice Period).",
                type="alert"
            )
            db.add(new_notif)
        db.commit()
    except Exception as e:
        print(f"Notification Error: {e}")

    return {"message": "You have successfully marked yourself as leaving (Notice Period)."}


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
        
    try:
        # Manually delete dependent records first to be safe, 
        # although ondelete="CASCADE" in models should handle it.
        # Sometimes MySQL needs explicit deletion if foreign keys aren't set perfectly.
        db.query(Complaint).filter(Complaint.user_id == user_id).delete()
        db.query(Payment).filter(Payment.user_id == user_id).delete()
        
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
