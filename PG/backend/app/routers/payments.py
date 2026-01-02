from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Payment, User, Complaint
from app.schemas import PaymentCreate, PaymentResponse
from app.auth import get_current_user

router = APIRouter(tags=["Payments & Stats"])

# -------------------------------
# Resident: Submit Payment
# -------------------------------
@router.post("/payments", response_model=PaymentResponse)
def submit_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    payment = Payment(
        user_id=current_user["user_id"],
        amount=data.amount,
        transaction_id=data.transaction_id,
        status="Pending"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

# -------------------------------
# Admin: Get All Payments
# -------------------------------
@router.get("/payments")
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    payments = db.query(Payment).all()
    result = []
    for p in payments:
        result.append({
            "id": p.id,
            "amount": p.amount,
            "transaction_id": p.transaction_id,
            "status": p.status,
            "created_at": p.created_at,
            "user_id": p.user_id,
            "user_name": p.user.full_name if p.user else "Unknown"
        })
    return result

# -------------------------------
# Resident: Get My Payments
# -------------------------------
@router.get("/payments/my")
def get_my_payments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Payment).filter(Payment.user_id == current_user["user_id"]).all()

# -------------------------------
# Admin: Approve Payment
# -------------------------------
@router.put("/payments/{payment_id}/approve")
def approve_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
         raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.status = "Approved"
    db.commit()
    return {"message": "Payment Approved"}

# -------------------------------
# Admin: Real-time Stats
# -------------------------------
@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    total_users = db.query(User).filter(User.role == "resident").count()
    
    # Determine total capacity (Hardcoded or Dynamic if needed, for user request we assume 100 for now or similar)
    total_capacity = 100 
    
    # Revenue: Sum of Approved Payments
    revenue = db.query(func.sum(Payment.amount)).filter(Payment.status == "Approved").scalar() or 0
    
    pending_revenue_count = db.query(Payment).filter(Payment.status == "Pending").count()
    
    active_issues = db.query(Complaint).filter(Complaint.status != "Resolved").count()
    high_priority_issues = 0 # If we implemented priority column properly we would count it
    
    # Staff (Dummy for now as we don't have staff model)
    total_staff = 8
    
    return {
        "total_residents": total_users,
        "revenue": revenue,
        "pending_revenue_count": pending_revenue_count,
        "capacity": total_capacity,
        "active_issues": active_issues,
        "total_staff": total_staff
    }
