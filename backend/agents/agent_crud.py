import os
from strands import Agent
from .language_model import LanguageModel
from rich.console import Console
from .tools.task_tools import (
    find_task_tool, create_task_tool, 
    update_task_tool, delete_task_tool
)

console = Console()

class AgentCrud(LanguageModel):
    def __init__(self):
        try:
            super().__init__()
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(base_dir, "system_prompts", "ai-agent-crud.txt")
            with open(prompt_path,"r") as f:
                self.__crud_sys_prompt = f.read()
            
            self.__initialize_agent()
            
            console.print("[green]CRUD Agent initialized successfully[/green]")
            
        except Exception as e:
            console.print_exception(show_locals=True)
            console.print(f"[red](ai_agent.py) | Error in model initialization: {e}[/red]")
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
                                system_prompt=self.__crud_sys_prompt
                            )

        except Exception as e:
            console.print(f"[red](ai_agent.py) | Error initialize agent:[/red]: {e}")
            raise

    async def call(self, prompt):
        try:
            
            agent = self.__agent(prompt)
            return agent

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
            console.print("[green]CRUD Agent resources cleaned up successfully[/green]")
        except Exception as e:
            console.print(f"[red]Error closing agent resources: {e}[/red]")
