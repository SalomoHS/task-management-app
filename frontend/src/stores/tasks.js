import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    tasks: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchTasks() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/api/tasks`)
        this.tasks = response.data
      } catch (error) {
        console.error('Error fetching tasks:', error)
        this.error = error.response?.data?.error || 'Failed to fetch tasks'
      } finally {
        this.loading = false
      }
    },

    async createTask(taskData) {
      try {
        const response = await axios.post(`${API_BASE_URL}/api/tasks`, taskData)
        this.tasks.push(response.data)
        return { success: true, task: response.data }
      } catch (error) {
        console.error('Error creating task:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || 'Failed to create task' 
        }
      }
    },

    async updateTask(taskId, taskData) {
      try {
        const response = await axios.put(`${API_BASE_URL}/api/tasks/${taskId}`, taskData)
        const index = this.tasks.findIndex(task => task.task_id === taskId)
        if (index !== -1) {
          this.tasks[index] = response.data
        }
        return { success: true, task: response.data }
      } catch (error) {
        console.error('Error updating task:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || 'Failed to update task' 
        }
      }
    },

    async deleteTask(taskId) {
      try {
        await axios.delete(`${API_BASE_URL}/api/tasks/${taskId}`)
        this.tasks = this.tasks.filter(task => task.task_id !== taskId)
        return { success: true }
      } catch (error) {
        console.error('Error deleting task:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || 'Failed to delete task' 
        }
      }
    }
  }
})