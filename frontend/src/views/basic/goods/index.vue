<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">货品管理</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button type="primary" @click="handleAdd">
          <template #icon><icon-plus /></template>
          新增货品
        </a-button>
        <a-button @click="handleExport">
          <template #icon><icon-download /></template>
          导出
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="货品编码">
          <a-input v-model="listQuery.sku" placeholder="输入货品编码" allow-clear />
        </a-form-item>
        <a-form-item label="货品名称">
          <a-input v-model="listQuery.name" placeholder="输入货品名称" allow-clear />
        </a-form-item>
        <a-form-item label="分类">
          <a-select v-model="listQuery.category" placeholder="选择分类" allow-clear style="width: 180px">
            <a-option label="五金" value="五金" />
            <a-option label="配件" value="配件" />
            <a-option label="耗材" value="耗材" />
            <a-option label="劳保" value="劳保" />
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
        @page-change="handleCurrentChange"
        @page-size-change="handleSizeChange"
      >
        <template #columns>
          <a-table-column title="货品编码" data-index="sku" :width="120" />
          <a-table-column title="货品名称" :min-width="200">
            <template #cell="{ record }">
              <div class="goods-name-cell">
                <div class="goods-icon">{{ record.name.charAt(0) }}</div>
                <span>{{ record.name }}</span>
              </div>
            </template>
          </a-table-column>
          <a-table-column title="规格" data-index="spec" :width="120" />
          <a-table-column title="单位" data-index="unit" :width="100" align="center" />
          <a-table-column title="分类" data-index="category" :width="120" align="center" />
          <a-table-column title="操作" align="center" :width="180">
            <template #cell="{ record }">
              <a-space>
                <a-button type="text" size="small" @click="handleEdit(record)">
                  <template #icon><icon-edit /></template>
                  编辑
                </a-button>
                <a-button type="text" status="danger" size="small" @click="handleDelete(record)">
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
      width="600px"
    >
      <a-form ref="dataFormRef" :model="temp" :rules="rules" auto-label-width>
        <a-form-item label="货品名称" field="name">
          <a-input v-model="temp.name" placeholder="请输入货品名称" />
        </a-form-item>
        <a-form-item label="SKU编码" field="sku">
          <a-input v-model="temp.sku" placeholder="请输入SKU编码" />
        </a-form-item>
        <a-form-item label="条码" field="barcode">
          <a-input v-model="temp.barcode" placeholder="请输入条码" />
        </a-form-item>
        <a-form-item label="分类" field="category">
          <a-input v-model="temp.category" placeholder="请输入分类" />
        </a-form-item>
        <a-form-item label="单位" field="unit">
          <a-input v-model="temp.unit" placeholder="请输入单位" />
        </a-form-item>
        <a-form-item label="规格" field="spec">
          <a-input v-model="temp.spec" placeholder="请输入规格" />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="安全库存" field="min_stock">
              <a-input-number v-model="temp.min_stock" :min="0" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="单价" field="price">
              <a-input-number v-model="temp.price" :min="0" :precision="2" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="状态" field="status">
          <a-radio-group v-model="temp.status">
            <a-radio :value="1">启用</a-radio>
            <a-radio :value="0">禁用</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { getGoodsList, createGoods, updateGoods, deleteGoods } from '@/api/basic'
import { Message, Modal } from '@arco-design/web-vue'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  name: undefined,
  sku: undefined,
  category: undefined
})

const pagination = computed(() => ({
  total: total.value,
  current: listQuery.page,
  pageSize: listQuery.limit,
  showTotal: true,
  showPageSize: true
}))

const dialogVisible = ref(false)
const dialogTitle = ref('')
const dataFormRef = ref()
const temp = reactive({
  _id: undefined,
  name: '',
  sku: '',
  barcode: '',
  category: '',
  unit: '',
  spec: '',
  min_stock: 0,
  price: 0,
  status: 1
})

const rules = {
  name: [{ required: true, message: '货品名称是必填项' }],
  sku: [{ required: true, message: 'SKU编码是必填项' }],
  unit: [{ required: true, message: '单位是必填项' }]
}

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getGoodsList({
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
  listQuery.name = undefined
  listQuery.sku = undefined
  listQuery.category = undefined
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
    name: '',
    sku: '',
    barcode: '',
    category: '',
    unit: '',
    spec: '',
    min_stock: 0,
    price: 0,
    status: 1
  })
}

const handleAdd = () => {
  resetTemp()
  dialogTitle.value = '新增货品'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  Object.assign(temp, row)
  dialogTitle.value = '编辑货品'
  dialogVisible.value = true
}

const confirmData = async () => {
  const errors = await dataFormRef.value?.validate()
  if (!errors) {
    try {
      if (temp._id) {
        await updateGoods(temp._id, temp)
        Message.success('更新成功')
      } else {
        await createGoods(temp)
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
    content: '确认删除该货品吗?',
    onOk: async () => {
      try {
        await deleteGoods(row._id)
        Message.success('删除成功')
        getList()
      } catch (error) {
        console.error(error)
      }
    }
  })
}

const handleExport = () => {
  Message.info('功能开发中...')
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
  background-color: #fff;
}

.filter-card {
  margin-bottom: 16px;
  background-color: #fff;
}

.table-card {
  background-color: #fff;
}

.goods-name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  .goods-icon {
    width: 32px;
    height: 32px;
    background-color: #f2f3f5;
    color: #4e5969;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    font-weight: bold;
    font-size: 14px;
  }
}
</style>
