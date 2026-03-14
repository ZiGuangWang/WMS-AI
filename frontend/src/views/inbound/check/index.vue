<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">入库验收</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button @click="handleExport">
          <template #icon><icon-download /></template>
          导出验收单
        </a-button>
        <a-button @click="handlePrint">
          <template #icon><icon-printer /></template>
          打印入库单
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="入库单号">
          <a-input v-model="listQuery.order_no" placeholder="输入入库单号" allow-clear @keyup.enter="handleFilter" />
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
          <a-table-column title="入库单号" data-index="order_no" :width="180">
            <template #cell="{ record }">
              <span class="order-no">{{ record.order_no }}</span>
            </template>
          </a-table-column>
          <a-table-column title="类型" data-index="type" :width="120" align="center" />
          <a-table-column title="供应商" data-index="supplier_name" :min-width="150" />
          <a-table-column title="状态" align="center" :width="120">
            <template #cell="{ record }">
              <a-tag :color="getStatusColor(record.status)" bordered>
                {{ getStatusLabel(record.status) }}
              </a-tag>
            </template>
          </a-table-column>
          <a-table-column title="操作" align="center" :width="220" fixed="right">
            <template #cell="{ record }">
              <a-space>
                <a-button v-if="record.status === 2" type="text" size="small" @click="handleCheck(record)">
                  <template #icon><icon-archive /></template>
                  验收货物
                </a-button>
                <a-button v-if="record.status === 3" type="text" status="success" size="small" @click="handleShelve(record)">
                  <template #icon><icon-send /></template>
                  确认上架
                </a-button>
                <a-button type="text" size="small" @click="handleDetail(record)">
                  <template #icon><icon-eye /></template>
                  详情
                </a-button>
              </a-space>
            </template>
          </a-table-column>
        </template>
      </a-table>
    </a-card>

    <!-- 验收弹窗 -->
    <a-modal
      :visible="checkDialogVisible"
      title="货物验收"
      @cancel="checkDialogVisible = false"
      @before-ok="confirmCheck"
      width="850px"
    >
      <div class="dialog-inner-content">
        <a-descriptions title="单据信息" :column="2" border>
          <a-descriptions-item label="入库单号">
            <span class="info-text">{{ temp.order_no }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="供应商">
            <span class="info-text">{{ temp.supplier_name }}</span>
          </a-descriptions-item>
        </a-descriptions>
        
        <div class="detail-section">
          <div class="section-title">货品验收明细</div>
          <a-table :data="temp.items" :pagination="false" :bordered="true">
            <template #columns>
              <a-table-column title="货品名称" data-index="goods_name" :min-width="150" />
              <a-table-column title="SKU" data-index="sku" :width="120" align="center" />
              <a-table-column title="计划数量" data-index="planned_quantity" :width="100" align="center">
                <template #cell="{ record }">
                  <span class="quantity-text">{{ record.planned_quantity }}</span>
                </template>
              </a-table-column>
              <a-table-column title="实收数量" :width="150" align="center">
                <template #cell="{ record }">
                  <a-input-number v-model="record.received_quantity" :min="0" :max="record.planned_quantity" size="small" />
                </template>
              </a-table-column>
            </template>
          </a-table>
        </div>
      </div>
    </a-modal>

    <!-- 上架弹窗 -->
    <a-modal
      :visible="shelveDialogVisible"
      title="货物上架"
      @cancel="shelveDialogVisible = false"
      @before-ok="confirmShelve"
      width="950px"
    >
      <div class="dialog-inner-content">
        <a-descriptions title="单据信息" :column="2" border>
          <a-descriptions-item label="入库单号">
            <span class="info-text">{{ temp.order_no }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="供应商">
            <span class="info-text">{{ temp.supplier_name }}</span>
          </a-descriptions-item>
        </a-descriptions>
        
        <div class="detail-section">
          <div class="section-title">货品上架明细</div>
          <a-table :data="temp.items" :pagination="false" :bordered="true">
            <template #columns>
              <a-table-column title="货品名称" data-index="goods_name" :min-width="150" />
              <a-table-column title="SKU" data-index="sku" :width="120" align="center" />
              <a-table-column title="实收数量" data-index="received_quantity" :width="100" align="center">
                <template #cell="{ record }">
                  <span class="quantity-text">{{ record.received_quantity }}</span>
                </template>
              </a-table-column>
              <a-table-column title="上架库位" :width="220" align="center">
                <template #cell="{ record, rowIndex }">
                  <a-select 
                    v-model="record.location_id" 
                    placeholder="选择库位" 
                    allow-search
                    @change="(val) => handleLocationChange(val as string, rowIndex)" 
                    style="width: 100%"
                  >
                    <a-option v-for="loc in locationOptions" :key="loc._id" :label="loc.code" :value="loc._id" />
                  </a-select>
                </template>
              </a-table-column>
            </template>
          </a-table>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { getInboundOrderList, checkInboundGoods, shelveInboundGoods } from '@/api/inbound'
import { getLocationList } from '@/api/basic'
import { Message } from '@arco-design/web-vue'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  order_no: undefined,
  status: 2 // 默认查询待验收
})

