# Task Management Application

A full-stack task management application built with Vue.js frontend, Flask backend, and Supabase database.

## Project Structure

```
task-management-app/
├── frontend/                 # Vue.js frontend application
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/          # Vue views/pages
│   │   ├── services/       # API services
│   │   ├── utils/          # Utility functions
│   │   └── router/         # Vue Router configuration
│   ├── package.json
│   └── vite.config.js
├── backend/                 # Flask backend API
│   ├── models/             # Database models
│   ├── routes/             # API routes
│   ├── utils/              # Utility functions
│   ├── tests/              # Test files
│   ├── app.py              # Flask application
│   └── requirements.txt
└── package.json            # Root package.json for scripts
```

## Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Supabase account

### Installation

1. Clone the repository
2. Install all dependencies:
   ```bash
   npm run install:all
   ```

3. Set up environment variables:
   - Copy `frontend/.env.example` to `frontend/.env`
   - Copy `backend/.env.example` to `backend/.env`
   - Fill in your Supabase credentials

### Development

Run both frontend and backend in development mode:
```bash
npm run dev
```

Or run them separately:
```bash
# Frontend only (runs on http://localhost:3000)
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
# Frontend tests
npm run test:frontend

# Backend tests
npm run test:backend
```

### Build

Build the frontend for production:
```bash
npm run build
```

## Features

- User authentication
- Task CRUD operations (Create, Read, Update, Delete)

## Technology Stack

**Frontend:**
- Vue.js 3

**Backend:**
- Flask web framework
- Supabase PostgreSQL database

**Testing:**
- Frontend: Vitest + Vue Test Utils + fast-check
- Backend: pytest + Hypothesis