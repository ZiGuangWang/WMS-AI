<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">库存调整</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button type="primary" @click="handleAdd">
          <template #icon><icon-plus /></template>
          新增调整单
        </a-button>
        <a-button @click="handleExport">
          <template #icon><icon-download /></template>
          导出调整记录
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="操作类型">
          <a-select v-model="listQuery.type" placeholder="全部类型" allow-clear style="width: 150px">
            <a-option label="入库" value="入库" />
            <a-option label="出库" value="出库" />
            <a-option label="调整" value="调整" />
          </a-select>
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
          <a-table-column title="货品信息" :min-width="200">
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
          <a-table-column title="单据号" data-index="order_no" :width="180" align="center">
            <template #cell="{ record }">
              <span class="order-no">{{ record.order_no }}</span>
            </template>
          </a-table-column>
          <a-table-column title="批次号" data-index="batch_no" :width="150" align="center" />
          <a-table-column title="类型" :width="100" align="center">
            <template #cell="{ record }">
              <a-tag :color="getTypeTagColor(record.type)" bordered>{{ record.type }}</a-tag>
            </template>
          </a-table-column>
          <a-table-column title="库位" data-index="location_code" :width="120" align="center" />
          <a-table-column title="变动数量" :width="120" align="center">
            <template #cell="{ record }">
              <span :class="['change-quantity', record.change_quantity > 0 ? 'text-success' : 'text-danger']">
                {{ record.change_quantity > 0 ? '+' : '' }}{{ record.change_quantity }}
              </span>
            </template>
          </a-table-column>
          <a-table-column title="余量" data-index="after_quantity" :width="100" align="center" />
          <a-table-column title="时间" :width="180" align="center">
            <template #cell="{ record }">
              {{ formatTime(record.created_at) }}
            </template>
          </a-table-column>
          <a-table-column title="备注" data-index="remark" :min-width="150" ellipsis tooltip />
        </template>
      </a-table>
    </a-card>

    <!-- 调整弹窗 -->
    <a-modal
      :visible="dialogVisible"
      title="新增库存调整"
      @cancel="dialogVisible = false"
      @before-ok="confirmAdjust"
      width="550px"
    >
      <a-form ref="dataFormRef" :model="temp" :rules="rules" auto-label-width>
        <a-form-item label="货品" field="goods_id">
          <a-select v-model="temp.goods_id" allow-search placeholder="选择货品" style="width: 100%">
            <a-option v-for="item in goodsOptions" :key="item._id" :label="`${item.name} (${item.sku})`" :value="item._id" />
          </a-select>
        </a-form-item>
        <a-form-item label="库位" field="location_id">
          <a-select v-model="temp.location_id" allow-search placeholder="选择库位" style="width: 100%">
            <a-option v-for="loc in locationOptions" :key="loc._id" :label="loc.code" :value="loc._id" />
          </a-select>
        </a-form-item>
        <a-form-item label="调整数量" field="adjust_quantity">
          <a-input-number v-model="temp.adjust_quantity" placeholder="正数为增，负数为减" style="width: 100%" />
        </a-form-item>
        <a-form-item label="原因/备注" field="remark">
          <a-textarea v-model="temp.remark" :rows="3" placeholder="请输入调整原因" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { getInventoryLogs, adjustInventory } from '@/api/inventory'
import { getGoodsList, getLocationList } from '@/api/basic'
import { Message } from '@arco-design/web-vue'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  type: undefined
})

const pagination = computed(() => ({
  total: total.value,
  current: listQuery.page,
  pageSize: listQuery.limit,
  showTotal: true,
  showPageSize: true
}))

const goodsOptions = ref<any[]>([])
const locationOptions = ref<any[]>([])
const dialogVisible = ref(false)
const dataFormRef = ref()
const temp = reactive({
  goods_id: '',
  location_id: '',
  adjust_quantity: 0,
  remark: ''
})

const rules = {
  goods_id: [{ required: true, message: '请选择货品' }],
  location_id: [{ required: true, message: '请选择库位' }],
  adjust_quantity: [{ required: true, message: '请输入调整数量' }]
}

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getInventoryLogs({
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

const loadOptions = async () => {
  try {
    const [goods, locations]: any = await Promise.all([
      getGoodsList({ limit: 1000 }),
      getLocationList({ limit: 1000 })
    ])
    goodsOptions.value = goods
    locationOptions.value = locations
  } catch (error) {
    console.error(error)
  }
}

const handleFilter = () => {
  listQuery.page = 1
  getList()
}

const resetQuery = () => {
  listQuery.type = undefined
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

const handleAdd = () => {
  temp.goods_id = ''
  temp.location_id = ''
  temp.adjust_quantity = 0
  temp.remark = ''
  dialogVisible.value = true
}

const confirmAdjust = async () => {
  const errors = await dataFormRef.value?.validate()
  if (!errors) {
    try {
      await adjustInventory(temp)
      Message.success('调整成功')
      dialogVisible.value = false
      getList()
      return true
    } catch (error) {
      console.error(error)
      return false
    }
  }
  return false
}

const handleExport = () => {
  Message.info('导出功能开发中...')
}

const getTypeTagColor = (type: string) => {
  const map: any = {
    '入库': 'green',
    '出库': 'orange',
    '调整': 'arcoblue'
  }
  return map[type] || 'gray'
}

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString()
}

onMounted(() => {
  getList()
  loadOptions()
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

.order-no {
  color: #86909c;
  font-size: 13px;
}

.change-quantity {
  font-weight: bold;
  &.text-success {
    color: #00b42a;
  }
  &.text-danger {
    color: #f53f3f;
  }
}
</style>
