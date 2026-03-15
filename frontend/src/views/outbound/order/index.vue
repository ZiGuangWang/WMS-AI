<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">出库管理</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button type="primary" v-permission="'wms:outbound:order:add'" @click="handleAdd">
          <template #icon><icon-plus /></template>
          新增出库单
        </a-button>
        <a-button v-permission="'wms:outbound:order:export'" @click="handleExport">
          <template #icon><icon-download /></template>
          导出
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="出库单号">
          <a-input v-model="listQuery.order_no" placeholder="输入出库单号" allow-clear style="width: 180px" />
        </a-form-item>
        <a-form-item label="类型">
          <a-select v-model="listQuery.type" placeholder="全部类型" allow-clear style="width: 150px">
            <a-option label="销售出库" value="销售出库" />
            <a-option label="领用出库" value="领用出库" />
            <a-option label="其他出库" value="其他出库" />
          </a-select>
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model="listQuery.status" placeholder="全部状态" allow-clear style="width: 150px">
            <a-option label="待审核" :value="1" />
            <a-option label="待复核" :value="2" />
            <a-option label="待发货" :value="3" />
            <a-option label="已完成" :value="4" />
            <a-option label="已取消" :value="0" />
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-space>
            <a-button type="primary" v-permission="'wms:outbound:order:search'" @click="handleFilter">
              <template #icon><icon-search /></template>
              查询
            </a-button>
            <a-button v-permission="'wms:outbound:order:reset'" @click="resetQuery">
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
          <a-table-column title="创建时间" :width="180" align="center">
            <template #cell="{ record }">
              {{ formatTime(record.created_at) }}
            </template>
          </a-table-column>
          <a-table-column title="操作" align="center" :width="220" fixed="right">
            <template #cell="{ record }">
              <a-space>
                <a-button v-if="record.status === 1" type="text" size="small" v-permission="'wms:outbound:order:audit'" @click="handleAudit(record)">
                  <template #icon><icon-check /></template>
                  审核
                </a-button>
                <a-button v-if="record.status === 2" type="text" size="small" v-permission="'wms:outbound:order:review_go'" @click="handleGoReview(record)">
                  <template #icon><icon-check-square /></template>
                  去复核
                </a-button>
                <a-button type="text" size="small" v-permission="'wms:outbound:order:detail'" @click="handleDetail(record)">
                  <template #icon><icon-eye /></template>
                  详情
                </a-button>
                <a-button v-if="record.status === 1" type="text" size="small" v-permission="'wms:outbound:order:edit'" @click="handleEdit(record)">
                  <template #icon><icon-edit /></template>
                  编辑
                </a-button>
                <a-button v-if="record.status === 1" type="text" status="danger" size="small" v-permission="'wms:outbound:order:delete'" @click="handleDelete(record)">
                  <template #icon><icon-delete /></template>
                  删除
                </a-button>
              </a-space>
            </template>
          </a-table-column>
        </template>
      </a-table>
    </a-card>

    <!-- 新增/编辑弹窗 -->
    <a-modal
      :visible="dialogVisible"
      :title="dialogTitle"
      @cancel="dialogVisible = false"
      @before-ok="confirmData"
      width="850px"
    >
      <a-form ref="dataFormRef" :model="temp" :rules="rules" auto-label-width>
        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="出库类型" field="type">
              <a-select v-model="temp.type" placeholder="请选择出库类型">
                <a-option label="销售出库" value="销售出库" />
                <a-option label="领用出库" value="领用出库" />
                <a-option label="其他出库" value="其他出库" />
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="客户/部门" field="customer_name">
              <a-input v-model="temp.customer_name" placeholder="请输入客户或部门名称" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="备注" field="remark">
          <a-textarea v-model="temp.remark" :rows="2" placeholder="请输入备注" />
        </a-form-item>

        <div class="detail-section">
          <div class="section-header">
            <span class="title">货品明细</span>
            <a-button type="text" v-permission="'wms:outbound:order:item_add'" @click="addItem">
              <template #icon><icon-plus /></template>
              添加货品
            </a-button>
          </div>
          
          <a-table :data="temp.items" :pagination="false" :bordered="true">
            <template #columns>
              <a-table-column title="货品" :min-width="250">
                <template #cell="{ record, rowIndex }">
                  <a-select
                    v-model="record.goods_id"
                    allow-search
                    placeholder="选择货品"
                    @change="(val) => handleGoodsChange(val as string, rowIndex)"
                  >
                    <a-option
                      v-for="item in goodsOptions"
                      :key="item._id"
                      :label="`${item.name} (${item.sku})`"
                      :value="item._id"
                    />
                  </a-select>
                </template>
              </a-table-column>
              <a-table-column title="SKU" data-index="sku" :width="150" align="center" />
              <a-table-column title="计划出库数" :width="150" align="center">
                <template #cell="{ record }">
                  <a-input-number v-model="record.planned_quantity" :min="1" size="small" />
                </template>
              </a-table-column>
              <a-table-column title="操作" align="center" :width="80">
                <template #cell="{ rowIndex }">
                  <a-button type="text" status="danger" v-permission="'wms:outbound:order:item_remove'" @click="removeItem(rowIndex)">
                    <template #icon><icon-delete /></template>
                  </a-button>
                </template>
              </a-table-column>
            </template>
          </a-table>
        </div>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getOutboundOrderList, createOutboundOrder, updateOutboundOrder, auditOutboundOrder } from '@/api/outbound'
