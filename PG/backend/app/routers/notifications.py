from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Notification
from app.auth import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/notifications", tags=["Notifications"])

class NotificationModel(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

@router.get("/", response_model=list[NotificationModel])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Notification).filter(
        Notification.user_id == current_user["user_id"]
    ).order_by(Notification.created_at.desc()).all()

@router.put("/{notif_id}/read")
def mark_notification_read(
    notif_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notif = db.query(Notification).filter(
        Notification.id == notif_id,
        Notification.user_id == current_user["user_id"]
    ).first()
    
    if not notif:
         raise HTTPException(status_code=404, detail="Notification not found")
         
    notif.is_read = True
    db.commit()
    return {"message": "Marked as read"}

@router.delete("/")
def clear_all_notifications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db.query(Notification).filter(
        Notification.user_id == current_user["user_id"]
    ).delete()
    db.commit()
    return {"message": "All notifications cleared"}

