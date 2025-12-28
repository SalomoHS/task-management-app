# Backend Service

This directory contains the Flask-based backend for the Task Management application. It provides APIs for user authentication, task management, and AI agent interactions.

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
5. **AI Agent** (Optional):
   - Can be enabled to test prompt processing endpoints.

