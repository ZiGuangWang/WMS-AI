import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/index.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: () => import('../layout/index.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/index.vue'),
        meta: { title: '控制台首页', icon: 'Dashboard' }
      },
      {
        path: 'basic/goods',
        name: 'Goods',
        component: () => import('../views/basic/goods/index.vue'),
        meta: { title: '货品管理' }
      },
      {
        path: 'basic/location',
        name: 'Location',
        component: () => import('../views/basic/location/index.vue'),
        meta: { title: '库位管理' }
      },
      {
        path: 'basic/supplier',
        name: 'Supplier',
        component: () => import('../views/basic/supplier/index.vue'),
        meta: { title: '供应商管理' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
