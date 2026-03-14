<template>
  <div class="dashboard-container">
    <!-- 数据概览 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <template #header>今日入库单</template>
          <div class="stat-value">12</div>
          <div class="stat-footer">较昨日 +2</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <template #header>今日出库单</template>
          <div class="stat-value">8</div>
          <div class="stat-footer">较昨日 -1</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <template #header>库存总量</template>
          <div class="stat-value">2,540</div>
          <div class="stat-footer">健康</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card warning">
          <template #header>库存预警</template>
          <div class="stat-value">5</div>
          <div class="stat-footer">需要及时处理</div>
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
            <el-table-column prop="goodsName" label="货品名称" />
            <el-table-column prop="sku" label="规格型号" />
            <el-table-column prop="currentStock" label="当前库存">
              <template #default="scope">
                <span class="text-danger">{{ scope.row.currentStock }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="minStock" label="安全库存" />
            <el-table-column prop="location" label="建议补货库位" />
            <el-table-column label="操作" width="120">
              <template #default>
                <el-button link type="primary">去补货</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const warningList = ref([
  { goodsName: '不锈钢螺丝', sku: 'M6*20', currentStock: 45, minStock: 100, location: 'A-01-02' },
  { goodsName: '锂电池', sku: '3.7V 2000mAh', currentStock: 12, minStock: 50, location: 'B-02-01' },
  { goodsName: '铝型材', sku: '2020 1000mm', currentStock: 5, minStock: 20, location: 'C-01-05' }
])
</script>

<style scoped lang="scss">
.dashboard-container {
  padding: 0;
}

.stat-card {
  .stat-value {
    font-size: 32px;
    font-weight: bold;
    color: #303133;
    margin: 10px 0;
  }
  .stat-footer {
    font-size: 14px;
    color: #909399;
  }
  &.warning {
    .stat-value {
      color: #f56c6c;
    }
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