import { getGoodsList } from '@/api/basic'
import { Message, Modal } from '@arco-design/web-vue'

const router = useRouter()
const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  order_no: undefined,
  type: undefined,
  status: undefined
})

const pagination = computed(() => ({
  total: total.value,
  current: listQuery.page,
  pageSize: listQuery.limit,
  showTotal: true,
  showPageSize: true
}))

const goodsOptions = ref<any[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const dataFormRef = ref()
const temp = reactive({
  _id: undefined,
  order_no: '',
  type: '销售出库',
  customer_name: '',
  remark: '',
  items: [] as any[]
})

const rules = {
  type: [{ required: true, message: '请选择出库类型' }],
  customer_name: [{ required: true, message: '请输入客户或部门名称' }]
}

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

const loadOptions = async () => {
  try {
    const response: any = await getGoodsList({ limit: 1000 })
    goodsOptions.value = response
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
  listQuery.type = undefined
  listQuery.status = undefined
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

const resetTemp = () => {
  Object.assign(temp, {
    _id: undefined,
    order_no: '',
    type: '销售出库',
    customer_name: '',
    remark: '',
    items: []
  })
}

const handleAdd = () => {
  resetTemp()
  dialogTitle.value = '新增出库单'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  Object.assign(temp, JSON.parse(JSON.stringify(row)))
  dialogTitle.value = '编辑出库单'
  dialogVisible.value = true
}

const handleAudit = (row: any) => {
  Modal.confirm({
    title: '提示',
    content: '确认审核通过该出库单吗?',
    onOk: async () => {
      await auditOutboundOrder(row._id)
      Message.success('审核成功')
      getList()
    }
  })
}

const handleGoReview = (row: any) => {
  router.push({
    path: '/outbound/review',
    query: { order_no: row.order_no }
  })
}

const addItem = () => {
  temp.items.push({
    goods_id: '',
    goods_name: '',
    sku: '',
    planned_quantity: 1
  })
}

const removeItem = (index: number) => {
  temp.items.splice(index, 1)
}

const handleGoodsChange = (val: string, index: number) => {
  const goods = goodsOptions.value.find(g => g._id === val)
  if (goods) {
    temp.items[index].goods_name = goods.name
    temp.items[index].sku = goods.sku
  }
}

const confirmData = async () => {
  const errors = await dataFormRef.value?.validate()
  if (!errors) {
    if (temp.items.length === 0) {
      Message.warning('请添加至少一个货品明细')
      return false
    }
    try {
      if (temp._id) {
        await updateOutboundOrder(temp._id, temp)
        Message.success('更新成功')
      } else {
        await createOutboundOrder(temp)
        Message.success('创建成功')
      }
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

const handleDelete = (row: any) => {
  Modal.confirm({
    title: '提示',
    content: '确认删除该出库单吗?',
    onOk: async () => {
      Message.info('删除功能暂未开放')
    }
  })
}

const handleDetail = (row: any) => {
  Message.info('详情查看功能开发中...')
}

const handleExport = () => {
  Message.info('导出功能开发中...')
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

.order-no {
  color: #165dff;
  font-weight: 500;
  cursor: pointer;
  &:hover {
    text-decoration: underline;
  }
}

.detail-section {
  margin-top: 24px;
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    .title {
      font-weight: bold;
      font-size: 16px;
      color: #1d2129;
    }
  }
}
</style>
