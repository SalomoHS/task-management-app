<template>
  <div v-if="isOpen" class="modal-overlay" @click="handleClose">
    <div class="modal" :class="type" @click.stop>
      <div class="modal-header">
        <h3 :class="type">{{ title }}</h3>
      </div>
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>
      <div class="modal-actions">
        <button @click="handleClose" class="close-btn" :class="type">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ResponseModal',
  props: {
    title: {
      type: String,
      default: 'Response'
    },
    message: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'success', // 'success' or 'error'
      validator: (value) => ['success', 'error'].includes(value)
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const isOpen = ref(false)
    
    const open = () => {
      isOpen.value = true
    }
    
    const close = () => {
      isOpen.value = false
      emit('close')
    }
    
    const handleClose = () => {
      close()
    }
    
    return {
      isOpen,
      open,
      close,
      handleClose
    }
  }
}
</script>

<style scoped>
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-left: 6px solid transparent; /* The edge */
}

.modal.success {
  border-left-color: #28a745;
}

.modal.error {
  border-left-color: #dc3545;
}

.modal-header {
  margin-bottom: 1rem;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.modal-header h3.success {
  color: #28a745;
}

.modal-header h3.error {
  color: #dc3545;
}

.modal-body {
  margin-bottom: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
  overflow-x: hidden;
}

.modal-body p {
  margin: 0;
  color: #333;
  line-height: 1.5;
  white-space: pre-wrap; /* Preserve line breaks in response */
  word-break: break-word;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
}

.close-btn {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  color: white;
  transition: background-color 0.2s;
}

.close-btn.success {
  background-color: #28a745;
}

.close-btn.success:hover {
  background-color: #218838;
}

.close-btn.error {
  background-color: #dc3545;
}

.close-btn.error:hover {
  background-color: #c82333;
}
</style>
