from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Complaint
from app.schemas import ComplaintCreate
from app.auth import get_current_user

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)

# -------------------------------------------------
# Resident: Create a new complaint
# -------------------------------------------------
@router.post("/")
def create_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # ✅ Role check
    if current_user["role"] != "resident":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only residents can raise complaints"
        )

    complaint = Complaint(
        category=data.category,
        description=data.description,
        status="Pending",
        user_id=current_user["user_id"]
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return {
        "message": "Complaint submitted successfully",
        "complaint_id": complaint.id
    }



# -------------------------------------------------
# Resident: Get API for MY complaints
# -------------------------------------------------
@router.get("/my")
def get_my_complaints(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # ✅ Role check
    if current_user["role"] != "resident":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only residents can access this"
        )

    complaints = db.query(Complaint).filter(
        Complaint.user_id == current_user["user_id"]
    ).order_by(Complaint.created_at.desc()).all()

    return complaints


# -------------------------------------------------
# Admin: Get all complaints
# -------------------------------------------------
@router.get("/all")
def get_all_complaints(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # ✅ Admin check
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )

    complaints = db.query(Complaint).all()

    result = []
    for c in complaints:
        result.append({
            "id": c.id,
            "category": c.category,
            "description": c.description,
            "status": c.status,
            "created_at": c.created_at,
            "user": {
                "id": c.user.id if c.user else None,
                "full_name": c.user.full_name if c.user else None,
                "email": c.user.email if c.user else None
            }
        })

    return result


# -------------------------------------------------
# Admin: Resolve a complaint
# -------------------------------------------------
@router.put("/{complaint_id}/resolve")
def resolve_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # ✅ Admin check
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )

    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    complaint.status = "Resolved"
    db.commit()

    return {
        "message": "Complaint marked as Resolved",
        "complaint_id": complaint_id
    }
