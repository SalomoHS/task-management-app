import os
from strands.models.gemini import GeminiModel
from rich.console import Console

console = Console()

class LanguageModel:
    def __init__(self):
        try:
            self.model = GeminiModel(
                client_args={
                    "api_key": os.getenv('GEMINI_API_KEY'),
                },
                model_id="gemini-2.5-flash",
                params={
                    "temperature": 0.7,
                    "max_output_tokens": 8192,
                }
            )

        except Exception as e:
            console.print_exception(show_locals=True)
            console.print(f"[red](llm_model.py) | Error in model initialization: {e}[/red]")
            raise