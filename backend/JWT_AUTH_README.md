# JWT Authentication Implementation

This implementation adds JWT (JSON Web Token) authentication to the task management API with a hardcoded dummy admin user.

## Features

- JWT token generation and validation
- Hardcoded admin user for demo purposes
- Protected API endpoints
- Token expiration (24 hours)
- Role-based access control

## Hardcoded Admin User

- **Username**: `admin`
- **Password**: `admin`
- **Role**: `admin`

## API Endpoints

### Authentication Endpoints

#### Login
```
POST /api/users/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Response (Success):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

#### Verify Token
```
POST /api/users/verify-token
Content-Type: application/json

{
  "token": "your-jwt-token-here"
}
```

#### Get Current User
```
GET /api/users/me
Authorization: Bearer your-jwt-token-here
```

### Protected Endpoints

All the following endpoints require authentication via JWT token in the Authorization header:

- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get specific user
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/{id}` - Get specific task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Using JWT Tokens

Include the JWT token in the Authorization header for all protected endpoints:

```
Authorization: Bearer your-jwt-token-here
```

## Environment Variables

Add to your `.env` file:
```
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-2024
```

## Installation

1. Install the required dependency:
```bash
pip install PyJWT==2.8.0
```

2. Or install all requirements:
```bash
pip install -r requirements.txt
```

## Testing

Run the test scripts to verify JWT functionality:

```bash
# Test JWT authentication specifically
python test_jwt.py

# Test all endpoints with JWT
python test_endpoints.py
```

## Security Notes

- The JWT secret key should be changed in production
- Tokens expire after 24 hours
- The hardcoded admin user is for demo purposes only
- In production, implement proper user management and password hashing

## Token Structure

The JWT payload contains:
- `user_id`: User ID
- `username`: Username
- `role`: User role
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

## Error Responses

### 401 Unauthorized
- Missing token
- Invalid token
- Expired token
- Wrong credentials

### 403 Forbidden
- Insufficient permissions (admin required)

## Example Usage

```python
import requests

# Login
login_response = requests.post('http://localhost:5000/api/users/login', json={
    'username': 'admin',
    'password': 'admin'
})

token = login_response.json()['token']

# Use token for protected endpoints
headers = {'Authorization': f'Bearer {token}'}
tasks_response = requests.get('http://localhost:5000/api/tasks', headers=headers)
```