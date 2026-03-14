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
      },
      {
        path: 'inbound/order',
        name: 'InboundOrder',
        component: () => import('../views/inbound/order/index.vue'),
        meta: { title: '入库单管理' }
      },
      {
        path: 'inbound/check',
        name: 'InboundCheck',
        component: () => import('../views/inbound/check/index.vue'),
        meta: { title: '货物验收' }
      },
      {
        path: 'outbound/order',
        name: 'OutboundOrder',
        component: () => import('../views/outbound/order/index.vue'),
        meta: { title: '出库单管理' }
      },
      {
        path: 'outbound/review',
        name: 'OutboundReview',
        component: () => import('../views/outbound/review/index.vue'),
        meta: { title: '货物复核' }
      },
      {
        path: 'inventory/query',
        name: 'InventoryQuery',
        component: () => import('../views/inventory/query/index.vue'),
        meta: { title: '实时库存查询' }
      },
      {
        path: 'inventory/warning',
        name: 'InventoryWarning',
        component: () => import('../views/inventory/warning/index.vue'),
        meta: { title: '库存预警' }
      },
      {
        path: 'inventory/adjust',
        name: 'InventoryAdjust',
        component: () => import('../views/inventory/adjust/index.vue'),
        meta: { title: '库存调整' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
