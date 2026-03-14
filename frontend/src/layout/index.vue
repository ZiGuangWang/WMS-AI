<template>
  <a-layout class="layout-container">
    <!-- 侧边栏 -->
    <a-layout-sider
      breakpoint="lg"
      :width="240"
      collapsible
      :collapsed="isCollapse"
      @collapse="onCollapse"
      class="aside"
    >
      <div class="logo">
        <icon-apps :size="28" style="color: #165dff" />
        <span v-show="!isCollapse">智云仓储管理系统</span>
      </div>
      <a-menu
        :selected-keys="[activeMenu]"
        :auto-open-selected="true"
        style="width: 100%"
        @menu-item-click="handleMenuClick"
      >
        <a-menu-item key="/dashboard">
          <template #icon><icon-dashboard /></template>
          工作台
        </a-menu-item>

        <a-sub-menu key="basic">
          <template #icon><icon-common /></template>
          <template #title>基础数据管理</template>
          <a-menu-item key="/basic/goods">货品管理</a-menu-item>
          <a-menu-item key="/basic/location">库位管理</a-menu-item>
          <a-menu-item key="/basic/supplier">供应商管理</a-menu-item>
        </a-sub-menu>

        <a-sub-menu key="inbound">
          <template #icon><icon-import /></template>
          <template #title>入库管理</template>
          <a-menu-item key="/inbound/order">入库单管理</a-menu-item>
          <a-menu-item key="/inbound/check">货物验收</a-menu-item>
        </a-sub-menu>

        <a-sub-menu key="outbound">
          <template #icon><icon-export /></template>
          <template #title>出库管理</template>
          <a-menu-item key="/outbound/order">出库单管理</a-menu-item>
          <a-menu-item key="/outbound/review">货物复核</a-menu-item>
        </a-sub-menu>

        <a-sub-menu key="inventory">
          <template #icon><icon-storage /></template>
          <template #title>库存管理</template>
          <a-menu-item key="/inventory/query">库存查询</a-menu-item>
          <a-menu-item key="/inventory/warning">库存预警</a-menu-item>
          <a-menu-item key="/inventory/adjust">库存调整</a-menu-item>
        </a-sub-menu>
      </a-menu>
    </a-layout-sider>

    <a-layout class="main-container">
      <!-- 顶部导航 -->
      <a-layout-header class="header">
        <div class="header-left">
          <a-breadcrumb>
            <a-breadcrumb-item>控制台首页</a-breadcrumb-item>
            <a-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index">{{ item }}</a-breadcrumb-item>
          </a-breadcrumb>
        </div>
        <div class="header-right">
          <a-space size="large">
            <div class="user-info-display">
              <a-avatar :size="24" style="background-color: #165dff">
                <icon-user />
              </a-avatar>
              <span class="username">系统管理员</span>
            </div>
            <a-button type="text" @click="handleLogout">
              <template #icon><icon-poweroff /></template>
              退出登录
            </a-button>
          </a-space>
        </div>
      </a-layout-header>

      <!-- 页签区域 -->
      <div class="tags-view">
        <a-space wrap>
          <a-tag
            v-for="tag in tags"
            :key="tag.path"
            :closable="tag.path !== '/dashboard'"
            :color="route.path === tag.path ? 'arcoblue' : 'gray'"
            class="tag-item"
            @click="router.push(tag.path)"
            @close="handleCloseTag(tag.path)"
          >
            {{ tag.title }}
          </a-tag>
        </a-space>
      </div>

      <a-layout-content class="main">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isCollapse = ref(false)
const activeMenu = computed(() => route.path)

const breadcrumbs = computed(() => {
  const matched = route.matched.filter(item => item.meta && item.meta.title)
  return matched.map(item => item.meta.title as string)
})

const tags = ref([
  { title: '控制台', path: '/dashboard' }
])

watch(() => route.path, (newPath) => {
  if (!tags.value.find(t => t.path === newPath)) {
    tags.value.push({
      title: (route.meta.title as string) || '新页面',
      path: newPath
    })
  }
}, { immediate: true })

const onCollapse = (val: boolean) => {
  isCollapse.value = val
}

const handleMenuClick = (key: string) => {
  router.push(key)
}

const handleCloseTag = (path: string) => {
  tags.value = tags.value.filter(t => t.path !== path)
  if (route.path === path) {
    router.push(tags.value[tags.value.length - 1].path)
  }
}

const handleLogout = () => {
  router.push('/login')
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
  background-color: #f2f3f5;
}

.aside {
  background-color: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 21, 41, 0.05);
  z-index: 100;
  
  .logo {
    height: 64px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    font-size: 18px;
    font-weight: 600;
    color: #1d2129;
    gap: 12px;
    overflow: hidden;
    white-space: nowrap;
    border-bottom: 1px solid #f2f3f5;
  }
}

.main-container {
  overflow: hidden;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #f2f3f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 64px;
}

.header-right {
  .user-info-display {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #1d2129;
  }
  .username {
    font-weight: 500;
  }
}

.tags-view {
  padding: 6px 16px;
  background-color: #fff;
  border-bottom: 1px solid #f2f3f5;
  .tag-item {
    cursor: pointer;
    user-select: none;
  }
}

.main {
  padding: 16px;
  overflow-y: auto;
}

/* 动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
