<template>
  <div class="task-grid-container">
    <div class="task-grid-header">
      <h2>My Tasks</h2>
      <button @click="showCreateModal = true" class="create-btn">
        + Create Task
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      Loading tasks...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else-if="tasks.length === 0" class="no-tasks">
      No tasks found. Create your first task!
    </div>
    
    <div v-else class="task-grid">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="task-card"
      >
        <div class="task-header">
          <h3 class="task-title">{{ task.title }}</h3>
          <div class="task-actions">
            <button @click="editTask(task)" class="edit-btn">Edit</button>
            <button @click="deleteTask(task.task_id)" class="delete-btn">Delete</button>
          </div>
        </div>
        
        <p class="task-description">{{ task.description }}</p>
        
        <div class="task-footer">
          <span class="task-date">
            Created: {{ formatDate(task.created_at) }}
          </span>
          <span class="task-status" :class="getStatusClass(task)">
            {{ getStatusDisplay(task) }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Create/Edit Task Modal -->
    <div v-if="showCreateModal || editingTask" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h3>{{ editingTask ? 'Edit Task' : 'Create New Task' }}</h3>
        
        <form @submit.prevent="saveTask">
          <div class="form-group">
            <label for="title">Title:</label>
            <input
              id="title"
              v-model="taskForm.title"
              type="text"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea
              id="description"
              v-model="taskForm.description"
              rows="4"
              required
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="status">Status:</label>
            <select id="status" v-model="taskForm.status">
              <option value="to_do">To Do</option>
              <option value="in_progress">In Progress</option>
              <option value="done">Done</option>
            </select>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="cancel-btn">
              Cancel
            </button>
            <button type="submit" class="save-btn">
              {{ editingTask ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useTasksStore } from '../stores/tasks'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'TaskGrid',
  setup() {
    const tasksStore = useTasksStore()
    const authStore = useAuthStore()
    
    const showCreateModal = ref(false)
    const editingTask = ref(null)
    const taskForm = ref({
      title: '',
      description: '',
      status: 'to_do'
    })
    
    // Status mapping for API calls (status_id values)
    const statusMapping = {
      'to_do': 'TODO',
      'in_progress': 'INPROGRESS', 
      'done': 'DONE'
    }
    
    // Reverse mapping for status_id values
    const reverseStatusMapping = {
      'TODO': 'to_do',
      'INPROGRESS': 'in_progress',
      'DONE': 'done'
    }
    
    // Display mapping for status text from status table
    const displayStatusMapping = {
      'To Do': 'To Do',
      'In Progress': 'In Progress',
      'Done': 'Done'
    }
    
    const tasks = computed(() => tasksStore.tasks)
    const loading = computed(() => tasksStore.loading)
    const error = computed(() => tasksStore.error)
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const getStatusDisplay = (task) => {
      if (task.status_id) {
        if (typeof task.status_id === 'string') {
          // Direct status_id value like "TODO"
          const statusMap = {
            'TODO': 'To Do',
            'INPROGRESS': 'In Progress',
            'DONE': 'Done'
          }
          return statusMap[task.status_id] || 'To Do'
        } else if (task.status_id.status) {
          // Nested status object with display text like "To Do"
          return task.status_id.status
        }
      }
      return 'To Do'
    }
    
    const getStatusClass = (task) => {
      if (task.status_id) {
        if (typeof task.status_id === 'string') {
          // Direct status_id value like "TODO"
          const statusClassMap = {
            'TODO': 'to_do',
            'INPROGRESS': 'in_progress',
            'DONE': 'completed'
          }
          return statusClassMap[task.status_id] || 'to_do'
        } else if (task.status_id.status) {
          // Nested status object with display text like "To Do"
          const statusClassMap = {
            'To Do': 'to_do',
            'In Progress': 'in_progress',
            'Done': 'completed'
          }
          return statusClassMap[task.status_id.status] || 'to_do'
        }
      }
      return 'to_do'
    }
    
    const editTask = (task) => {
      editingTask.value = task
      
      // Handle both status_id (string) and status_id.status (display text)
      let currentStatus = 'to_do'
      if (task.status_id) {
        if (typeof task.status_id === 'string') {
          // Direct status_id value like "TODO"
          currentStatus = reverseStatusMapping[task.status_id] || 'to_do'
        } else if (task.status_id.status) {
          // Nested status object with display text like "To Do"
          const statusReverseMap = {
            'To Do': 'to_do',
            'In Progress': 'in_progress',
            'Done': 'completed'
          }
          currentStatus = statusReverseMap[task.status_id.status] || 'to_do'
        }
      }
      
      taskForm.value = {
        title: task.title,
        description: task.description,
        status: currentStatus
      }
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      editingTask.value = null
      taskForm.value = {
        title: '',
        description: '',
        status: 'to_do'
      }
    }
    
    const saveTask = async () => {
      const taskData = {
        title: taskForm.value.title,
        description: taskForm.value.description,
        status_id: statusMapping[taskForm.value.status] || 'TODO'
      }
      
      if (editingTask.value) {
        await tasksStore.updateTask(editingTask.value.task_id, taskData)
      } else {
        await tasksStore.createTask(taskData)
      }
      closeModal()
    }
    
    const deleteTask = async (taskId) => {
      if (confirm('Are you sure you want to delete this task?')) {
        await tasksStore.deleteTask(taskId)
      }
    }
    
    onMounted(async () => {
      // Wait for authentication to be ready
      if (authStore.token && !authStore.isAuthenticated) {
        await authStore.initializeAuth()
      }
      
      if (authStore.isLoggedIn) {
        await tasksStore.fetchTasks()
      }
    })
    
    return {
      tasks,
      loading,
      error,
      showCreateModal,
      editingTask,
      taskForm,
      formatDate,
      getStatusDisplay,
      getStatusClass,
      editTask,
      closeModal,
      saveTask,
      deleteTask
    }
  }
}
</script>

<style scoped>
.task-grid-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.task-grid-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.task-grid-header h2 {
  color: #333;
  margin: 0;
}

.create-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.create-btn:hover {
  background-color: #218838;
}

.loading, .error, .no-tasks {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.task-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}

.task-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.task-title {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
  flex: 1;
  margin-right: 1rem;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.edit-btn {
  background-color: #007bff;
  color: white;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
}

.task-description {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.task-date {
  color: #888;
}

.task-status {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: capitalize;
}

.task-status.to_do {
  background-color: #fff3cd;
  color: #856404;
}

.task-status.in_progress {
  background-color: #d1ecf1;
  color: #0c5460;
}

.task-status.completed {
  background-color: #d4edda;
  color: #155724;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.cancel-btn, .save-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background-color: #5a6268;
}

.save-btn {
  background-color: #007bff;
  color: white;
}

.save-btn:hover {
  background-color: #0056b3;
}
</style>