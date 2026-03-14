<template>
  <a-config-provider update-at-scroll>
    <router-view />
  </a-config-provider>
</template>

<script setup lang="ts">
</script>

<style>
#app {
  height: 100vh;
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #f2f3f5;
}

.app-container {
  padding: 8px;
}

/* 自定义一些全局 Arco 样式覆盖（如有需要） */
.arco-card {
  border-radius: 4px;
}

.arco-table-th {
  background-color: #f8f9fa !important;
  font-weight: 600 !important;
}
</style>
