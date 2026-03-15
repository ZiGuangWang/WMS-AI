<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">供应商管理</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button type="primary" v-permission="'wms:basic:supplier:add'" @click="handleAdd">
          <template #icon><icon-plus /></template>
          新增供应商
        </a-button>
        <a-button v-permission="'wms:basic:supplier:export'" @click="handleExport">
          <template #icon><icon-download /></template>
          导出
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="供应商名称">
          <a-input v-model="listQuery.name" placeholder="输入供应商名称" allow-clear />
        </a-form-item>
        <a-form-item>
          <a-space>
            <a-button type="primary" v-permission="'wms:basic:supplier:search'" @click="handleFilter">
              <template #icon><icon-search /></template>
              查询
            </a-button>
            <a-button v-permission="'wms:basic:supplier:reset'" @click="resetQuery">
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
          <a-table-column title="供应商名称" :min-width="200">
            <template #cell="{ record }">
              <div class="supplier-name-cell">
                <div class="supplier-icon">{{ record.name.charAt(0) }}</div>
                <span>{{ record.name }}</span>
              </div>
            </template>
          </a-table-column>
          <a-table-column title="联系人" data-index="contact_person" :width="120" />
          <a-table-column title="联系电话" data-index="phone" :width="150" />
          <a-table-column title="邮箱" data-index="email" :width="180" />
          <a-table-column title="地址" data-index="address" :min-width="200" ellipsis tooltip />
          <a-table-column title="状态" align="center" :width="100">
            <template #cell="{ record }">
              <a-tag :color="record.status === 1 ? 'green' : 'red'" bordered>
                {{ record.status === 1 ? '启用' : '禁用' }}
              </a-tag>
            </template>
          </a-table-column>
          <a-table-column title="操作" align="center" :width="180">
            <template #cell="{ record }">
              <a-space>
                <a-button type="text" size="small" v-permission="'wms:basic:supplier:edit'" @click="handleEdit(record)">
                  <template #icon><icon-edit /></template>
                  编辑
                </a-button>
                <a-button type="text" status="danger" size="small" v-permission="'wms:basic:supplier:delete'" @click="handleDelete(record)">
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
      width="550px"
    >
      <a-form ref="dataFormRef" :model="temp" :rules="rules" auto-label-width>
        <a-form-item label="供应商名称" field="name">
          <a-input v-model="temp.name" placeholder="请输入供应商名称" />
        </a-form-item>
        <a-form-item label="联系人" field="contact_person">
          <a-input v-model="temp.contact_person" placeholder="请输入联系人" />
        </a-form-item>
        <a-form-item label="联系电话" field="phone">
          <a-input v-model="temp.phone" placeholder="请输入联系电话" />
        </a-form-item>
        <a-form-item label="邮箱" field="email">
          <a-input v-model="temp.email" placeholder="请输入邮箱" />
        </a-form-item>
        <a-form-item label="地址" field="address">
          <a-textarea v-model="temp.address" :rows="3" placeholder="请输入地址" />
        </a-form-item>
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
import { getSupplierList, createSupplier, updateSupplier, deleteSupplier } from '@/api/basic'
import { Message, Modal } from '@arco-design/web-vue'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  name: undefined
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
  contact_person: '',
  phone: '',
  email: '',
  address: '',
  status: 1
})

const rules = {
  name: [{ required: true, message: '供应商名称是必填项' }],
  contact_person: [{ required: true, message: '联系人是必填项' }],
  phone: [{ required: true, message: '联系电话是必填项' }]
}

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getSupplierList({
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
    contact_person: '',
    phone: '',
    email: '',
    address: '',
    status: 1
  })
}

const handleAdd = () => {
  resetTemp()
  dialogTitle.value = '新增供应商'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  Object.assign(temp, row)
  dialogTitle.value = '编辑供应商'
  dialogVisible.value = true
}

const confirmData = async () => {
  const errors = await dataFormRef.value?.validate()
  if (!errors) {
    try {
      if (temp._id) {
        await updateSupplier(temp._id, temp)
        Message.success('更新成功')
      } else {
        await createSupplier(temp)
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
    content: '确定要删除该供应商吗？',
    onOk: async () => {
      try {
        await deleteSupplier(row._id)
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
}

.filter-card {
  margin-bottom: 16px;
}

.table-card {
  background-color: #fff;
}

.supplier-name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  .supplier-icon {
    width: 32px;
    height: 32px;
    background-color: #e8f3ff;
    color: #165dff;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    font-weight: bold;
    font-size: 14px;
  }
}
</style>
