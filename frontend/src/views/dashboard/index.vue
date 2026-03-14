<template>
  <div class="dashboard-container">
    <div class="welcome-section">
      <h1 class="page-title">工作台</h1>
      <p class="subtitle">欢迎回到仓储管理系统，这是您的工作中心</p>
    </div>

    <!-- 数据概览 -->
    <a-row :gutter="24" class="stat-row">
      <a-col :span="6">
        <a-card :bordered="false" class="stat-card">
          <div class="stat-header">
            <span class="label">今日入库单</span>
            <div class="icon-wrapper blue">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" style="width: 20px; height: 20px;">
                <path d="M7.43433 15.8921L24 25.4621L40.5657 15.8921V32.1079L24 41.6779L7.43433 32.1079V15.8921Z" />
                <path d="M24 25.4621V41.6779" />
                <path d="M7.43433 15.8921L24 6.32214L40.5657 15.8921L24 25.4621L7.43433 15.8921Z" />
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats.today_inbound.value }}</div>
          <div class="stat-footer">
            <span :class="['trend', stats.today_inbound.status]" :style="{ visibility: stats.today_inbound.trend === 0 ? 'hidden' : 'visible' }">
              <icon-caret-up v-if="stats.today_inbound.status === 'up'" />
              <icon-caret-down v-if="stats.today_inbound.status === 'down'" />
              {{ stats.today_inbound.trend > 0 ? '+' : '' }}{{ stats.today_inbound.trend }}%
            </span>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card :bordered="false" class="stat-card">
          <div class="stat-header">
            <span class="label">今日出库单</span>
            <div class="icon-wrapper blue">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" style="width: 20px; height: 20px;">
                <path d="M7.43433 15.8921L24 25.4621L40.5657 15.8921V32.1079L24 41.6779L7.43433 32.1079V15.8921Z" />
                <path d="M24 25.4621V41.6779" />
                <path d="M7.43433 15.8921L24 6.32214L40.5657 15.8921L24 25.4621L7.43433 15.8921Z" />
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats.today_outbound.value }}</div>
          <div class="stat-footer">
            <span :class="['trend', stats.today_outbound.status]" :style="{ visibility: stats.today_outbound.trend === 0 ? 'hidden' : 'visible' }">
              <icon-caret-up v-if="stats.today_outbound.status === 'up'" />
              <icon-caret-down v-if="stats.today_outbound.status === 'down'" />
              {{ stats.today_outbound.trend > 0 ? '+' : '' }}{{ stats.today_outbound.trend }}%
            </span>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card :bordered="false" class="stat-card">
          <div class="stat-header">
            <span class="label">当前库存总量</span>
            <div class="icon-wrapper blue">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" style="width: 20px; height: 20px;">
                <path d="M7.43433 15.8921L24 25.4621L40.5657 15.8921V32.1079L24 41.6779L7.43433 32.1079V15.8921Z" />
                <path d="M24 25.4621V41.6779" />
                <path d="M7.43433 15.8921L24 6.32214L40.5657 15.8921L24 25.4621L7.43433 15.8921Z" />
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ stats.inventory_total.value }}</div>
          <div class="stat-footer">
            <span :class="['trend', stats.inventory_total.status]" :style="{ visibility: stats.inventory_total.trend === 0 ? 'hidden' : 'visible' }">
              <icon-caret-up v-if="stats.inventory_total.status === 'up'" />
              <icon-caret-down v-if="stats.inventory_total.status === 'down'" />
              {{ stats.inventory_total.trend > 0 ? '+' : '' }}{{ stats.inventory_total.trend }}%
            </span>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card :bordered="false" class="stat-card warning">
          <div class="stat-header">
            <span class="label">库存预警数量</span>
            <div class="icon-wrapper orange"><icon-exclamation-circle-fill /></div>
          </div>
          <div class="stat-value">{{ stats.warning_count.value }}</div>
          <div class="stat-footer">
            <span :class="['trend', stats.warning_count.status]" :style="{ visibility: stats.warning_count.trend === 0 ? 'hidden' : 'visible' }">
              <icon-caret-up v-if="stats.warning_count.status === 'up'" />
              <icon-caret-down v-if="stats.warning_count.status === 'down'" />
              {{ stats.warning_count.trend > 0 ? '+' : '' }}{{ stats.warning_count.trend }}%
            </span>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 快捷操作 -->
    <div class="section-container">
      <h2 class="section-title">快捷操作</h2>
      <a-row :gutter="20">
        <a-col :span="6">
          <div class="quick-btn blue" @click="router.push('/inbound/order')">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" style="width: 24px; height: 24px; margin-bottom: 8px;">
              <path d="M24 44L7.43433 34.4378V15.3444L24 5.78223L40.5657 15.3444V34.4378L24 44Z" />
              <path d="M24 24.8911V44" />
              <path d="M7.43433 15.3444L24 24.8911L40.5657 15.3444" />
              <path d="M24 5.78223L7.43433 15.3444" />
              <path d="M40.5657 15.3444L24 5.78223" />
              <path d="M16 28L24 23L32 28" stroke-width="4" />
            </svg>
            <span>创建入库单</span>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="quick-btn green" @click="router.push('/outbound/order')">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" style="width: 24px; height: 24px; margin-bottom: 8px;">
              <path d="M24 44L7.43433 34.4378V15.3444L24 5.78223L40.5657 15.3444V34.4378L24 44Z" />
              <path d="M24 24.8911V44" />
              <path d="M7.43433 15.3444L24 24.8911L40.5657 15.3444" />
              <path d="M24 5.78223L7.43433 15.3444" />
              <path d="M40.5657 15.3444L24 5.78223" />
              <path d="M32 23L24 28L16 23" stroke-width="4" />
            </svg>
            <span>创建出库单</span>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="quick-btn purple" @click="router.push('/inventory/query')">
            <icon-search :size="24" />
            <span>库存查询</span>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="quick-btn orange" @click="handleImport">
            <icon-upload :size="24" />
            <span>货品导入</span>
          </div>
        </a-col>
      </a-row>
    </div>

    <!-- 库存预警 -->
    <div class="section-container warning-section">
      <div class="section-header">
        <h2 class="section-title">
          <icon-exclamation-circle style="color: #ff7d00; margin-right: 8px" />
          库存预警
        </h2>
        <a-button type="text" @click="router.push('/inventory/warning')">
          查看全部 <icon-right />
        </a-button>
      </div>
      
      <div class="warning-list">
        <div v-for="(item, index) in warningList" :key="index" class="warning-item">
          <div class="warning-info">
            <div class="name">{{ item.goods_name }}</div>
            <div class="detail">库存不足：当前 {{ item.current_stock }} 件，安全库存 {{ item.min_stock }} 件</div>
          </div>
          <a-button type="text" @click="router.push('/inventory/adjust')">
            <template #icon><icon-edit /></template>
            调整
          </a-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { getStats } from '@/api/dashboard'
