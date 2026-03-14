<template>
  <div class="app-container">
    <div class="header-section">
      <h1 class="page-title">库位管理</h1>
    </div>

    <a-card class="action-card" :bordered="false">
      <a-space>
        <a-button type="primary" @click="handleAdd">
          <template #icon><icon-plus /></template>
          新增库位
        </a-button>
        <a-button>
          <template #icon><icon-upload /></template>
          导入
        </a-button>
        <a-button>
          <template #icon><icon-download /></template>
          导出
        </a-button>
      </a-space>
    </a-card>

    <a-card class="filter-card" :bordered="false">
      <a-form :model="listQuery" layout="inline" @submit="handleFilter">
        <a-form-item label="库房">
          <a-select v-model="listQuery.warehouse" placeholder="选择库房" allow-clear style="width: 160px">
            <a-option label="主仓库" value="主仓库" />
            <a-option label="辅助仓库" value="辅助仓库" />
          </a-select>
        </a-form-item>
        <a-form-item label="区域">
          <a-select v-model="listQuery.area" placeholder="选择区域" allow-clear style="width: 160px">
            <a-option label="A区冷成型" value="A区冷成型" />
            <a-option label="B区成品" value="B区成品" />
            <a-option label="维修件区" value="维修件区" />
          </a-select>
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model="listQuery.status" placeholder="选择状态" allow-clear style="width: 140px">
            <a-option label="空闲" :value="1" />
            <a-option label="占用" :value="2" />
            <a-option label="禁用" :value="0" />
          </a-select>
        </a-form-item>
        <a-form-item label="库位编码">
          <a-input v-model="listQuery.code" placeholder="输入库位编码" allow-clear style="width: 180px" />
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
          <a-table-column title="库位编码" data-index="code" :width="120" />
          <a-table-column title="库房" data-index="warehouse" :width="150" />
          <a-table-column title="区域" data-index="area" :width="180" />
          <a-table-column title="状态" align="center" :width="120">
            <template #cell="{ record }">
              <a-tag :color="getLocationStatusColor(record.status)" bordered>
                {{ getLocationStatusLabel(record.status) }}
              </a-tag>
            </template>
          </a-table-column>
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
      width="500px"
    >
      <a-form ref="dataFormRef" :model="temp" :rules="rules" auto-label-width>
        <a-form-item label="库位编码" field="code">
          <a-input v-model="temp.code" placeholder="如: A-01-01" />
        </a-form-item>
        <a-form-item label="所属库区" field="area">
          <a-input v-model="temp.area" placeholder="如: Area A" />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="货架号" field="shelf">
              <a-input v-model="temp.shelf" placeholder="如: 01" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="货位号" field="bin">
              <a-input v-model="temp.bin" placeholder="如: 01" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="状态" field="status">
          <a-select v-model="temp.status" placeholder="请选择状态">
            <a-option label="空置" :value="1" />
            <a-option label="部分占用" :value="2" />
            <a-option label="满载" :value="3" />
            <a-option label="禁用" :value="0" />
          </a-select>
        </a-form-item>
        <a-form-item label="备注" field="remark">
          <a-textarea v-model="temp.remark" placeholder="请输入备注" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { getLocationList, createLocation, updateLocation, deleteLocation } from '@/api/basic'
import { Message, Modal } from '@arco-design/web-vue'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  code: undefined,
  area: undefined,
  warehouse: undefined,
  status: undefined
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
  code: '',
  area: '',
  shelf: '',
  bin: '',
  status: 1,
  remark: ''
})

const rules = {
  code: [{ required: true, message: '库位编码是必填项' }],
  area: [{ required: true, message: '所属库区是必填项' }]
}

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getLocationList({
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
  listQuery.code = undefined
  listQuery.area = undefined
  listQuery.warehouse = undefined
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
    code: '',
    area: '',
    shelf: '',
    bin: '',
    status: 1,
    remark: ''
  })
}

const handleAdd = () => {
  resetTemp()
  dialogTitle.value = '新增库位'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  Object.assign(temp, row)
  dialogTitle.value = '编辑库位'
  dialogVisible.value = true
}

const confirmData = async () => {
  const errors = await dataFormRef.value?.validate()
  if (!errors) {
    try {
      if (temp._id) {
        await updateLocation(temp._id, temp)
        Message.success('更新成功')
      } else {
        await createLocation(temp)
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
    content: '确认删除该库位吗?',
    onOk: async () => {
      try {
        await deleteLocation(row._id)
        Message.success('删除成功')
        getList()
      } catch (error) {
        console.error(error)
      }
    }
  })
}

const getLocationStatusColor = (status: number) => {
  const map: any = {
    1: 'green',
    2: 'orange',
    3: 'red',
    0: 'gray'
  }
  return map[status] || 'gray'
}

const getLocationStatusLabel = (status: number) => {
  const map: any = {
    1: '空置',
    2: '部分占用',
    3: '满载',
    0: '禁用'
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
</style>
