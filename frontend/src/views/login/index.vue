<template>
  <div class="login-container">
    <a-card :bordered="false" class="login-card">
      <div class="login-header">
        <div class="logo-wrapper">
          <icon-apps :size="48" style="color: #165dff" />
        </div>
        <h2 class="title">智云仓储管理系统</h2>
        <p class="subtitle">WMS-AI Smart Warehouse Solution</p>
      </div>
      
      <a-form :model="loginForm" ref="loginFormRef" class="login-form" layout="vertical" @submit="handleLogin">
        <a-form-item field="username" :rules="[{ required: true, message: '请输入用户名' }]">
          <a-input v-model="loginForm.username" placeholder="用户名" size="large">
            <template #prefix><icon-user /></template>
          </a-input>
        </a-form-item>
        
        <a-form-item field="password" :rules="[{ required: true, message: '请输入密码' }]">
          <a-input-password v-model="loginForm.password" placeholder="密码" size="large">
            <template #prefix><icon-lock /></template>
          </a-input-password>
        </a-form-item>
        
        <div class="form-options">
          <a-checkbox v-model="loginForm.remember">记住密码</a-checkbox>
          <a-link type="primary" :underline="false">忘记密码？</a-link>
        </div>
        
        <a-form-item>
          <a-button
            type="primary"
            class="login-button"
            size="large"
            :loading="loading"
            long
            html-type="submit"
          >
            登录
          </a-button>
        </a-form-item>
      </a-form>
      
      <div class="login-footer">
        <p>© 2026 WMS-AI Pro Warehouse Management</p>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'
import { login } from '@/api/auth'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const handleLogin = async ({ values, errors }: any) => {
  if (errors) return
  
  loading.value = true
  try {
    const res: any = await login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    // 保存 Token
    localStorage.setItem('token', res.access_token)
    localStorage.setItem('username', loginForm.username)
    
    Message.success('登录成功，欢迎回来')
    router.push('/')
  } catch (error: any) {
    console.error(error)
    const errorMsg = error.response?.data?.detail || '登录失败，请检查账号信息'
    Message.error(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f2f3f5;
  background-image: linear-gradient(135deg, #e5e6eb 0%, #f2f3f5 100%);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -10%;
    left: -10%;
    width: 40%;
    height: 40%;
    background: radial-gradient(circle, rgba(22, 93, 255, 0.05) 0%, transparent 70%);
    z-index: 1;
  }
}

.login-card {
  width: 420px;
  background: #ffffff;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
  border-radius: 12px;
  z-index: 10;
  
  :deep(.arco-card-body) {
    padding: 40px;
  }
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
  
  .logo-wrapper {
    margin-bottom: 16px;
    display: flex;
    justify-content: center;
  }
  
  .title {
    font-size: 24px;
    font-weight: 600;
    color: #1d2129;
    margin: 0 0 8px 0;
  }
  
  .subtitle {
    font-size: 14px;
    color: #86909c;
    margin: 0;
  }
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.login-button {
  font-weight: 600;
}

.login-footer {
  margin-top: 40px;
  text-align: center;
  p {
    font-size: 12px;
    color: #86909c;
  }
}
</style>
