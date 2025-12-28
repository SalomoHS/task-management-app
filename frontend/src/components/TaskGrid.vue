<template>
  <div class="task-grid-container">
    <div class="task-grid-header">
      <h2>My Tasks</h2>
      <button @click="showCreateModal = true" class="create-btn">
        + Create Task
      </button>
    </div>
    
    <!-- Filters Container -->
    <div class="filters-container">
      <!-- Time Order Filter -->
      <div class="time-order-filter">
        <label for="time-order-filter">Order by Time:</label>
        <select id="time-order-filter" v-model="timeOrderFilter" class="filter-dropdown">
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
        </select>
      </div>
      
      <!-- Status Filter -->
      <div class="status-filter">
        <label for="status-filter">Status:</label>
        <select id="status-filter" v-model="statusFilter" class="filter-dropdown">
          <option value="all">All</option>
          <option value="to_do">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </div>
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
      <div class="task-column" v-for="(column, columnIndex) in zPatternTasks" :key="columnIndex">
        <div
          v-for="task in column"
          :key="task.id"
          class="task-card"
        >
        <div class="task-header">
          <h3 class="task-title">{{ task.title }}</h3>
          <div class="task-actions">
            <button @click="editTask(task)" class="edit-btn">Edit</button>
            <button @click="showDeleteConfirmation(task)" class="delete-btn">Delete</button>
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
    </div>
    
    <!-- Create/Edit Task Modal -->
    <div v-if="showCreateModal || editingTask" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h3>{{ editingTask ? 'Edit Task' : 'Create New Task' }}</h3>
        
        <form @submit.prevent="showSaveConfirmation">
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
    
    <!-- Confirmation Dialogs -->
    <ConfirmationDialog
      ref="saveDialog"
      title="Confirm Save Task"
      :message="editingTask ? 'Are you sure you want to save changes to this task?' : 'Are you sure you want to create this task?'"
      :confirmText="editingTask ? 'Save Changes' : 'Create Task'"
      cancelText="Cancel"
      confirmClass="success"
      @confirm="confirmSaveTask"
      @cancel="hideSaveConfirmation"
    />
    
    <ConfirmationDialog
      ref="deleteDialog"
      title="Confirm Delete Task"
      message="Are you sure you want to delete this task? This action cannot be undone."
      confirmText="Delete"
      cancelText="Cancel"
      confirmClass="danger"
      @confirm="confirmDeleteTask"
      @cancel="hideDeleteConfirmation"
    />

    <!-- Floating Input Prompt Bar -->
    <div class="input-prompt-container">
      <div class="input-prompt-bar" :class="{ 'loading': isPromptLoading }">
        <input 
          type="text" 
          v-model="promptInput" 
          placeholder="Ask AI to help..." 
          :disabled="isPromptLoading"
          @keyup.enter="handlePromptSubmit"
        />
        <button class="send-btn" @click="handlePromptSubmit" v-if="promptInput && !isPromptLoading">
          <span class="arrow-icon">↑</span>
        </button>
        <div class="loading-spinner" v-if="isPromptLoading"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useTasksStore } from '../stores/tasks'
import { useAuthStore } from '../stores/auth'
import ConfirmationDialog from './ConfirmationDialog.vue'

