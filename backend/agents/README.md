# AI Agents Module

This module implements the AI agent architecture for the Task Management System, leveraging the `strands` library and Gemini models to process natural language requests.

## Components

### 1. Agent Gateway (`gateway.py`)
The main entry point that orchestrates the agent workflow. It implements a two-step process:
- **Review**: Uses the `AgentPromptReviewer` to check if the user's prompt is relevant to the system's capabilities.
- **Execution**: If relevant, passes the prompt to the `AgentCrud` to perform the requested actions.

### 2. Prompt Reviewer (`agent_prompt_reviewer.py`)
A specialized agent responsible for validating user prompts. It ensures that the system only attempts to process requests related to task management, filtering out irrelevant or unsafe queries.

### 3. CRUD Agent (`agent_crud.py`)
The functional agent equipped with specific tools to interact with the task database. It can:
- Find tasks (`find_task_tool`)
- Create new tasks (`create_task_tool`)
- Update existing tasks (`update_task_tool`)
- Delete tasks (`delete_task_tool`)

### 4. Language Model (`language_model.py`)
Contains the configuration for the Large Language Model (LLM). It initializes the `GeminiModel` with the necessary API keys and parameters (temperature, token limits).

## Usage

The `AgentGateway` is primarily used by the API routes (specifically `routes/agent.py`) to handle incoming requests from the frontend or API clients.

```python
from agents.gateway import AgentGateway

gateway = AgentGateway()
result = await gateway.call_agents("Create a new task for reviewing the code")
```
