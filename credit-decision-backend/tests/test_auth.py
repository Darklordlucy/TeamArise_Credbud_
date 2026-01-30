import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "phone": "9876543210",
        "city_tier": "tier_1"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"

def test_login_user():
    """Test user login"""
    # First register
    client.post("/api/auth/register", json={
        "email": "login@example.com",
        "password": "testpass123",
        "full_name": "Login User",
        "phone": "9876543211",
        "city_tier": "tier_2"
    })
    
    # Then login
    response = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_invalid_login():
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