export default {
  name: 'TaskGrid',
  components: {
    ConfirmationDialog
  },
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
    
    // Status filter state
    const statusFilter = ref('all')
    
    // Time order filter state
    const timeOrderFilter = ref('newest')

    // Prompt input state
    const promptInput = ref('')
    const isPromptLoading = ref(false)
    
    // Confirmation dialog refs
    const saveDialog = ref(null)
    const deleteDialog = ref(null)
    const taskToDelete = ref(null)
    
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
    
    const tasks = computed(() => {
      return [...tasksStore.tasks].sort((a, b) => {
        if (timeOrderFilter.value === 'oldest') {
          return new Date(a.created_at) - new Date(b.created_at)
        } else {
          return new Date(b.created_at) - new Date(a.created_at)
        }
      })
    })
    
    // Filtered tasks based on status filter
    const filteredTasks = computed(() => {
      if (statusFilter.value === 'all') {
        return tasks.value
      }
      
      return tasks.value.filter(task => {
        const taskStatus = getStatusClass(task)
        return taskStatus === statusFilter.value
      })
    })
    
    // Z-pattern layout: distribute tasks across columns in Z-order
    const zPatternTasks = computed(() => {
      const columns = 3
      const result = [[], [], []]
      
      filteredTasks.value.forEach((task, index) => {
        const columnIndex = index % columns
        result[columnIndex].push(task)
      })
      
      return result
    })
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
            'DONE': 'done'
          }
          return statusClassMap[task.status_id] || 'to_do'
        } else if (task.status_id.status) {
          // Nested status object with display text like "To Do"
          const statusClassMap = {
            'To Do': 'to_do',
            'In Progress': 'in_progress',
            'Done': 'done'
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
            'Done': 'done'
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
    
    // Confirmation dialog methods
    const showSaveConfirmation = () => {
      saveDialog.value?.open()
    }
    
    const hideSaveConfirmation = () => {
      saveDialog.value?.close()
    }
    
    const confirmSaveTask = async () => {
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
      hideSaveConfirmation()
      closeModal()
    }
    
    const showDeleteConfirmation = (task) => {
      taskToDelete.value = task
      deleteDialog.value?.open()
    }
    
    const hideDeleteConfirmation = () => {
      deleteDialog.value?.close()
      taskToDelete.value = null
    }
    
    const confirmDeleteTask = async () => {
      if (taskToDelete.value) {
        await tasksStore.deleteTask(taskToDelete.value.task_id)
        hideDeleteConfirmation()
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

    const handlePromptSubmit = () => {
      if (!promptInput.value.trim() || isPromptLoading.value) return
      
      console.log('Prompt submitted:', promptInput.value)
      isPromptLoading.value = true
      
      // Simulate loading
      setTimeout(() => {
        isPromptLoading.value = false
        promptInput.value = ''
      }, 5000)
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
      filteredTasks,
      zPatternTasks,
      loading,
      error,
      statusFilter,
      timeOrderFilter,
      promptInput,
      isPromptLoading,
      showCreateModal,
      editingTask,
      taskForm,
      saveDialog,
      deleteDialog,
      formatDate,
      getStatusDisplay,
      getStatusClass,
      editTask,
      closeModal,
      saveTask,
      deleteTask,
      handlePromptSubmit,
      showSaveConfirmation,
      hideSaveConfirmation,
      confirmSaveTask,
      showDeleteConfirmation,
      hideDeleteConfirmation,
      confirmDeleteTask
    }
  }
}
</script>

<style scoped>
.task-grid-container {
  padding: 2rem;
  width: 100%;
  box-sizing: border-box;
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

/* Filters Container */
.filters-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

/* Time Order Filter Styles */
.time-order-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-align: left;
}

.time-order-filter label {
  color: #333;
  font-weight: 500;
  font-size: 1rem;
}

/* Status Filter Styles */
.status-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-align: left;
}

.status-filter label {
  color: #333;
  font-weight: 500;
  font-size: 1rem;
}

.filter-dropdown {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  color: #333;
  font-size: 1rem;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
  min-width: 120px;
}

.filter-dropdown:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.filter-dropdown:hover {
  border-color: #999;
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

/* Z-pattern layout using flexbox */
.task-grid {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-start;
  align-items: flex-start;
}

/* Individual columns for Z-pattern */
.task-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 0;
}

.task-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
  width: 100%;
  box-sizing: border-box;
  min-width: 0;
}

@media (max-width: 1024px) {
  .task-grid {
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .task-grid {
    flex-direction: column;
    gap: 1rem;
  }
}

.task-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  width: 100%;
}

.task-title {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
  flex: 1;
  margin-right: 1rem;
  text-align: left;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  min-width: 0;
  overflow: hidden;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
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
  text-align: left;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  width: 100%;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.task-footer span {
  text-align: left;
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

.task-status.done {
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

/* Floating Input Prompt Bar */
.input-prompt-container {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  width: 100%;
  max-width: 600px;
  padding: 0 20px;
  box-sizing: border-box;
}

/* Define the custom property for rotation */
@property --gradient-angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.input-prompt-bar {
  background: white;
  border-radius: 50px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 8px 16px;
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  transition: box-shadow 0.2s, border-color 0.2s;
  position: relative;
  /* z-index must be auto to allow negative z-index children to go behind background */
  z-index: auto; 
}

.input-prompt-bar.loading {
  background: white;
  border-color: transparent;
  box-shadow: none;
}

.input-prompt-bar.loading::before {
  content: '';
  position: absolute;
  z-index: -1;
  inset: -2px;
  border-radius: 52px;
  background: conic-gradient(
    from var(--gradient-angle),
    #B07CFF,
    #62B6FF,
    #B07CFF
  );
  animation: rotation 2s linear infinite;
}

.input-prompt-bar.loading::after {
  content: '';
  position: absolute;
  z-index: -2;
  inset: -4px;
  border-radius: 54px;
  background: conic-gradient(
    from var(--gradient-angle),
    #B07CFF,
    #62B6FF,
    #B07CFF
  );
  filter: blur(10px);
  opacity: 0.6;
  animation: rotation 2s linear infinite;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top-color: #7A56C9;
  border-right-color: #7A56C9;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-left: 8px;
  flex-shrink: 0;
}

@keyframes rotation {
  0% { --gradient-angle: 0deg; }
  100% { --gradient-angle: 360deg; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.input-prompt-bar:focus-within {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  border-color: #007bff;
}

.input-prompt-bar.loading:focus-within {
  box-shadow: none;
  border-color: transparent;
}

.input-prompt-bar input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 1rem;
  padding: 8px;
  background: transparent;
  flex: 1;
  color: black;
  transition: color 0.2s, opacity 0.2s;
}

.input-prompt-bar.loading input {
  color: #666;
  opacity: 0.75;
}

.send-btn {
  background: #007bff;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-left: 8px;
  flex-shrink: 0;
  transition: background-color 0.2s;
}

.send-btn:hover {
  background: #0056b3;
}

.arrow-icon {
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  line-height: 1;
}
</style>