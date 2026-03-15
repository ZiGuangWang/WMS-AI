<template>
  <div class="forbidden">
    <div class="card">
      <div class="title">无权限访问</div>
      <div class="desc">当前账号没有访问该页面的权限，请联系管理员调整角色权限。</div>
      <a-button type="primary" @click="goHome">返回可访问页面</a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.replace('/')
}
</script>

<style scoped>
.forbidden {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.card {
  width: 520px;
  max-width: 100%;
  padding: 28px 24px;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #1d2129;
  margin-bottom: 8px;
}

.desc {
  font-size: 14px;
  color: #4e5969;
  margin-bottom: 20px;
  line-height: 22px;
}
</style>
