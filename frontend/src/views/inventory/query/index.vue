<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">库存查询</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button @click="handleExport">
          <template #icon><icon-download /></template>
          导出库存报表
        </a-button>
        <a-button @click="getList">
          <template #icon><icon-refresh /></template>
          刷新数据
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="货品名称">
          <a-input v-model="listQuery.goods_name" placeholder="输入货品名称" allow-clear @keyup.enter="handleFilter" />
        </a-form-item>
        <a-form-item label="SKU编码">
          <a-input v-model="listQuery.sku" placeholder="输入SKU编码" allow-clear @keyup.enter="handleFilter" />
        </a-form-item>
        <a-form-item label="库位编码">
          <a-input v-model="listQuery.location_code" placeholder="输入库位编码" allow-clear @keyup.enter="handleFilter" />
        </a-form-item>
        <a-form-item>
          <a-space>
            <a-button type="primary" @click="handleFilter">
              <template #icon><icon-search /></template>
              查询
            </a-button>
            <a-button @click="resetQuery">
              <template #icon><icon-refresh /></template>
              重置
            </a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>

    <a-card class="table-card" :bordered="false">
      <a-table
        :loading="listLoading"
        :data="list"
        :pagination="pagination"
        row-key="_id"
        @page-change="handleCurrentChange"
        @page-size-change="handleSizeChange"
      >
        <template #columns>
          <a-table-column title="货品信息" :min-width="220">
            <template #cell="{ record }">
              <div class="goods-info-cell">
                <div class="goods-icon">{{ record.goods_name.charAt(0) }}</div>
                <div class="goods-detail">
                  <div class="name">{{ record.goods_name }}</div>
                  <div class="sku">{{ record.sku }}</div>
                </div>
              </div>
            </template>
          </a-table-column>
          <a-table-column title="库位编码" data-index="location_code" :width="150" align="center">
            <template #cell="{ record }">
              <a-tag bordered>{{ record.location_code }}</a-tag>
            </template>
          </a-table-column>
          <a-table-column title="当前库存" :width="120" align="center">
            <template #cell="{ record }">
              <span :class="['quantity-text', record.quantity === 0 ? 'text-danger' : 'text-primary']">
                {{ record.quantity }}
              </span>
            </template>
          </a-table-column>
          <a-table-column title="最近更新" :width="180" align="center">
            <template #cell="{ record }">
              {{ formatTime(record.updated_at) }}
            </template>
          </a-table-column>
          <a-table-column title="操作" align="center" :width="120" fixed="right">
            <template #cell="{ record }">
              <a-button type="text" size="small" @click="handleHistory(record)">
                <template #icon><icon-list /></template>
                流水
              </a-button>
            </template>
          </a-table-column>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { getInventoryQuery } from '@/api/inventory'
import { Message } from '@arco-design/web-vue'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  goods_name: undefined,
  sku: undefined,
  location_code: undefined
})

const pagination = computed(() => ({
  total: total.value,
  current: listQuery.page,
  pageSize: listQuery.limit,
  showTotal: true,
  showPageSize: true
}))

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getInventoryQuery({
      ...listQuery,
      skip: (listQuery.page - 1) * listQuery.limit
    })
    list.value = response
    total.value = response.length
  } catch (error) {
    console.error(error)
  } finally {
    listLoading.value = false
  }
}

const handleFilter = () => {
  listQuery.page = 1
  getList()
}

const resetQuery = () => {
  listQuery.goods_name = undefined
  listQuery.sku = undefined
  listQuery.location_code = undefined
  handleFilter()
}

const handleSizeChange = (pageSize: number) => {
  listQuery.limit = pageSize
  getList()
}

const handleCurrentChange = (current: number) => {
  listQuery.page = current
  getList()
}

const handleHistory = (row: any) => {
  Message.info('库存流水查询功能开发中...')
}

const handleExport = () => {
  Message.info('导出功能开发中...')
}

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString()
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

.filter-card {
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
    background-color: #f2f3f5;
    color: #4e5969;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    font-weight: bold;
    font-size: 16px;
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
  font-size: 15px;
  &.text-primary {
    color: #165dff;
  }
  &.text-danger {
    color: #f53f3f;
  }
}
</style>
