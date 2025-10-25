import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
from models import User
import pytest



client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_registration(db):
    response = client.post(
        "/registration",
        json={
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "testuser@example.com"


def test_duplicate_registration(db):
    client.post(
        "/registration", 
        json={
            "email": "testuser2@example.com",
            "password": "pass"
            }
        )
    response = client.post(
        "/registration",
        json={"email": "testuser2@example.com",
        "password": "pass"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login(db):
  

    client.post(
        "/registration",
        json={
        "email": "login@example.com",
        "password": "pass"
        }
    )
   
    response = client.post(
        "/login",
        json={
            "email": "login@example.com",
            "password": "pass"
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["message"] == "Login successful"


def test_dashboard(db):
  
    response = client.get("/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "total_savings_accounts" in data
    assert "total_current_accounts" in data


def test_apply_loan(db):

    reg = client.post(
        "/registration",
        json={
            "email": "loan@example.com",
            "password": "pass"
            }
        )
    user_id = reg.json()["id"]

    response = client.post(
        "/applyloan",
        json={
            "user_id": user_id,
            "loan_type": "Personal",
            "amount": 100000,
            "tenure_months": 12,
            "interest_rate": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "emi" in data
    assert data["message"] == "Loan application submitted successfully."
