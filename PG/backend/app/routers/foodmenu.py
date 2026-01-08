from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FoodMenu
from app.schemas import FoodMenuCreate
from app.auth import get_current_user

router = APIRouter(
    prefix="/food",
    tags=["Food Menu"]
)

# -------------------------------
# Resident/Admin: Get Food Menu
# -------------------------------
@router.get("/")
def get_food_menu(db: Session = Depends(get_db)):
    return db.query(FoodMenu).all()

# -------------------------------
# Admin: Add or Update Food Menu
# -------------------------------
@router.post("/")
def add_food_menu(
    data: FoodMenuCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if user["role"] != "admin":
        return {"detail": "Not authorized"}

    menu = FoodMenu(
        day=data.day,
        breakfast=data.breakfast,
        lunch=data.lunch,
        dinner=data.dinner
    )

    db.add(menu)
    db.commit()
    return {"message": "Menu updated"}


@router.delete("/{day}")
def delete_food_menu(
    day: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if user["role"] != "admin":
        return {"detail": "Not authorized"}
        
    menu = db.query(FoodMenu).filter(FoodMenu.day == day).first()
    if not menu:
        return {"detail": "Menu not found for this day"}
        
    db.delete(menu)
    db.commit()
    return {"message": f"Menu for {day} deleted successfully"}