const pagination = computed(() => ({
  total: total.value,
  current: listQuery.page,
  pageSize: listQuery.limit,
  showTotal: true,
  showPageSize: true
}))

const locationOptions = ref<any[]>([])
const checkDialogVisible = ref(false)
const shelveDialogVisible = ref(false)
const temp = reactive({
  _id: undefined,
  order_no: '',
  supplier_name: '',
  items: [] as any[]
})

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getInboundOrderList({
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

const loadLocations = async () => {
  try {
    const response: any = await getLocationList({ limit: 1000 })
    locationOptions.value = response
  } catch (error) {
    console.error(error)
  }
}

const handleFilter = () => {
  listQuery.page = 1
  getList()
}

const resetQuery = () => {
  listQuery.order_no = undefined
  listQuery.status = 2
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

const handleCheck = (row: any) => {
  Object.assign(temp, JSON.parse(JSON.stringify(row)))
  // 初始化实收数量
  temp.items.forEach((item: any) => {
    if (!item.received_quantity) {
      item.received_quantity = item.planned_quantity
    }
  })
  checkDialogVisible.value = true
}

const confirmCheck = async () => {
  try {
    await checkInboundGoods(temp._id, { items: temp.items })
    Message.success('验收完成')
    checkDialogVisible.value = false
    getList()
    return true
  } catch (error) {
    console.error(error)
    return false
  }
}

const handleShelve = (row: any) => {
  Object.assign(temp, JSON.parse(JSON.stringify(row)))
  shelveDialogVisible.value = true
  loadLocations()
}

const handleLocationChange = (val: string, index: number) => {
  const loc = locationOptions.value.find(l => l._id === val)
  if (loc) {
    temp.items[index].location_code = loc.code
  }
}

const confirmShelve = async () => {
  const hasNoLocation = temp.items.some((item: any) => !item.location_id)
  if (hasNoLocation) {
    Message.warning('请为所有货品选择上架库位')
    return false
  }

  try {
    await shelveInboundGoods(temp._id, { items: temp.items })
    Message.success('上架完成')
    shelveDialogVisible.value = false
    getList()
    return true
  } catch (error) {
    console.error(error)
    return false
  }
}

const handleDetail = (row: any) => {
  Message.info('详情查看功能开发中...')
}

const handleExport = () => {
  Message.info('导出功能开发中...')
}

const handlePrint = () => {
  Message.info('打印功能开发中...')
}

const getStatusColor = (status: number) => {
  const map: any = {
    1: 'orange',
    2: 'arcoblue',
    3: 'cyan',
    4: 'green',
    0: 'gray'
  }
  return map[status] || 'gray'
}

const getStatusLabel = (status: number) => {
  const map: any = {
    1: '待审核',
    2: '待验收',
    3: '待上架',
    4: '已完成',
    0: '已取消'
  }
  return map[status] || '未知'
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

.order-no {
  color: #165dff;
  font-weight: 500;
}

.info-text {
  color: #1d2129;
  font-weight: 500;
}

.detail-section {
  margin-top: 24px;
  .section-title {
    font-size: 16px;
    font-weight: bold;
    color: #1d2129;
    margin-bottom: 16px;
    padding-left: 8px;
    border-left: 4px solid #165dff;
  }
}

.quantity-text {
  font-weight: bold;
  color: #165dff;
}
</style>
