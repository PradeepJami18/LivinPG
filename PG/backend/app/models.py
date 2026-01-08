from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(20), default="resident")
    phone = Column(String(15))
    status = Column(String(20), default="Active") # Active, Left, Notice
    created_at = Column(DateTime, server_default=func.now())

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category = Column(String(50))
    description = Column(Text)
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")

class FoodMenu(Base):
    __tablename__ = "food_menu"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(String(20))
    breakfast = Column(String(100))
    lunch = Column(String(100))
    dinner = Column(String(100))

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    amount = Column(Integer)
    transaction_id = Column(String(100))
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")

class MealAttendance(Base):
    __tablename__ = "meal_attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    
    # Defaults to True (Eating), User sets to False (Opt-out)
    breakfast = Column(Boolean, default=True) 
    lunch = Column(Boolean, default=True)
    dinner = Column(Boolean, default=True)

    user = relationship("User")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(100))
    message = Column(String(255))
    type = Column(String(50), default="info") # payment, complaint, system
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")

