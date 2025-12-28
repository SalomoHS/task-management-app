"""
Simple test script to demonstrate AI agent with task management tools.
Run this after starting the Flask server with: python app.py
"""
from agents.gateway import AgentGateway
from dotenv import load_dotenv
from rich.console import Console
load_dotenv()

console = Console()

def main():
    try:
        agent = AgentGateway()
        prompts = [
            "Tell me a joke",
            # "Create a new task called 'Review python code' with description 'Review the pull request'",
            # "Update task 'Review python code' status to complete",
            # "Delete task 'Review python code'"
        ]
        
        console.print("[bold blue]AI Task Manager Example[/bold blue]")
        console.print("=" * 50)
        
        for prompt in prompts:
            console.print(f"\n[bold]User:[/bold] {prompt}")
            console.print("[bold]AI Agent:[/bold] ")
            
            try:
                response = agent.call_agents(prompt)
                console.print(f"{response}")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
            
        
        console.print("\n[green]Example completed![/green]")
    except Exception as e:
        console.print(f"\n[red]Errpr! {e}[/red]") 

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
