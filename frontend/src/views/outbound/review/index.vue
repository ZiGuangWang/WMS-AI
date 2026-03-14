<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">出库复核</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button @click="handleExport">
          <template #icon><icon-download /></template>
          导出
        </a-button>
        <a-button @click="handlePrint">
          <template #icon><icon-printer /></template>
          打印出库单
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="出库单号">
          <a-input v-model="listQuery.order_no" placeholder="输入出库单号" allow-clear @keyup.enter="handleFilter" />
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
          <a-table-column title="出库单号" data-index="order_no" :width="180">
            <template #cell="{ record }">
              <span class="order-no">{{ record.order_no }}</span>
            </template>
          </a-table-column>
          <a-table-column title="类型" data-index="type" :width="120" align="center">
            <template #cell="{ record }">
              <a-tag color="gray" bordered>{{ record.type }}</a-tag>
            </template>
          </a-table-column>
          <a-table-column title="客户/部门" data-index="customer_name" :min-width="150" />
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
                <a-button v-if="record.status === 2" type="text" size="small" @click="handleReview(record)">
                  <template #icon><icon-search /></template>
                  货物复核
                </a-button>
                <a-button v-if="record.status === 3" type="text" status="success" size="small" @click="handleShip(record)">
                  <template #icon><icon-send /></template>
                  确认发货
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

    <!-- 复核弹窗 -->
    <a-modal
      :visible="reviewDialogVisible"
      title="货物复核"
      @cancel="reviewDialogVisible = false"
      @before-ok="confirmReview"
      width="950px"
    >
      <div class="review-dialog-content">
        <a-descriptions title="单据信息" :column="2" border>
          <a-descriptions-item label="出库单号">
            <span class="info-text">{{ temp.order_no }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="客户/部门">
            <span class="info-text">{{ temp.customer_name }}</span>
          </a-descriptions-item>
        </a-descriptions>
        
        <div class="detail-section">
          <div class="section-title">拣货复核明细</div>
          <a-table :data="temp.items" :pagination="false" :bordered="true">
            <template #columns>
              <a-table-column title="货品名称" data-index="goods_name" :min-width="150" />
              <a-table-column title="SKU" data-index="sku" :width="120" align="center" />
              <a-table-column title="计划数量" data-index="planned_quantity" :width="100" align="center">
                <template #cell="{ record }">
                  <span class="quantity-text">{{ record.planned_quantity }}</span>
                </template>
              </a-table-column>
              <a-table-column title="出库库位" :width="220" align="center">
                <template #cell="{ record, rowIndex }">
                  <a-select 
                    v-model="record.location_id" 
                    placeholder="选择拣货库位" 
                    allow-search
                    @change="(val) => handleLocationChange(val as string, rowIndex)" 
                    style="width: 100%"
                  >
                    <a-option v-for="loc in locationOptions" :key="loc._id" :label="loc.code" :value="loc._id" />
                  </a-select>
                </template>
              </a-table-column>
              <a-table-column title="实发数量" :width="150" align="center">
                <template #cell="{ record }">
                  <a-input-number v-model="record.picked_quantity" :min="0" :max="record.planned_quantity" size="small" />
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
import { getOutboundOrderList, getOutboundOrderDetail, reviewOutboundGoods, shipOutboundGoods } from '@/api/outbound'
import { getLocationList } from '@/api/basic'
import { Message, Modal } from '@arco-design/web-vue'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  order_no: undefined,
  status: 2 // 默认查询待复核
})

const pagination = computed(() => ({
  total: total.value,
  current: listQuery.page,
  pageSize: listQuery.limit,
  showTotal: true,
  showPageSize: true
}))

const locationOptions = ref<any[]>([])
const reviewDialogVisible = ref(false)
const temp = reactive({
  _id: undefined,
  order_no: '',
  customer_name: '',
  items: [] as any[]
})

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getOutboundOrderList({
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

const handleReview = (row: any) => {
  Object.assign(temp, JSON.parse(JSON.stringify(row)))
  // 初始化实发数量
  temp.items.forEach((item: any) => {
    if (!item.picked_quantity) {
      item.picked_quantity = item.planned_quantity
    }
  })
  reviewDialogVisible.value = true
  loadLocations()
}

const handleLocationChange = (val: string, index: number) => {
  const loc = locationOptions.value.find(l => l._id === val)
  if (loc) {
    temp.items[index].location_code = loc.code
  }
}

const confirmReview = async () => {
  const hasIncomplete = temp.items.some((item: any) => !item.location_id || item.picked_quantity === undefined)
  if (hasIncomplete) {
    Message.warning('请选择库位并填写实发数量')
    return false
  }

  try {
    await reviewOutboundGoods(temp._id, { items: temp.items })
    Message.success('复核完成')
    reviewDialogVisible.value = false
    getList()
    return true
  } catch (error) {
    console.error(error)
    return false
  }
}

const handleShip = (row: any) => {
  Modal.confirm({
    title: '提示',
    content: '确认商品已发货?',
    onOk: async () => {
      try {
        await shipOutboundGoods(row._id)
        Message.success('已确认发货')
        getList()
      } catch (error) {
        console.error(error)
      }
    }
  })
}

const handleDetail = async (row: any) => {
  try {
    const res: any = await getOutboundOrderDetail(row._id)
    Object.assign(temp, res)
    reviewDialogVisible.value = true
  } catch (error) {
    console.error(error)
  }
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
    0: 'red'
  }
  return map[status] || 'gray'
}

const getStatusLabel = (status: number) => {
  const map: any = {
    1: '待审核',
    2: '待复核',
    3: '待发货',
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
