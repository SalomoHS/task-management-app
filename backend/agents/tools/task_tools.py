"""
Task management tools for AI agent
These tools provide CRUD operations for tasks via HTTP requests to the Flask API
"""
import requests
import os
from strands import tool
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
from rich.console import Console
from utils.context import request_token

load_dotenv()
console = Console()

class TaskTools:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        token = request_token.get() or self.get_auth_token()
        self.headers = {"Authorization": f"Bearer {token}"}
        console.print(f"[green]Successfully create token {self.headers}[/green]")
    
    def get_auth_token(self):
        """Get JWT token by logging in"""
        try:
            login_data = {
                "username": "admin",
                "password": "admin"
            }
            response = requests.post(f"{self.base_url}/api/users/login", json=login_data)
            if response.status_code == 200:
                return response.json()['token']
            return None
        except Exception as e:
            console.print(f"[red]Error create JWT: {e}[/red]")
        
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks from the database"""
        try:
            response = requests.get(f"{self.base_url}/api/tasks", headers=self.headers)
            response.raise_for_status()
            tasks = response.json()
            console.print(f"[green]Successfully retrieved {len(tasks)} tasks[/green]")
            return tasks
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error getting tasks: {e}[/red]")
            return []
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID"""
        try:
            response = requests.get(f"{self.base_url}/api/tasks/{task_id}", headers=self.headers)
            response.raise_for_status()
            task = response.json()
            console.print(f"[green]Successfully retrieved task {task_id}[/green]")
            return task
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error getting task {task_id}: {e}[/red]")
            return None
    
    def create_task(self, title: str, description: str = "no description", status_id: str = "TODO") -> Optional[Dict[str, Any]]:
        """Create a new task"""
        try:
            data = {
                "title": title,
                "description": description,
                "status_id": status_id
            }

            console.print(f"[green]Created task payload: {data}[/green]")
            
            response = requests.post(f"{self.base_url}/api/tasks", 
                                   headers=self.headers, 
                                   json=data)
            response.raise_for_status()
            task = response.json()
            console.print(f"[green]Successfully created task: {task['title']}[/green]")
            return task
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error creating task: {e}[/red]")
            return None
    
    def find_task_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Find a task by its title"""
        all_tasks = self.get_all_tasks()
        for task in all_tasks:
            if task.get('title', '').lower() == title.lower():
                return task
        console.print(f"[yellow]Task with title '{title}' not found[/yellow]")
        return None

    def update_task(self, task_id: int, current_title:str, title: str,  status_id: str,
                   description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update an existing task"""
        try:
            data = {}

            if title is not None:
                data["title"] = title
            if description is not None:
                data["description"] = description
            if status_id is not None:
                data["status_id"] = status_id
            
            console.print(f"[yellow]Update payload: {data}[/yellow]")
                
            if not data:
                console.print("[yellow]No fields provided for update[/yellow]")
                return None
            
            response = requests.put(f"{self.base_url}/api/tasks/{task_id}", 
                                  headers=self.headers, 
                                  json=data)
            response.raise_for_status()
            task = response.json()
            console.print(f"[green]Successfully updated task '{current_title}'[/green]")
            return task
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error updating task '{current_title}': {e}[/red]")
            return None
    
    def delete_task(self, task_id: int, title:str) -> bool:
        """Delete a task"""
        try:
            response = requests.delete(f"{self.base_url}/api/tasks/{task_id}", headers=self.headers)
            response.raise_for_status()
            console.print(f"[green]Successfully deleted task '{title}'[/green]")
            return True
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error deleting task '{title}': {e}[/red]")
            return False

# Tool functions that can be used by the AI agent
def get_all_tasks_tool() -> str:
    """Tool function to get all tasks. Returns a formatted string with task information."""
    task_tools = TaskTools()
    tasks = task_tools.get_all_tasks()
    
    if not tasks:
        return "No tasks found or error occurred."
    
    result = "Available Tasks:\n"
    for task in tasks:
        result += f"- ID: {task.get('task_id')}, Title: {task.get('title')}, Status: {task.get('status', 'Unknown')}\n"
    
    return result

def get_task_by_id_tool(task_id: int) -> str:
    """Tool function to get a specific task by ID. Returns formatted task information."""
    task_tools = TaskTools()
    task = task_tools.get_task_by_id(task_id)
    
    if not task:
        return f"Task with ID {task_id} not found."
    
    return f"Task Details:\nID: {task.get('task_id')}\nTitle: {task.get('title')}\nDescription: {task.get('description')}\nStatus: {task.get('status', 'Unknown')}"

@tool
def find_task_tool(title: str) -> str:
    """
    Tool: find_task_tool
    Description: Tool function to find a task by its title.
    Args:
        title (str): task title
    Return
        Returns formatted task information.
    """
    task_tools = TaskTools()
    task = task_tools.find_task_by_title(title)
    
    if not task:
        return f"Task with title '{title}' not found."
    
    return f"Found Task:\nID: {task.get('task_id')}"

@tool
def create_task_tool(title: str, description: str = "no description", status_id: str = "TODO") -> str:
    """
    Tool: create_task_tool
    Description: Tool function to create a new task.
    Args:
        title (str): task title
        description (str): task description
        status_id (str): TODO | INPROGRESS | DONE
    Return:
        Returns success message or error.
    """
    task_tools = TaskTools()
    task = task_tools.create_task(title, description, status_id)
    
    if not task:
        return "Failed to create task."
    
    return f"Successfully created task: {task.get('title')} (ID: {task.get('task_id')})"

@tool
def update_task_tool(task_id: int = None, current_title: str = None, title: str = None, status: str = None, description: str = None) -> str:
    """
    Tool: update_task_tool
    Description: Tool function to update an existing task. You must provide task_id and current_title to identify the task.
    Args:
        task_id (int): task id
        current_title (str): current title
        title (str): new task title
        status (str): new task status, convert any input to exactly TODO | INPROGRESS | DONE
        description (str): new task description
    Return:
        Returns success message or error.
    """
    task_tools = TaskTools()
    
    # Resolve task_id if not provided
    if task_id is None:
        if current_title:
            found_task = task_tools.find_task_by_title(current_title)
            if found_task:
                task_id = found_task.get('task_id')
            else:
                return f"Could not find task with title '{current_title}' to update."
        else:
            return "Error: You must provide 'task_id' and 'current_title' to identify the task to update."

    task = task_tools.update_task(task_id=task_id, current_title=current_title, title=title, status_id=status, description=description)
    if not task:
        return f"Failed to update task {task_id}."
    
    return f"Successfully updated task {task_id}: {task.get('title')}"

@tool
def delete_task_tool(task_id: int = None, title: str = None) -> str:
    """
    Tool: delete_task_tool
    Description: Tool function to delete a task. You must provide task_id AND title to identify the task.
    Args:
        task_id (int): task id
        title (str): task title
    Return:
        Returns success message or error.
    """
    task_tools = TaskTools()
    
    # Resolve task_id if not provided
    if task_id is None:
        if title:
            found_task = task_tools.find_task_by_title(title)
            if found_task:
                task_id = found_task.get('task_id')
            else:
                return f"Could not find task with title '{title}' to delete."
        else:
            return "Error: You must provide 'task_id' and 'title' to identify the task to delete."

    success = task_tools.delete_task(task_id, title)
    
    if success:
        return f"Successfully deleted task {task_id}."
    else:
        return f"Failed to delete task {task_id}."