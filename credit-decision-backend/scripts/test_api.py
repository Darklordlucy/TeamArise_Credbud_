import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "phone": "9876543210",
        "city_tier": "tier_1"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def test_loan_application(token):
    """Test loan application"""
    print("\n=== Testing Loan Application ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "amount_requested": 100000,
        "num_debts": 2,
        "total_debt_amount": 50000,
        "monthly_emis": 5000,
        "total_assets": 200000,
        "monthly_income": 50000,
        "city_tier": "tier_1"
    }
    response = requests.post(f"{BASE_URL}/api/loans/apply", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_banks():
    """Test banks endpoint"""
    print("\n=== Testing Banks Endpoint ===")
    response = requests.get(f"{BASE_URL}/api/banks/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

if __name__ == "__main__":
    print("=" * 60)
    print("API ENDPOINT TESTING")
    print("=" * 60)
    
    results = []
    
    # Test basic endpoints
    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    
    # Test authentication
    token = test_register()
    if token:
        results.append(("User Registration", True))
        
        # Test login
        login_token = test_login()
        if login_token:
            results.append(("User Login", True))
            
            # Test loan application
            results.append(("Loan Application", test_loan_application(login_token)))
    else:
        results.append(("User Registration", False))
    
    # Test banks
    results.append(("Banks Endpoint", test_banks()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
