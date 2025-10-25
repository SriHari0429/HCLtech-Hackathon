from fastapi import FastAPI, HTTPException, Depends, UploadFile,File,Form
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User ,SavingsAccount, CurrentAccount,Loan
from schemas import UserCreate, UserLogin, UserResponse, SavingsAccountCreate, CurrentAccountCreate,LoanCreate
from passlib.context import CryptContext
from sqlalchemy import func
from math import pow
from datetime import datetime

from auth import create_access_token
import shutil
import os
import random

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

app = FastAPI(title="SmartBank MySQL Backend")


Base.metadata.create_all(bind=engine)


def generate_account_number():
    return str(random.randint(10**14, 10**15 - 1))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# registration api
@app.post("/registration", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# login api
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email, "id": db_user.id})
    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}

# savings account api
@app.post("/savingsaccount")
def create_savings_account(
    user_id: int = Form(...),
    full_name: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...),
    passport_photo: UploadFile = File(...),
    aadhar_doc: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    account_number = generate_account_number()

    passport_path = os.path.join(UPLOAD_DIR, f"{account_number}_passport_{passport_photo.filename}")
    aadhar_path = os.path.join(UPLOAD_DIR, f"{account_number}_aadhar_{aadhar_doc.filename}")

    for file, path in [(passport_photo, passport_path), (aadhar_doc, aadhar_path)]:
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    new_account = SavingsAccount(
    user_id=user_id,
    account_number=account_number,
    full_name=full_name,
    dob=dob,
    address=address,
    passport_photo=passport_path,
    aadhar_doc=aadhar_path
)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {"message": "Savings Account created successfully", "account_number": account_number}

# current account api
@app.post("/currentaccount")
def create_current_account(
    user_id: int = Form(...),
    full_name: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...),
    passport_photo: UploadFile = File(...),
    pan_card: UploadFile = File(...),
    business_proof: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    account_number = generate_account_number()

    passport_path = os.path.join(UPLOAD_DIR, f"{account_number}_passport_{passport_photo.filename}")
    pan_path = os.path.join(UPLOAD_DIR, f"{account_number}_pan_{pan_card.filename}")
    business_path = os.path.join(UPLOAD_DIR, f"{account_number}_business_{business_proof.filename}")

    for file, path in [(passport_photo, passport_path), (pan_card, pan_path), (business_proof, business_path)]:
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    new_account = CurrentAccount(
        user_id=user_id,
        account_number=account_number,
        full_name=full_name,
        dob=dob,
        address=address,
        passport_photo=passport_path,
        pan_card=pan_path,
        business_proof=business_path
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {"message": "Current Account created successfully", "account_number": account_number}


# dashboard data api
@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_savings_accounts = db.query(SavingsAccount).count()
    total_current_accounts = db.query(CurrentAccount).count()

    return {
        "total_users": total_users,
        "total_savings_accounts": total_savings_accounts,
        "total_current_accounts": total_current_accounts,
    }

# applying for loan api
@app.post("/applyloan")
def apply_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    P = loan.amount
    R = loan.interest_rate / (12 * 100)  # convert to monthly rate
    N = loan.tenure_months

    emi = (P * R * pow(1 + R, N)) / (pow(1 + R, N) - 1)

    new_loan = Loan(
        user_id=loan.user_id,
        loan_type=loan.loan_type,
        amount=loan.amount,
        tenure_months=loan.tenure_months,
        interest_rate=loan.interest_rate,
        emi=round(emi, 2),
        created_at=datetime.utcnow()
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return {
        "message": "Loan application submitted successfully.",
        "loan_id": new_loan.id,
        "emi": new_loan.emi
    }
# only for admin use to approve loan
@app.put("/admin/loanstatus/{loan_id}")
def update_loan_status(loan_id: int, status: str, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        return {"error": "Loan not found"}

    if status not in ["Approved", "Rejected"]:
        return {"error": "Invalid status. Choose 'Approved' or 'Rejected'"}

    loan.status = status
    db.commit()
    db.refresh(loan)

    return {"message": f"Loan {status.lower()} successfully.", "loan_id": loan.id}