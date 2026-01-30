import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    """Get authentication token"""
    response = client.post("/api/auth/register", json={
        "email": "loantest@example.com",
        "password": "testpass123",
        "full_name": "Loan Test User",
        "phone": "9876543212",
        "city_tier": "tier_1"
    })
    return response.json()["access_token"]

def test_apply_loan(auth_token):
    """Test loan application"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/loans/apply", 
        headers=headers,
        json={
            "amount_requested": 100000,
            "num_debts": 1,
            "total_debt_amount": 50000,
            "monthly_emis": 5000,
            "total_assets": 200000,
            "monthly_income": 50000,
            "city_tier": "tier_1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "acceptance_rate" in data
    assert "ml_score" in data
