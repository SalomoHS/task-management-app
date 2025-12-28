import os
from strands import Agent
from .language_model import LanguageModel
from rich.console import Console


console = Console()

class AgentPromptReviewer(LanguageModel):
    def __init__(self):
        try:
            super().__init__()
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(base_dir, "system_prompts", "ai-agent-reviewer.txt")
            with open(prompt_path,"r") as f:
                self.__reviewer_sys_prompt = f.read()
            
            self.__initialize_reviewer_agent()
            
            console.print("[green]Prompt Reviewer Agent initialized successfully[/green]")
            
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

    def __review_prompt(self, prompt: str) -> bool:
        """
        Review the user prompt to ensure it is relevant to the task management capabilities.
        Returns True if the prompt is relevant, False otherwise.
        """
        
        review_prompt = self.__reviewer_sys_prompt.format(
                prompt=str(prompt),
        )

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

    def call(self, prompt):
        try:
            # Step 1: Review the prompt
            is_relevant, review_message = self.__review_prompt(prompt)
            
            return is_relevant, review_message
            if not is_relevant:
                console.print(f"\n[red]Prompt rejected by Reviewer Agent: {review_message}[/red]")
                return review_message
            
            console.print(f"\n[green]Prompt accepted by Reviewer Agent: {review_message}[/green]")
                
            # Step 2: Proceed with the main agent
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
            console.print("\n[green]Prompt Reviewer Agent resources cleaned up successfully[/green]")
        except Exception as e:
            console.print(f"[red]Error closing agent resources: {e}[/red]")
