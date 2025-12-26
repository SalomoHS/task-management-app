"""
Simple test script to demonstrate CRUD endpoints
Run this after starting the Flask server with: python run.py
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_users():
    print("=== Testing User Endpoints (Hardcoded Admin) ===")
    
    # Get all users (should return hardcoded admin without password)
    response = requests.get(f"{BASE_URL}/users")
    print(f"Get All Users: {response.status_code} - {response.json()}")
    
    # Get specific user (admin)
    response = requests.get(f"{BASE_URL}/users/1")
    print(f"Get Admin User: {response.status_code} - {response.json()}")
    
    # Test login with correct credentials
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    print(f"Login (Correct): {response.status_code} - {response.json()}")
    
    # Test login with wrong credentials
    wrong_login_data = {
        "username": "admin",
        "password": "wrongpass"
    }
    response = requests.post(f"{BASE_URL}/users/login", json=wrong_login_data)
    print(f"Login (Wrong): {response.status_code} - {response.json()}")
    
    # Try to get non-existent user
    response = requests.get(f"{BASE_URL}/users/999")
    print(f"Get Non-existent User: {response.status_code} - {response.json()}")
    
    # Try to create user (should be disabled)
    user_data = {
        "username": "testuser",
        "password": "testpass",
        "role": "admin"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Create User (Disabled): {response.status_code} - {response.json()}")

def test_tasks():
    print("\n=== Testing Task CRUD ===")
    
    # Create task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status_id": "TODO"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    print(f"Create Task: {response.status_code} - {response.json()}")
    
    if response.status_code == 201:
        task_id = response.json()['task_id']
        
        # Get task
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        print(f"Get Task: {response.status_code} - {response.json()}")
        
        # Update task
        update_data = {"status_id": "INPROGRESS", "description": "Updated description"}
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
        print(f"Update Task: {response.status_code} - {response.json()}")
        
        # Get all tasks
        response = requests.get(f"{BASE_URL}/tasks")
        print(f"Get All Tasks: {response.status_code} - {len(response.json())} tasks")
        
        # Delete task
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        print(f"Delete Task: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
        
        # Test CRUD operations
        test_users()
        test_tasks()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask server. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"Error: {e}")