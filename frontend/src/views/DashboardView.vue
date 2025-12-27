<template>
  <div class="dashboard-view">
    <Navigation />
    <main class="main-content">
      <TaskGrid />
    </main>
  </div>
</template>

<script>
import Navigation from '../components/Navigation.vue'
import TaskGrid from '../components/TaskGrid.vue'

export default {
  name: 'DashboardView',
  components: {
    Navigation,
    TaskGrid
  }
}
</script>

<style scoped>
.dashboard-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.main-content {
  min-height: calc(100vh - 60px);
  width: 100%;
  padding: 60px 0 0 0;
  margin: 0;
  box-sizing: border-box;
}
</style>