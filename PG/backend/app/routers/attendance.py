from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MealAttendance, User
from app.schemas import MealAttendanceUpdate, MealAttendanceResponse
from app.auth import get_current_user
from datetime import date, datetime

router = APIRouter(prefix="/attendance", tags=["Meal Attendance"])

@router.post("/update")
def update_attendance(
    data: MealAttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        target_date = datetime.strptime(data.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Check if record exists
    attendance = db.query(MealAttendance).filter(
        MealAttendance.user_id == current_user["user_id"],
        MealAttendance.date == target_date
    ).first()

    if attendance:
        # Update existing
        attendance.breakfast = data.breakfast
        attendance.lunch = data.lunch
        attendance.dinner = data.dinner
    else:
        # Create new
        attendance = MealAttendance(
            user_id=current_user["user_id"],
            date=target_date,
            breakfast=data.breakfast,
            lunch=data.lunch,
            dinner=data.dinner
        )
        db.add(attendance)
    
    db.commit()
    return {"message": "Attendance updated successfully"}

@router.get("/my-status", response_model=list[MealAttendanceResponse])
def get_my_status(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Fetch range
    records = db.query(MealAttendance).filter(
        MealAttendance.user_id == current_user["user_id"],
        MealAttendance.date >= start_date,
        MealAttendance.date <= end_date
    ).all()

    # Convert to response
    return [
        MealAttendanceResponse(
            date=str(record.date),
            breakfast=record.breakfast,
            lunch=record.lunch,
            dinner=record.dinner
        ) for record in records
    ]

@router.get("/day-stats")
def get_daily_stats(
    target_date: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Total residents (consistent with dashboard count)
    total_residents = db.query(User).filter(User.role == "resident").count()
    
    # Fetch opt-outs for that day
    opt_outs = db.query(MealAttendance).filter(MealAttendance.date == target_date).all()
    
    # Calculate opt-outs (where meal is False)
    opt_out_breakfast = sum(1 for r in opt_outs if not r.breakfast)
    opt_out_lunch = sum(1 for r in opt_outs if not r.lunch)
    opt_out_dinner = sum(1 for r in opt_outs if not r.dinner)
    
    return {
        "date": target_date,
        "total_residents": total_residents,
        "breakfast": {
            "eating": max(0, total_residents - opt_out_breakfast),
            "opt_out": opt_out_breakfast
        },
        "lunch": {
            "eating": max(0, total_residents - opt_out_lunch),
            "opt_out": opt_out_lunch
        },
        "dinner": {
            "eating": max(0, total_residents - opt_out_dinner),
            "opt_out": opt_out_dinner
        }
    }
