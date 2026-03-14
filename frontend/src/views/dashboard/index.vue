<template>
  <div class="dashboard-container">
    <!-- 数据概览 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card primary">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-label">今日入库单</div>
              <div class="stat-value">{{ stats.today_inbound }}</div>
            </div>
            <div class="stat-icon">
              <el-icon size="40"><Download /></el-icon>
            </div>
          </div>
          <div class="stat-footer">
            <span class="trend">较昨日 <el-icon><CaretTop /></el-icon> 2</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card success">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-label">今日出库单</div>
              <div class="stat-value">{{ stats.today_outbound }}</div>
            </div>
            <div class="stat-icon">
              <el-icon size="40"><Upload /></el-icon>
            </div>
          </div>
          <div class="stat-footer">
            <span class="trend">较昨日 <el-icon><CaretBottom /></el-icon> 1</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card info">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-label">库存总量</div>
              <div class="stat-value">{{ stats.inventory_total }}</div>
            </div>
            <div class="stat-icon">
              <el-icon size="40"><Box /></el-icon>
            </div>
          </div>
          <div class="stat-footer">
            <span>实时数据更新</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card danger">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-label">库存预警</div>
              <div class="stat-value">{{ stats.warning_count }}</div>
            </div>
            <div class="stat-icon">
              <el-icon size="40"><Warning /></el-icon>
            </div>
          </div>
          <div class="stat-footer">
            <span>需要及时处理</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷操作 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>快捷操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" size="large" icon="Plus" @click="router.push('/inbound/order')">创建入库单</el-button>
            <el-button type="success" size="large" icon="Minus" @click="router.push('/outbound/order')">创建出库单</el-button>
            <el-button type="warning" size="large" icon="Search" @click="router.push('/inventory/query')">库存查询</el-button>
            <el-button type="danger" size="large" icon="Warning" @click="router.push('/inventory/warning')">预警处理</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 库存预警列表 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>库存预警提示</span>
              <el-button link type="primary">更多</el-button>
            </div>
          </template>
          <el-table :data="warningList" style="width: 100%">
            <el-table-column prop="goods_name" label="货品名称" />
            <el-table-column prop="sku" label="规格型号" />
            <el-table-column prop="current_stock" label="当前库存">
              <template #default="scope">
                <span class="text-danger">{{ scope.row.current_stock }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="min_stock" label="安全库存" />
            <el-table-column label="状态">
              <template #default="scope">
                <el-tag type="danger" size="small">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default>
                <el-button link type="primary" @click="router.push('/inbound/order')">去补货</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { getStats } from '@/api/dashboard'
import { getInventoryWarning } from '@/api/inventory'

const router = useRouter()

const stats = reactive({
  today_inbound: 0,
  today_outbound: 0,
  inventory_total: 0,
  warning_count: 0
})

const warningList = ref<any[]>([])

const loadData = async () => {
  try {
    const statsRes: any = await getStats()
    Object.assign(stats, statsRes)
    
    const warningRes: any = await getInventoryWarning()
    warningList.value = warningRes.slice(0, 5) // Just show top 5
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.dashboard-container {
  padding: 0;
}

.stat-card {
  border: none;
  border-radius: 8px;
  
  .stat-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .stat-label {
    font-size: 14px;
    color: #909399;
    margin-bottom: 8px;
  }
  
  .stat-value {
    font-size: 28px;
    font-weight: bold;
    color: #303133;
  }
  
  .stat-icon {
    opacity: 0.8;
  }
  
  .stat-footer {
    border-top: 1px solid #f0f2f5;
    padding-top: 10px;
    font-size: 13px;
    color: #606266;
    
    .trend {
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
  }
  
  &.primary {
    background: linear-gradient(135deg, #e6f7ff 0%, #ffffff 100%);
    .stat-icon { color: #1890ff; }
    .trend { color: #52c41a; }
  }
  &.success {
    background: linear-gradient(135deg, #f6ffed 0%, #ffffff 100%);
    .stat-icon { color: #52c41a; }
    .trend { color: #f5222d; }
  }
  &.info {
    background: linear-gradient(135deg, #f9f0ff 0%, #ffffff 100%);
    .stat-icon { color: #722ed1; }
  }
  &.danger {
    background: linear-gradient(135deg, #fff1f0 0%, #ffffff 100%);
    .stat-icon { color: #f5222d; }
    .stat-value { color: #f5222d; }
  }
}

.mt-20 {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-actions {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.text-danger {
  color: #f56c6c;
  font-weight: bold;
}
</style>
