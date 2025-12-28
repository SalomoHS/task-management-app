# API Routes Module

This module defines the RESTful API endpoints for the application using Flask Blueprints. It handles HTTP requests, input validation, and connects to the underlying business logic and database.

## Blueprints

### 1. Agent Routes (`agent.py`)
Handles interactions with the AI agent system.
- **POST** `/api/agent/process`: Accepts a natural language prompt and processes it via the `AgentGateway`. Returns the agent's response and any actions taken.
  - *Auth*: Required

### 2. Task Routes (`tasks.py`)
Provides standard CRUD operations for managing tasks.
- **GET** `/api/tasks`: Retrieve a list of all tasks.
- **GET** `/api/tasks/<id>`: Retrieve details of a specific task.
- **POST** `/api/tasks`: Create a new task. Required fields: `title`, `status_id`.
- **PUT** `/api/tasks/<id>`: Update an existing task. Supports partial updates.
- **DELETE** `/api/tasks/<id>`: Delete a task.
  - *Auth*: Required for all endpoints

### 3. User Routes (`users.py`)
Manages user authentication and retrieval.
- **POST** `/api/users/login`: Authenticate using username and password to receive a JWT token.
- **GET** `/api/users`: List all users (currently returns the hardcoded admin).
- **GET** `/api/users/me`: Get details of the currently authenticated user.
- **POST** `/api/users/verify-token`: Verify if a provided JWT token is valid.
  - *Auth*: Required for most endpoints except login and token verification.

## Authentication

The API uses JSON Web Tokens (JWT) for authentication. Protected endpoints require a valid token in the `Authorization` header:
```
Authorization: Bearer <your_token>
```
