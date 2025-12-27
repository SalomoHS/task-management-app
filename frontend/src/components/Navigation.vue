<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">
        <router-link to="/dashboard" class="brand-link">
          Task Manager
        </router-link>
      </div>
      
      <div class="nav-menu">
        <div class="nav-user">
          <span class="user-greeting">
            Welcome, {{ user?.username || 'User' }}
          </span>
          <button @click="showLogoutConfirmation" class="logout-btn">
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
  
  <ConfirmationDialog
    ref="logoutDialog"
    title="Confirm Logout"
    message="Are you sure you want to logout?"
    confirmText="Logout"
    cancelText="Cancel"
    confirmClass="danger"
    @confirm="handleLogout"
    @cancel="hideLogoutConfirmation"
  />
</template>

<script>
import { computed, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import ConfirmationDialog from './ConfirmationDialog.vue'

export default {
  name: 'Navigation',
  components: {
    ConfirmationDialog
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const logoutDialog = ref(null)
    
    const user = computed(() => authStore.user)
    
    const showLogoutConfirmation = () => {
      logoutDialog.value?.open()
    }
    
    const hideLogoutConfirmation = () => {
      logoutDialog.value?.close()
    }
    
    const handleLogout = async () => {
      await authStore.logout()
      router.push('/login')
    }
    
    return {
      user,
      logoutDialog,
      showLogoutConfirmation,
      hideLogoutConfirmation,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #343a40;
  color: white;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 2rem;
  box-sizing: border-box;
  height: 60px;
}

.nav-brand .brand-link {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-brand .brand-link:hover {
  color: #f8f9fa;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-greeting {
  color: #f8f9fa;
  font-size: 0.9rem;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.logout-btn:hover {
  background-color: #c82333;
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0.75rem 1rem;
  }
  
  .nav-user {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-end;
  }
  
  .user-greeting {
    font-size: 0.8rem;
  }
}
</style>