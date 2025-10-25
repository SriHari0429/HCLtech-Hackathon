from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SavingsAccount(Base):
    __tablename__ = "savings_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_number = Column(Integer, unique=True, index=True) 
    full_name = Column(String(255))
    dob = Column(String(255))
    address = Column(String(255))
    passport_photo = Column(String(255)) 
    aadhar_doc = Column(String(255))      
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class CurrentAccount(Base):
    __tablename__ = "current_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_number = Column(Integer, unique=True, index=True) 
    full_name = Column(String(255))
    dob = Column(String(255))
    address = Column(String(255))
    passport_photo = Column(String(255))
    pan_card = Column(String(255))
    business_proof = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loan_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    interest_rate = Column(Float, nullable=False)
    emi = Column(Float, nullable=False)
    status = Column(String(20), default="Pending") 
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

