import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { getMe } from '@/api/auth'
import { setPermissionCodes, hasPermission } from '@/utils/permission'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/index.vue'),
    meta: { title: '登录', permission: 'wms:auth:login:view' }
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
        meta: { title: '控制台首页', icon: 'Dashboard', permission: 'wms:dashboard:home:view' }
      },
      {
        path: 'basic/goods',
        name: 'Goods',
        component: () => import('../views/basic/goods/index.vue'),
        meta: { title: '货品管理', permission: 'wms:basic:goods:view' }
      },
      {
        path: 'basic/location',
        name: 'Location',
        component: () => import('../views/basic/location/index.vue'),
        meta: { title: '库位管理', permission: 'wms:basic:location:view' }
      },
      {
        path: 'basic/supplier',
        name: 'Supplier',
        component: () => import('../views/basic/supplier/index.vue'),
        meta: { title: '供应商管理', permission: 'wms:basic:supplier:view' }
      },
      {
        path: 'inbound/order',
        name: 'InboundOrder',
        component: () => import('../views/inbound/order/index.vue'),
        meta: { title: '入库单管理', permission: 'wms:inbound:order:view' }
      },
      {
        path: 'inbound/check',
        name: 'InboundCheck',
        component: () => import('../views/inbound/check/index.vue'),
        meta: { title: '货物验收', permission: 'wms:inbound:check:view' }
      },
      {
        path: 'outbound/order',
        name: 'OutboundOrder',
        component: () => import('../views/outbound/order/index.vue'),
        meta: { title: '出库单管理', permission: 'wms:outbound:order:view' }
      },
      {
        path: 'outbound/review',
        name: 'OutboundReview',
        component: () => import('../views/outbound/review/index.vue'),
        meta: { title: '货物复核', permission: 'wms:outbound:review:view' }
      },
      {
        path: 'inventory/query',
        name: 'InventoryQuery',
        component: () => import('../views/inventory/query/index.vue'),
        meta: { title: '实时库存查询', permission: 'wms:inventory:query:view' }
      },
      {
        path: 'inventory/warning',
        name: 'InventoryWarning',
        component: () => import('../views/inventory/warning/index.vue'),
        meta: { title: '库存预警', permission: 'wms:inventory:warning:view' }
      },
      {
        path: 'inventory/adjust',
        name: 'InventoryAdjust',
        component: () => import('../views/inventory/adjust/index.vue'),
        meta: { title: '库存调整', permission: 'wms:inventory:adjust:view' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  if (to.path === '/login') return true
  const token = localStorage.getItem('token')
  if (!token) return '/login'

  const required = (to.meta?.permission as string | undefined) || ''
  if (required && !hasPermission(required)) {
    try {
      const res: any = await getMe()
      setPermissionCodes(res.permissions || [])
    } catch {
      return '/login'
    }
    if (required && !hasPermission(required)) {
      return '/dashboard'
    }
  }

  return true
})

export default router
