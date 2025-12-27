import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),

  getters: {
    isLoggedIn: (state) => !!state.token && state.isAuthenticated
  },

  actions: {
    async login(username, password) {
      try {
        const response = await axios.post(`${API_BASE_URL}/api/users/login`, {
          username,
          password
        })
        
        const { token, user } = response.data
        
        this.token = token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        
        return { success: true }
      } catch (error) {
        console.error('Login error:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || 'Login failed' 
        }
      }
    },

    async logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },

    async initializeAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        
        try {
          // Verify token is still valid by making a test request
          await axios.get(`${API_BASE_URL}/api/users/me`)
          this.isAuthenticated = true
        } catch (error) {
          // Token is invalid, clear it
          this.logout()
        }
      }
    }
  }
})