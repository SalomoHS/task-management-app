from .agent_crud import AgentCrud
from .agent_prompt_reviewer import AgentPromptReviewer
from rich.console import Console

console = Console()

class AgentGateway():
    def __init__(self):
        try:
            self.__reviewer_agent = AgentPromptReviewer()
            self.__crud_agent = AgentCrud()

        except Exception as e:
            console.print_exception(show_locals=True)
            console.print(f"[red](ai_agent.py) | Error in model initialization: {e}[/red]")
            raise

    async def call_agents(self, prompt):
        try:
            is_relevant, review_message = await self.__reviewer_agent.call(prompt)
            
            if not is_relevant:
                console.print(f"\n[red]Prompt rejected by Reviewer Agent: {review_message}[/red]")
                return {
                    "status": "rejected",
                    "message": review_message
                }
            
            console.print(f"\n[green]Prompt accepted by Reviewer Agent[/green]")
                
            agent = await self.__crud_agent.call(prompt)
            return {
                "status": "success",
                "message": agent
            }

        except Exception as e:
            console.print_exception(show_locals=True)
            console.print(f"[red](ai_agent.py) | Error processing your prompt:[/red]: {e}")
            return {
                "status": "error",
                "message": f"(ai_agent.py) | Error processing your prompt: {str(e)}"
            }

        finally:
            self.__reviewer_agent.close()
            self.__crud_agent.close()