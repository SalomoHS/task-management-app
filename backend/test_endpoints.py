"""
Simple test script to demonstrate CRUD endpoints with JWT authentication
Run this after starting the Flask server with: python app.py
"""
import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def get_auth_token():
    """Get JWT token by logging in"""
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    # Note: users routes are prefixed with /api/users
    response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_users():
    print("=== Testing User Endpoints (Hardcoded Admin with JWT) ===")
    
    # Test login with correct credentials
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    # Note: users routes are prefixed with /api/users
    response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
    print(f"Login (Correct): {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        token = response.json()['token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get all users (now requires authentication)
        response = requests.get(f"{BASE_URL}/api/users", headers=headers)
        print(f"Get All Users (Authenticated): {response.status_code} - {response.json()}")
        
        # Get specific user (admin)
        response = requests.get(f"{BASE_URL}/api/users/1", headers=headers)
        print(f"Get Admin User (Authenticated): {response.status_code} - {response.json()}")
        
        # Get current user info
        response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
        print(f"Get Current User: {response.status_code} - {response.json()}")
        
        # Verify token
        verify_data = {"token": token}
        response = requests.post(f"{BASE_URL}/api/users/verify-token", json=verify_data)
        print(f"Verify Token: {response.status_code} - {response.json()}")
    
    # Test login with wrong credentials
    wrong_login_data = {
        "username": "admin",
        "password": "wrongpass"
    }
    response = requests.post(f"{BASE_URL}/api/users/login", json=wrong_login_data)
    print(f"Login (Wrong): {response.status_code} - {response.json()}")
    
    # Try to access protected route without token
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Get Users (No Auth): {response.status_code} - {response.json()}")
    
    # Try to get non-existent user
    token = get_auth_token()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/users/999", headers=headers)
        print(f"Get Non-existent User: {response.status_code} - {response.json()}")

def test_tasks():
    print("\n=== Testing Task CRUD with JWT Authentication ===")
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("Failed to get authentication token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to access tasks without authentication first
    # Note: tasks routes are prefixed with /api/tasks
    response = requests.get(f"{BASE_URL}/api/tasks")
    print(f"Get Tasks (No Auth): {response.status_code} - {response.json()}")
    
    # Create task with authentication
    task_data = {
        "title": "Test Task with JWT",
        "description": "This is a test task with JWT authentication",
        "status_id": "TODO"
    }
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
    print(f"Create Task (Authenticated): {response.status_code} - {response.json()}")
    
    if response.status_code == 201:
        task_id = response.json()['task_id']
        
        # Get task
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
        print(f"Get Task (Authenticated): {response.status_code} - {response.json()}")
        
        # Update task
        update_data = {"status_id": "INPROGRESS", "description": "Updated description with JWT"}
        response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data, headers=headers)
        print(f"Update Task (Authenticated): {response.status_code} - {response.json()}")
        
        # Get all tasks
        response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        print(f"Get All Tasks (Authenticated): {response.status_code} - {len(response.json())} tasks")
        
        # Delete task
        response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
        print(f"Delete Task (Authenticated): {response.status_code} - {response.json()}")

def test_ai_agent():
    print("\n=== Testing AI Agent CRUD Operations ===")
    
    # Test AI agent health
    response = requests.get(f"{BASE_URL}/ai-agent/health")
    print(f"AI Agent Health: {response.status_code} - {response.json()}")
    
    # Test create entity
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "developer"
    }
    response = requests.post(f"{BASE_URL}/ai-agent/create/user", json=user_data)
    print(f"Create User (AI): {response.status_code} - {response.json()}")
    
    # Test read entities
    response = requests.get(f"{BASE_URL}/ai-agent/read/user")
    print(f"Read Users (AI): {response.status_code} - {len(response.json().get('data', []))} users")
    
    # Test update entity
    update_data = {"role": "senior developer", "department": "engineering"}
    response = requests.put(f"{BASE_URL}/ai-agent/update/user/user-123", json=update_data)
    print(f"Update User (AI): {response.status_code} - {response.json()}")
    
    # Test delete entity
    response = requests.delete(f"{BASE_URL}/ai-agent/delete/user/user-123")
    print(f"Delete User (AI): {response.status_code} - {response.json()}")
    
    # Test query entities with natural language
    query_data = {"query": "find all senior developers in engineering department"}
    response = requests.post(f"{BASE_URL}/ai-agent/query/user", json=query_data)
    print(f"Query Users (AI): {response.status_code} - {len(response.json().get('data', []))} results")
    
    # Test validate entity
    test_data = {"name": "Jane Smith", "email": "jane@example.com", "role": "manager"}
    response = requests.post(f"{BASE_URL}/ai-agent/validate/user", json=test_data)
    print(f"Validate User (AI): {response.status_code} - {response.json()}")
    
    # Test task operations
    task_data = {
        "title": "Implement AI feature",
        "description": "Add AI-powered task management",
        "priority": "high",
        "estimated_hours": 8
    }
    response = requests.post(f"{BASE_URL}/ai-agent/create/task", json=task_data)
    print(f"Create Task (AI): {response.status_code} - {response.json()}")
    
    # Test query tasks
    task_query = {"query": "find high priority tasks that take less than 10 hours"}
    response = requests.post(f"{BASE_URL}/ai-agent/query/task", json=task_query)
    print(f"Query Tasks (AI): {response.status_code} - {len(response.json().get('data', []))} results")

if __name__ == "__main__":
    try:
        # Test health endpoint (no auth required)
        response = requests.get("http://localhost:5000/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
        
        # Test CRUD operations with JWT
        test_users()
        test_tasks()
        
        # Test AI Agent CRUD operations
        # test_ai_agent()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask server. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"Error: {e}")