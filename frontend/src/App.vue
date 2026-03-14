<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style>
:root {
  --primary-color: #1890ff;
  --success-color: #52c41a;
  --warning-color: #faad14;
  --danger-color: #f5222d;
  --bg-color: #f0f2f5;
}

#app {
  height: 100vh;
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
}

body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: var(--bg-color);
}

.app-container {
  padding: 24px;
}

.el-card {
  border-radius: 4px;
  border: none !important;
  box-shadow: 0 1px 2px 0 rgba(0,0,0,0.03), 0 1px 6px -1px rgba(0,0,0,0.02), 0 2px 4px 0 rgba(0,0,0,0.02) !important;
}

.el-table {
  border-radius: 4px;
}

.el-table th {
  background-color: #fafafa !important;
  color: rgba(0, 0, 0, 0.85);
  font-weight: 600;
}

.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}
</style>
