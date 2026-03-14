<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="aside">
      <div class="logo">
        <el-icon size="24"><Box /></el-icon>
        <span>WMS-AI</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        router
        background-color="#001529"
        text-color="rgba(255, 255, 255, 0.65)"
        active-text-color="#fff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Monitor /></el-icon>
          <span>控制台首页</span>
        </el-menu-item>

        <el-sub-menu index="basic">
          <template #title>
            <el-icon><DataAnalysis /></el-icon>
            <span>基础数据管理</span>
          </template>
          <el-menu-item index="/basic/goods">货品管理</el-menu-item>
          <el-menu-item index="/basic/location">库位管理</el-menu-item>
          <el-menu-item index="/basic/supplier">供应商管理</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="inbound">
          <template #title>
            <el-icon><Download /></el-icon>
            <span>入库管理</span>
          </template>
          <el-menu-item index="/inbound/order">入库单管理</el-menu-item>
          <el-menu-item index="/inbound/check">货物验收</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="outbound">
          <template #title>
            <el-icon><Upload /></el-icon>
            <span>出库管理</span>
          </template>
          <el-menu-item index="/outbound/order">出库单管理</el-menu-item>
          <el-menu-item index="/outbound/review">货物复核</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="inventory">
          <template #title>
            <el-icon><Management /></el-icon>
            <span>库存管理</span>
          </template>
          <el-menu-item index="/inventory/query">实时库存查询</el-menu-item>
          <el-menu-item index="/inventory/warning">库存预警</el-menu-item>
          <el-menu-item index="/inventory/adjust">库存调整</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ route.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              管理员 <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
  router.push('/login')
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
}

.aside {
  background-color: #001529;
  color: #fff;
  box-shadow: 2px 0 6px rgba(0,21,41,.35);
  transition: width 0.3s;
  z-index: 10;
  
  .logo {
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 600;
    color: #fff;
    background-color: #002140;
    gap: 12px;
    letter-spacing: 1px;
  }
}

.el-menu-vertical {
  border-right: none;
  
  :deep(.el-menu-item) {
    &.is-active {
      background-color: #1890ff !important;
    }
  }
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  height: 64px !important;
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  height: 64px;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #f8f8f8;
  }
}

.main {
  background-color: #f0f2f5;
  padding: 24px;
  overflow-y: auto;
}

/* fade-transform */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.5s;
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
