import axios from 'axios'
import { Message } from '@arco-design/web-vue'

const service = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API || '/api/v1',
  timeout: 5000
})

// Request interceptor
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
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
    
    if (error.response) {
      if (error.response.status === 401 && window.location.pathname !== '/login') {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
      if (error.response.data && error.response.data.detail) {
        message = error.response.data.detail
      }
    }
    
    Message.error({
      content: message,
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
