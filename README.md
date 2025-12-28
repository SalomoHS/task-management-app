# Task Management Application

A full-stack task management application built with Vue.js frontend, Flask backend (PostgreSQL) database, and AI capabilities powered by Gemini and Strands.

## Project Structure

```
task-management-app/
├── frontend/                 # Vue.js frontend application
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/           # Vue views/pages
│   │   ├── services/        # API services
│   │   ├── stores/          # Pinia state management
│   │   ├── router/          # Vue Router configuration
│   │   └── lib/             # Library utilities
│   ├── package.json
│   └── vite.config.js
├── backend/                  # Flask backend API
│   ├── agents/              # AI Agents module (Gateway, Reviewer, CRUD)
│   ├── routes/              # API routes (tasks, users, agent)
│   ├── utils/               # Utility functions (DB, JWT)
│   ├── dev.py               # Development entry point
│   ├── prod.py              # Production entry point
│   ├── test_endpoints.py    # Endpoint testing script
│   └── requirements.txt
└── package.json              # Root package.json for scripts
```

## Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Supabase account (or any PostgreSQL database)
- Google Gemini API Key (for AI features)

### Installation

1. Clone the repository:
   ```bash
   https://github.com/SalomoHS/task-management-app git
   cd task-management-app
   ```

2. Install all dependencies:
   ```bash
   npm run install:all
   ```

3. Set up environment variables:

   **Frontend** (`frontend/.env`):
   ```
   VITE_API_BASE_URL=http://localhost:5000
   ```

   **Backend** (`backend/.env`):
   ```
   DB_NAME=your-db-name
   DB_HOST=your-db-host
   DB_PORT=your-db-port
   DB_USER=your-db-username
   DB_PASSWORD=your-db-password
   DB_SCHEMA=public
   
   FLASK_DEV_HOST=localhost
   FLASK_DEV_PORT=5000
   BASE_URL=http://localhost:5000
   
   JWT_SECRET_KEY=your-super-secret-jwt-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

### Development

Run both frontend and backend in development mode:
```bash
npm run dev
```

Or run them separately:
```bash
# Frontend only (runs on http://localhost:3000 by default)
npm run dev:frontend

# Backend only (runs on http://localhost:5000)
npm run dev:backend
```

### Testing

Run all tests:
```bash
npm test
```

Run tests separately:
```bash
# Frontend tests (Vitest)
npm run test:frontend

# Backend tests (Endpoint script)
npm run test:backend
```

### Build

Build the frontend for production:
```bash
npm run build
```

Run backend in production mode (Waitress):
```bash
npm run prod:backend
```

## Features

- **User Authentication**: Secure login with JWT tokens.
- **Task Management**: Full CRUD operations for tasks (Create, Read, Update, Delete).
- **AI Agent Integration**: 
  - Natural language processing for task management.
  - Intelligent prompt review and execution.
  - Powered by Google Gemini and Strands library.

## Technology Stack

**Frontend:**
- Vue.js 3
- Pinia (State Management)
- Vue Router
- Tailwind CSS
- Vite

**Backend:**
- Flask (Async)
- Waitress (Production Server)
- Strands (AI Agent Framework)
- Psycopg2 (PostgreSQL Adapter)
- PyJWT (Authentication)

**Database:**
- PostgreSQL