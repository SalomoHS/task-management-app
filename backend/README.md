# Backend Service

This directory contains the Flask-based backend for the Task Management application. It provides APIs for user authentication, task management, and AI agent interactions.

# Backend Structure

```
backend/
├── agents/                 # AI Agent logic and tools
│   ├── system_prompts/     # System prompts for AI agents
│   ├── tools/              # Tools available to agents
│   ├── agent_crud.py       # CRUD agent implementation
│   ├── agent_prompt_reviewer.py # Prompt reviewer agent
│   ├── gateway.py          # Gateway for agent interactions
│   └── language_model.py   # LLM configuration
├── routes/                 # API Routes (Blueprints)
│   ├── agent.py            # AI feature endpoints
│   ├── tasks.py            # Task management endpoints
│   └── users.py            # User authentication endpoints
├── utils/                  # Utility functions
│   ├── context.py          # Context management
│   ├── db_connection.py    # Database connection logic
│   └── jwt_utils.py        # JWT authentication utilities
├── dev.py                  # Development entry point
├── prod.py                 # Production entry point
├── requirements.txt        # Python dependencies
└── test_endpoints.py       # API testing script
```

## Setup

1. **Install Dependencies**
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Copy the example environment file and configure your credentials:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your database credentials, JWT secret, and API keys.

   **Example `.env` configuration:**

   ```ini
   # Database Configuration
   DB_NAME=my_db
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_SCHEMA=task-management-app

   # Flask Server Configuration
   FLASK_DEV_HOST=localhost
   FLASK_DEV_PORT=5000
   BASE_URL=http://localhost:5000

   # JWT Configuration
   JWT_SECRET_KEY=dev_secret_key_change_in_prod
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24

   # AI Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **Configuration Guide:**

   | Variable | Description | How to obtain |
   |----------|-------------|---------------|
   | **Database** | | |
   | `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` | PostgreSQL connection details. | Ensure you have PostgreSQL installed (I use PgAdmin4). Create a database (e.g., `my_db`,`task_management`). `DB_USER` and `DB_PASSWORD` are your Postgres credentials. |
   | `DB_SCHEMA` | Database schema name. | For this repo, set to `task-management-app`. |
   | **Flask** | | |
   | `FLASK_DEV_HOST`, `FLASK_DEV_PORT` | Host and port for the dev server. | Default to `localhost` and `5000`. |
   | `BASE_URL` | Base URL of the API. | Used for constructing absolute URLs. |
   | **JWT** | | |
   | `JWT_SECRET_KEY` | Secret key for signing tokens. | It can be a random value (e.g., `1234`, `abcd`). |
   | `JWT_ALGORITHM` | Encryption algorithm. | Common choice is `HS256`. |
   | `JWT_EXPIRATION_HOURS` | Token validity in hours. | Set as integer (e.g., `24`). |
   | **AI** | | |
   | `GEMINI_API_KEY` | Google Gemini API Key. | Get it from [Google AI Studio](https://aistudio.google.com/app/apikey). |

## Running the Application

The project provides two entry points depending on the environment:

### Development (`dev.py`)

The `dev.py` script is designed for local development.

- **Features**:
  - Automatically loads environment variables from `.env`.
  - Runs Flask in debug mode (`debug=True`) for hot reloading.
  - Uses `FLASK_DEV_HOST` and `FLASK_DEV_PORT` env variables from your configuration.
  - Configures rich logging for better readability in the console.

**Command**:
```bash
python dev.py
```

### Production (`prod.py`)

The `prod.py` script serves as the WSGI entry point for production deployments.

- **Features**:
  - Exposes the Flask `app` object for WSGI servers (e.g., Gunicorn, Waitress).
  - Does not enable debug mode.
  - Expects environment variables to be set in the system or container environment (though it still uses the same app factory pattern).
  - Configured for production-grade logging.

**Usage with a WSGI Server**:
Since `waitress` is included in the requirements, you can run the production app using:

```bash
# Example using waitress
waitress-serve --listen=*:8000 prod:app
```

## API Health Checks

Both entry points expose health check endpoints:
- `/health`: Basic connectivity check (checks DB connection).
- `/api/health`: JSON response with API version and status.

# Backend Test File

The `test_endpoints.py` script is provided to demonstrate and verify the API functionality, including JWT authentication and CRUD operations.

**Prerequisites**:
- The backend server must be running (e.g., via `python dev.py`).
- The `admin` user with password `admin` must exist (or update the script credentials).

**Usage**:
```bash
python test_endpoints.py
```

**What it tests**:
1. **Health Check**: Verifies the server is reachable.
2. **User Authentication**:
   - Logs in as `admin` to retrieve a JWT token.
   - Verifies the token.
   - Tests access control (authenticated vs. unauthenticated requests).
3. **User Management**:
   - Fetches user lists and specific user details.
4. **Task Management**:
   - Creates a new task.
   - Retrieves, updates, and deletes the created task.
5. **AI Agent**:
   - Test prompt processing endpoints.