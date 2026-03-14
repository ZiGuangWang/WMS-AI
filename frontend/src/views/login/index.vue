<template>
  <div class="login-container">
    <el-card class="login-card shadow-lg">
      <div class="login-header">
        <el-icon size="40" color="#409EFF"><Box /></el-icon>
        <h2>WMS-AI 仓库管理系统</h2>
      </div>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        <div class="form-options">
          <el-checkbox v-model="loginForm.remember">记住密码</el-checkbox>
          <el-link type="primary" :underline="false">忘记密码？</el-link>
        </div>
        <el-form-item>
          <el-button
            type="primary"
            class="login-button"
            size="large"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        // 模拟登录
        setTimeout(() => {
          loading.value = false
          ElMessage.success('登录成功')
          router.push('/')
        }, 1000)
      } catch (error) {
        loading.value = false
        ElMessage.error('登录失败，请检查用户名或密码')
      }
    }
  })
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
  background-image: radial-gradient(#e1e4e8 1px, transparent 1px);
  background-size: 20px 20px;
}

.login-card {
  width: 450px;
  padding: 20px;
  border-radius: 8px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
  h2 {
    margin-top: 15px;
    color: #303133;
    font-weight: 600;
  }
}

.login-form {
  padding: 0 10px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  font-weight: 600;
  letter-spacing: 2px;
  height: 44px;
  background-color: #1890ff;
  border-color: #1890ff;
}
</style>
