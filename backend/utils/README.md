# Utilities Module

This module provides shared utility functions, classes, and helpers used across the backend application to handle common cross-cutting concerns like database access and authentication.

## Components

### 1. Database Connection (`db_connection.py`)
Manages interactions with the PostgreSQL database using `psycopg2`.
- **`DatabaseConnection` Class**: Singleton-style class that handles connection parameters and pooling.
- **Context Managers**:
  - `get_connection()`: Provides a safe way to get and release database connections.
  - `get_cursor()`: Provides a cursor for executing queries, handling commits and rollbacks automatically.
- **Helper Methods**:
  - `execute_query()`: Executes SELECT queries and returns results (fetch one or all).
  - `execute_update()`: Executes INSERT/UPDATE/DELETE queries and returns the row count.

### 2. JWT Utilities (`jwt_utils.py`)
Handles JSON Web Token (JWT) operations for authentication and security.
- **Token Management**:
  - `generate_jwt_token(user_data)`: Creates a signed token with user claims and expiration.
  - `decode_jwt_token(token)`: Decodes and validates a token.
  - `verify_jwt_token()`: Helper to extract and verify the token from the request header.
- **Decorators**:
  - `@jwt_required`: Protects routes by ensuring a valid token is present.
  - `@admin_required`: Restricts access to routes to users with the 'admin' role.

### 3. Context (`context.py`)
Provides context management for the application.
- **`request_token`**: A `ContextVar` used to store and access the JWT authentication token throughout the request lifecycle, which can be useful for passing context to agents or deep logic without threading arguments.
