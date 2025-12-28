import os
import json
from typing import Dict, Any, Optional, List
from strands.models.gemini import GeminiModel
from strands import Agent
from rich.console import Console
from task_tools import (
    get_all_tasks_tool, get_task_by_id_tool, find_task_tool, create_task_tool, 
    update_task_tool, delete_task_tool
)

console = Console()

class AICrudAgent:
    def __init__(self, temperature: float = 0.7):
        try:
            self.model = GeminiModel(
                client_args={
                    "api_key": os.getenv('GEMINI_API_KEY'),
                },
                model_id="gemini-2.5-flash",
                params={
                    "temperature": temperature,
                    "max_output_tokens": 8192,
                }
            )
            
            # Define system prompt for the AI agent
            self.__sys_prompt = """You are a helpful AI assistant that can manage tasks using the provided tools.
            
Available tools:
- find_task_tool(title: str): Find a task by its exact title. Use this to get the task_id if the user provides a title.
- create_task_tool(title: str, description: str, status_id: str): Create a new task (status_id: DONE/INPROGRESS/TODO)
- update_task_tool(task_id: int, current_title: str, title: str, description: str, status_id: str): Update an existing task.
- delete_task_tool(task_id: int, title: str): Delete a task.

IMPORTANT Workflow:
1. If the user refers to a task by name (e.g., "delete the 'shopping' task"), you MUST first use 'find_task_tool' to get the task's details and ID.
2. Once you have the 'task_id', use it in 'update_task_tool' or 'delete_task_tool'.
3. Although 'update_task_tool' and 'delete_task_tool' accept 'current_title', it is safer and preferred to find the ID first.

Use these tools to help users manage their tasks. Always provide clear and helpful responses.
"""
            
            # Initialize agents once
            self.__initialize_reviewer_agent()
            self.__initialize_agent()
            
            console.print("[green]AI Agent initialized successfully[/green]")
            
        except Exception as e:
            console.print_exception(show_locals=True)
            console.print(f"[red](ai_agent.py) | Error in model initialization: {e}[/red]")
            raise
    
    def __initialize_reviewer_agent(self):
        try:
            self.__reviewer_agent = Agent(
                    model=self.model,
                    tools=[], 
                    system_prompt="You are a Reviewer Agent for a Task Management System."
                )
        except Exception as e:
            console.print(f"[red](ai_agent.py) | Error initialize agent:[/red]: {e}")
            raise

    def __initialize_agent(self):
        try:
            self.__agent = Agent(
                model=self.model,
                tools=[
                    find_task_tool,
                    create_task_tool,
                    update_task_tool,
                    delete_task_tool
                ],
                system_prompt=self.__sys_prompt
            )

        except Exception as e:
            console.print(f"[red](ai_agent.py) | Error initialize agent:[/red]: {e}")
            raise

    def __review_prompt(self, prompt: str) -> bool:
        """
        Review the user prompt to ensure it is relevant to the task management capabilities.
        Returns True if the prompt is relevant, False otherwise.
        """
        review_prompt = f"""
        You are a Reviewer Agent for a Task Management System.
        Your job is to analyze the user's input and determine if it is related to managing tasks (CRUD operations: Create, Read, Update, Delete, Find).
        
        User Input: "{prompt}"
        
        If the input is relevant to task management (e.g., "add a task", "show tasks", "delete task", "change status"), respond with exactly: "SAFE"
        If the input is NOT relevant (e.g., "tell me a joke", "what is the weather", "write code"), respond with a polite explanation that you can only assist with task management.
        
        Response:
        """
        try:
            console.print(f"[yellow]Prompt REVIEW: {prompt}[/yellow]")
                
            response = self.__reviewer_agent(review_prompt)
            # Handle response structure safely
            if hasattr(response, 'message') and 'content' in response.message:
                 result = response.message['content'][0]['text'].strip()
            elif hasattr(response, 'text'):
                 result = response.text.strip()
            else:
                 # Fallback for unexpected response structure
                 result = str(response).strip()

            if "SAFE" in result:
                return True, None
            else:
                return False, result
                
        except Exception as e:
            console.print(f"[red]Error in prompt review: {e}[/red]")
            return False, "I encountered an error while reviewing your request. Please try again."

    def call_agent(self, prompt):
        try:
            # Step 1: Review the prompt
            is_relevant, review_message = self.__review_prompt(prompt)
            
            if not is_relevant:
                console.print(f"\n[red]Prompt rejected by Reviewer Agent: {review_message}[/red]")
                return review_message
            
            console.print(f"\n[green]Prompt accepted by Reviewer Agent: {review_message}[/green]")
                
            # Step 2: Proceed with the main agent
            agent = self.__agent(prompt)
            return agent
            # return review_message

        except Exception as e:
            console.print_exception(show_locals=True)
            console.print(f"[red](ai_agent.py) | Error processing your prompt:[/red]: {e}")
            return f"(ai_agent.py) | Error processing your prompt: {str(e)}"
            
    def close(self):
        """Cleanup resources used by the agents"""
        try:
            if hasattr(self, '_AICrudAgent__agent'):
                self.__agent.cleanup()
            if hasattr(self, '_AICrudAgent__reviewer_agent'):
                self.__reviewer_agent.cleanup()
            console.print("[green]AI Agent resources cleaned up successfully[/green]")
        except Exception as e:
            console.print(f"[red]Error closing agent resources: {e}[/red]")
