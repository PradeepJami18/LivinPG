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

