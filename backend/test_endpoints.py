"""
Simple test script to demonstrate CRUD endpoints with JWT authentication
Run this after starting the Flask server with: python app.py
"""
import aiohttp
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from rich.panel import Panel
from rich.console import Console
console = Console()

BASE_URL = os.getenv("BASE_URL")

async def get_auth_token(session):
    """Get JWT token by logging in"""
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    # Note: users routes are prefixed with /api/users
    try:
        async with session.post(f"{BASE_URL}/api/users/login", json=login_data) as response:
            if response.status == 200:
                data = await response.json()
                return data['token']
    except Exception as e:
        print(f"Error getting auth token: {e}")
    return None

async def test_users(session):
    console.print("\n")
    console.rule("[bold blue]Testing User Endpoints (Hardcoded Admin with JWT)[/bold blue]")
    
    # Test login with correct credentials
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    # Note: users routes are prefixed with /api/users
    async with session.post(f"{BASE_URL}/api/users/login", json=login_data) as response:
        data = await response.json()
        style = "bold green" if response.status == 200 else "bold red"
        console.print(f"Login (Correct): [{style}]{response.status}[/{style}] - {data}")
        
        if response.status == 200:
            token = data['token']
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get all users (now requires authentication)
            async with session.get(f"{BASE_URL}/api/users", headers=headers) as resp:
                console.print(f"Get All Users (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
            
            # Get specific user (admin)
            async with session.get(f"{BASE_URL}/api/users/1", headers=headers) as resp:
                console.print(f"Get Admin User (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
            
            # Get current user info
            async with session.get(f"{BASE_URL}/api/users/me", headers=headers) as resp:
                console.print(f"Get Current User: [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
            
            # Verify token
            verify_data = {"token": token}
            async with session.post(f"{BASE_URL}/api/users/verify-token", json=verify_data) as resp:
                console.print(f"Verify Token: [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
    
    # Test login with wrong credentials
    wrong_login_data = {
        "username": "admin",
        "password": "wrongpass"
    }
    async with session.post(f"{BASE_URL}/api/users/login", json=wrong_login_data) as response:
        console.print(f"Login (Wrong): [{ 'green' if response.status == 200 else 'red' }]{response.status}[/] - {await response.json()}")
    
    # Try to access protected route without token
    async with session.get(f"{BASE_URL}/api/users") as response:
        console.print(f"Get Users (No Auth): [{ 'green' if response.status == 200 else 'red' }]{response.status}[/] - {await response.json()}")
    
    # Try to get non-existent user
    token = await get_auth_token(session)
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        async with session.get(f"{BASE_URL}/api/users/999", headers=headers) as response:
            console.print(f"Get Non-existent User: [{ 'green' if response.status == 200 else 'red' }]{response.status}[/] - {await response.json()}")

async def test_tasks(session):
    console.print("\n")
    console.rule("[bold blue]Testing Task CRUD with JWT Authentication[/bold blue]")
    
    # Get authentication token
    token = await get_auth_token(session)
    if not token:
        console.print("[bold red]Failed to get authentication token[/bold red]")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    
    # Try to access tasks with authentication first
    # Note: tasks routes are prefixed with /api/tasks
    
    task_data = {
        "title": "Test Task with JWT",
        "description": "This is a test task with JWT authentication",
        "status_id": "TODO"
    }

    async with session.get(f"{BASE_URL}/api/tasks",headers=headers) as response:
        console.print(f"Get Tasks (Authenticated): [{ 'green' if response.status == 200 else 'red' }]{response.status}[/] - {await response.json()}")
    
    async with session.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers) as response:
        data = await response.json()
        console.print(f"Create Task (Authenticated): [{ 'green' if response.status == 201 else 'red' }]{response.status}[/] - {data}")
    
        if response.status == 201:
            task_id = data['task_id']
            
            # Get task
            async with session.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers) as resp:
                console.print(f"Get Task (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
            
            # Update task
            update_data = {"status_id": "INPROGRESS", "description": "Updated description with JWT"}
            async with session.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data, headers=headers) as resp:
                console.print(f"Update Task (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
            
            # Get all tasks
            async with session.get(f"{BASE_URL}/api/tasks", headers=headers) as resp:
                tasks = await resp.json()
                console.print(f"Get All Tasks (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {len(tasks)} tasks")
            
            # Delete task
            async with session.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers) as resp:
                console.print(f"Delete Task (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
    
    console.print("\n")
    console.rule("[bold blue]Testing Task CRUD without JWT Authentication[/bold blue]")
    
    # Try to access tasks without authentication first
    # Note: tasks routes are prefixed with /api/tasks
    async with session.get(f"{BASE_URL}/api/tasks") as response:
        console.print(f"Get Tasks (No Auth): [{ 'green' if response.status == 200 else 'red' }]{response.status}[/] - {await response.json()}")
    
    async with session.post(f"{BASE_URL}/api/tasks", json=task_data) as response:
        data = await response.json()
        console.print(f"Create Task (No Auth): [{ 'green' if response.status == 201 else 'red' }]{response.status}[/] - {data}")
    
        if response.status == 201:
            task_id = data['task_id']
            
            # Get task
            async with session.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers) as resp:
                console.print(f"Get Task (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
            
            # Update task
            update_data = {"status_id": "INPROGRESS", "description": "Updated description with JWT"}
            async with session.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data, headers=headers) as resp:
                console.print(f"Update Task (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
            
            # Get all tasks
            async with session.get(f"{BASE_URL}/api/tasks", headers=headers) as resp:
                tasks = await resp.json()
                console.print(f"Get All Tasks (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {len(tasks)} tasks")
            
            # Delete task
            async with session.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers) as resp:
                console.print(f"Delete Task (Authenticated): [{ 'green' if resp.status == 200 else 'red' }]{resp.status}[/] - {await resp.json()}")
    
async def test_ai_agent(session):
    console.print("\n")
    console.rule("[bold blue]Testing AI Agent (Prompt-based)[/bold blue]")
    
    # Get authentication token
    token = await get_auth_token(session)
    if not token:
        console.print("[bold red]Failed to get authentication token[/bold red]")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test prompt processing
    # prompt = "Create a new task called 'Test Task from Agent' with description 'Created via API agent'"
    prompt = "Tell me a joke"
    console.print(f"Sending prompt: [italic]{prompt}[/italic]")
    
    try:
        # First try without token (should fail)
        console.print("Testing without token (expecting 401)...")
        async with session.post(f"{BASE_URL}/api/agent/process", json={"prompt": prompt}) as response:
            console.print(f"Agent Response (No Auth): [{ 'green' if response.status == 200 else 'yellow' }]{response.status}[/] - {await response.json()}")

        # Then try with token
        console.print("Testing with token...")
        async with session.post(f"{BASE_URL}/api/agent/process", json={"prompt": prompt}, headers=headers) as response:
            console.print(f"Agent Response (Authenticated): [{ 'green' if response.status == 200 else 'red' }]{response.status}[/] - {await response.json()}")
    except Exception as e:
        console.print(f"[bold red]Error testing agent: {e}[/bold red]")

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            # Test health endpoint (no auth required)
            try:
                async with session.get(f"{BASE_URL}/health") as response:
                    console.print(Panel.fit(f"Health Check: [{ 'green' if response.status == 200 else 'red' }]{response.status}[/] - {await response.json()}", title="System Status"))
            except aiohttp.ClientError:
                 console.print("[bold red]Error: Could not connect to Flask server. Make sure it's running on localhost:5000[/bold red]")
                 return

            # Test CRUD operations with JWT
            await test_users(session)
            await test_tasks(session)
            
            # Test AI Agent
            await test_ai_agent(session)
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

if __name__ == "__main__":
    asyncio.run(main())
