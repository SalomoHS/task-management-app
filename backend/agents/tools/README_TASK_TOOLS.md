# AI Agent Task Management Integration

This integration allows your AI agent to manage tasks using the Flask API endpoints as tools.

## Architecture

The integration consists of three main components:

1. **Flask API Endpoints** (`routes/tasks.py`): RESTful endpoints for task CRUD operations
2. **Task Tools** (`task_tools.py`): Tool functions that wrap the API endpoints
3. **AI Agent** (`ai_agent.py`): AI agent that can use the task tools

## How It Works

### 1. Task Tools (`task_tools.py`)

The `TaskTools` class provides methods to interact with the Flask API:

- `get_all_tasks()`: Retrieves all tasks
- `get_task_by_id(task_id)`: Gets a specific task
- `create_task(title, description, status_id)`: Creates a new task
- `update_task(task_id, title, description, status_id)`: Updates an existing task
- `delete_task(task_id)`: Deletes a task

Each tool function returns a user-friendly string that the AI agent can use in its responses.

### 2. AI Agent Integration (`ai_agent.py`)

The AI agent is configured with:

- **System Prompt**: Explains the available tools and their purposes
- **Tool Functions**: The task management functions are registered as tools
- **Gemini Model**: Uses Google's Gemini model for natural language processing

### 3. Flask API (`routes/tasks.py`)

The existing Flask endpoints provide the backend functionality:

- `GET /api/tasks`: List all tasks
- `GET /api/tasks/<id>`: Get specific task
- `POST /api/tasks`: Create new task
- `PUT /api/tasks/<id>`: Update task
- `DELETE /api/tasks/<id>`: Delete task

## Setup and Usage

### Prerequisites

1. Set up your environment variables:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   export JWT_TOKEN="your-jwt-token-for-api-authentication"
   ```

2. Ensure your Flask API is running (typically on `http://localhost:5000`)

### Basic Usage

```python
from ai_agent import AICrudAgent

# Initialize the AI agent
agent = AICrudAgent()

# Ask the agent to manage tasks
response = agent.call_agent("Show me all my tasks")
print(response)

response = agent.call_agent("Create a new task called 'Review code'")
print(response)
```

### Example Commands

The AI agent can understand natural language commands like:

- "Show me all my tasks"
- "Create a new task called 'Review code' with description 'Review the pull request'"
- "Get task with ID 1"
- "Update task 1 to have status 2"
- "Delete task with ID 5"

## Configuration

### Base URL

You can configure the base URL for the Flask API by passing it to the `TaskTools` constructor:

```python
task_tools = TaskTools(base_url="http://your-api-server.com")
```

### JWT Token

The tools automatically use the JWT token from the `JWT_TOKEN` environment variable, or you can pass it explicitly:

```python
task_tools = TaskTools(jwt_token="your-jwt-token")
```

## Error Handling

The integration includes comprehensive error handling:

- API request failures are caught and logged
- Tool functions return user-friendly error messages
- The AI agent can gracefully handle tool failures

## Testing

Run the example script to test the integration:

```bash
cd backend
python example_usage.py
```

This will demonstrate various task management operations through the AI agent.