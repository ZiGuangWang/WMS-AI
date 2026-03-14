import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API || '/api/v1',
  timeout: 5000
})

// Request interceptor
service.interceptors.request.use(
  config => {
    // Add token if needed
    return config
  },
  error => {
    console.log(error)
    return Promise.reject(error)
  }
)

// Response interceptor
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.log('err' + error)
    let message = error.message
    if (error.response && error.response.data && error.response.data.detail) {
      message = error.response.data.detail
    }
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
