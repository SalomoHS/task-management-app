# Frontend Services

This directory contains the Vue.js 3 frontend application for task management.

## Frontend Structure

```
src/
├── components/          # Reusable Vue components
│   ├── ConfirmationDialog.vue # Confirmation dialog
│   ├── LoginForm.vue    # Login form component
│   ├── Navigation.vue   # Navigation bar with logout
│   ├── ResponseModal.vue # Response modal
│   └── TaskGrid.vue     # Task grid display and management
├── lib/                 # Library utilities
│   └── utils.js         # Utility functions
├── stores/              # Pinia stores
│   ├── auth.js          # Authentication state management
│   ├── tasks.js         # Tasks state management
│   └── index.js         # Store exports
├── views/               # Page components
│   ├── DashboardView.vue # Main dashboard
│   └── LoginView.vue    # Login page
├── router/              # Vue Router configuration
│   └── index.js         # Routes and navigation guards
├── test/                # Test configuration
│   └── setup.js         # Test setup
├── App.vue              # Root component
└── main.js              # Application entry point
```

## Features

- **Authentication**: Login/logout functionality with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **Grid View**: Tasks displayed in a responsive grid layout
- **Real-time Updates**: State management with Pinia
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

- Vue.js 3 (Composition API)
- Vue Router 4
- Pinia (State Management)
- Axios (HTTP Client)
- Vite (Build Tool)

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update the FLask API URL in `.env` if needed:
Example `.env` content:
```
VITE_API_BASE_URL=http://localhost:5000
```

4. Start the development server:
```bash
npm run dev
```

5. Build for production:
```bash
npm run build
```

6. Preview production build:
```bash
npm run preview
```
The application will be available at `http://localhost:4173` by default.

## Authentication Flow

1. User enters credentials on login page
2. Frontend sends login request to backend API
3. Backend returns JWT token and user info
4. Token is stored in localStorage and added to axios headers
5. Protected routes require valid token
6. Logout clears token and redirects to login

## Task Management

- **Grid View**: Tasks displayed in responsive cards
- **CRUD Operations**: Create, edit, and delete tasks
- **Status Tracking**: Pending, In Progress, Completed
- **Date Display**: Creation date formatting
- **Modal Forms**: Inline editing and creation

## API Integration

The frontend communicates with the backend API at `http://localhost:5000` by default.

### Endpoints Used:
- `POST /users/login` - User authentication
- `GET /users/profile` - Token validation
- `GET /tasks` - Fetch user tasks
- `POST /tasks` - Create new task
- `PUT /tasks/:id` - Update task
- `POST /api/agent/process` - Process agent prompt
- `DELETE /tasks/:id` - Delete task