import { getInventoryWarning } from '@/api/inventory'
import { Message } from '@arco-design/web-vue'

const router = useRouter()

const stats = reactive({
  today_inbound: { value: 0, trend: 0, status: 'neutral' },
  today_outbound: { value: 0, trend: 0, status: 'neutral' },
  inventory_total: { value: 0, trend: 0, status: 'neutral' },
  warning_count: { value: 0, trend: 0, status: 'neutral' }
})

const warningList = ref<any[]>([])

const loadData = async () => {
  try {
    const statsRes: any = await getStats()
    Object.assign(stats, statsRes)
    
    const warningRes: any = await getInventoryWarning()
    warningList.value = warningRes.slice(0, 2) // Show only 2
  } catch (error) {
    console.error(error)
  }
}

const handleImport = () => {
  Message.info('货品导入功能开发中...')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.dashboard-container {
  padding: 8px;
}

.welcome-section {
  margin-bottom: 32px;
  .page-title {
    font-size: 28px;
    font-weight: bold;
    color: #1d2129;
    margin: 0 0 8px 0;
  }
  .subtitle {
    font-size: 14px;
    color: #86909c;
    margin: 0;
  }
}

.stat-row {
  margin-bottom: 32px;
}

.stat-card {
  border-radius: 8px;
  background-color: #ffffff;
  transition: all 0.3s;
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  :deep(.arco-card-body) {
    padding: 24px;
  }

  .stat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    .label {
      font-size: 14px;
      color: #4e5969;
    }
    .icon-wrapper {
      font-size: 20px;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      &.blue {
        background-color: #e8f3ff;
        color: #165dff;
      }
      &.orange {
        background-color: #fff7e8;
        color: #ff7d00;
      }
    }
  }
  
  .stat-value {
    font-size: 32px;
    font-weight: bold;
    color: #1d2129;
    margin-bottom: 8px;
  }
  
  .stat-footer {
    .trend {
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 4px;
      height: 20px;
      &.up { color: #00b42a; }
      &.down { color: #f53f3f; }
      &.neutral { color: #86909c; }
    }
  }
  
  &.warning {
    border: 1px solid #ff7d00;
  }
}

.section-container {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  border: 1px solid #f2f3f5;
  
  .section-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 20px 0;
    color: #1d2129;
    display: flex;
    align-items: center;
  }
}

.quick-btn {
  height: 100px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    filter: brightness(1.1);
    transform: scale(1.02);
  }

  &.blue { background: linear-gradient(135deg, #165dff 0%, #4e89ff 100%); }
  &.green { background: linear-gradient(135deg, #00b42a 0%, #34d399 100%); }
  &.purple { background: linear-gradient(135deg, #722ed1 0%, #b37feb 100%); }
  &.orange { background: linear-gradient(135deg, #ff7d00 0%, #ffb649 100%); }
  
  span {
    font-size: 14px;
    font-weight: 500;
  }
}

.warning-section {
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    .section-title {
      margin-bottom: 0;
    }
  }
}

.warning-list {
  .warning-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-radius: 6px;
    background-color: #fffaf5;
    margin-bottom: 12px;
    border: 1px solid #ffe4ba;
    
    .warning-info {
      .name {
        font-weight: 600;
        color: #1d2129;
        margin-bottom: 4px;
      }
      .detail {
        font-size: 13px;
        color: #4e5969;
      }
    }
  }
}
</style>
