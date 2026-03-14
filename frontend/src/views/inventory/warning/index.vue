<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">库存预警</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button status="danger" @click="handleExport">
          <template #icon><icon-exclamation-circle /></template>
          导出预警列表
        </a-button>
        <a-button @click="getList">
          <template #icon><icon-refresh /></template>
          刷新数据
        </a-button>
      </a-space>
    </a-card>

    <a-card class="table-card" :bordered="false">
      <a-table
        :loading="listLoading"
        :data="list"
        :pagination="false"
        row-key="sku"
      >
        <template #columns>
          <a-table-column title="货品信息" :min-width="220">
            <template #cell="{ record }">
              <div class="goods-info-cell">
                <div class="goods-icon warning">{{ record.goods_name.charAt(0) }}</div>
                <div class="goods-detail">
                  <div class="name">{{ record.goods_name }}</div>
                  <div class="sku">{{ record.sku }}</div>
                </div>
              </div>
            </template>
          </a-table-column>
          <a-table-column title="当前库存" :width="120" align="center">
            <template #cell="{ record }">
              <span class="quantity-text danger">{{ record.current_stock }}</span>
            </template>
          </a-table-column>
          <a-table-column title="安全库存" data-index="min_stock" :width="120" align="center" />
          <a-table-column title="状态" align="center" :width="120">
            <template #cell="{ record }">
              <a-tag color="red" bordered>{{ record.status }}</a-tag>
            </template>
          </a-table-column>
          <a-table-column title="操作" align="center" :width="150" fixed="right">
            <template #cell="{ record }">
              <a-button type="text" size="small" @click="handleRestock(record)">
                <template #icon><icon-shopping-cart /></template>
                去补货
              </a-button>
            </template>
          </a-table-column>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getInventoryWarning } from '@/api/inventory'
import { useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'

const router = useRouter()
const list = ref([])
const listLoading = ref(true)

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getInventoryWarning()
    list.value = response
  } catch (error) {
    console.error(error)
  } finally {
    listLoading.value = false
  }
}

const handleRestock = (row: any) => {
  router.push('/inbound/order')
}

const handleExport = () => {
  Message.info('导出功能开发中...')
}

onMounted(() => {
  getList()
})
</script>

<style scoped lang="scss">
.header-section {
  margin-bottom: 24px;
  .page-title {
    font-size: 24px;
    font-weight: bold;
    color: #1d2129;
    margin: 0;
  }
}

.action-card {
  margin-bottom: 16px;
}

.table-card {
  background-color: #fff;
}

.goods-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  .goods-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    font-weight: bold;
    font-size: 16px;
    &.warning {
      background-color: #fff5f5;
      color: #f53f3f;
    }
  }
  .goods-detail {
    .name {
      font-weight: 500;
      color: #1d2129;
      margin-bottom: 2px;
    }
    .sku {
      font-size: 12px;
      color: #86909c;
    }
  }
}

.quantity-text {
  font-weight: bold;
  font-size: 16px;
  &.danger {
    color: #f53f3f;
  }
}
</style>
