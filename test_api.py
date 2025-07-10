import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Task Manager API...")
    
    # Test 1: API info
    print("\n1. Testing API info...")
    response = requests.get(f"{BASE_URL}/api")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Register user
    print("\n2. Testing user registration...")
    register_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 3: Login
    print("\n3. Testing login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        print(f"Token: {token[:50]}...")
        
        # Test 4: Get tasks (should be empty)
        print("\n4. Testing get tasks...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 5: Create task
        print("\n5. Testing create task...")
        task_data = {"title": "Test task from script"}
        response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 6: Get tasks again (should have 1 task)
        print("\n6. Testing get tasks after creation...")
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
    else:
        print(f"Login failed: {response.text}")

if __name__ == "__main__":
    test_api() 