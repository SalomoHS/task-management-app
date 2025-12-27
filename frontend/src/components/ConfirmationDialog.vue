<template>
  <div v-if="isOpen" class="modal-overlay" @click="handleCancel">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3>{{ title }}</h3>
      </div>
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>
      <div class="modal-actions">
        <button @click="handleCancel" class="cancel-btn">
          {{ cancelText }}
        </button>
        <button @click="handleConfirm" class="confirm-btn" :class="confirmClass">
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ConfirmationDialog',
  props: {
    title: {
      type: String,
      default: 'Confirm Action'
    },
    message: {
      type: String,
      default: 'Are you sure you want to proceed?'
    },
    confirmText: {
      type: String,
      default: 'Confirm'
    },
    cancelText: {
      type: String,
      default: 'Cancel'
    },
    confirmClass: {
      type: String,
      default: ''
    }
  },
  emits: ['confirm', 'cancel'],
  setup(props, { emit }) {
    const isOpen = ref(false)
    
    const open = () => {
      isOpen.value = true
    }
    
    const close = () => {
      isOpen.value = false
    }
    
    const handleConfirm = () => {
      emit('confirm')
      close()
    }
    
    const handleCancel = () => {
      emit('cancel')
      close()
    }
    
    return {
      isOpen,
      open,
      close,
      handleConfirm,
      handleCancel
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
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  margin-bottom: 1rem;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.25rem;
}

.modal-body {
  margin-bottom: 1.5rem;
}

.modal-body p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.cancel-btn, .confirm-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background-color: #5a6268;
}

.confirm-btn {
  background-color: #007bff;
  color: white;
}

.confirm-btn:hover {
  background-color: #0056b3;
}

.confirm-btn.danger {
  background-color: #dc3545;
}

.confirm-btn.danger:hover {
  background-color: #c82333;
}

.confirm-btn.success {
  background-color: #28a745;
}

.confirm-btn.success:hover {
  background-color: #218838;
}
</style>