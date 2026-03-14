<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="never">
      <el-form :inline="true" :model="listQuery" class="demo-form-inline">
        <el-form-item label="库位编码">
          <el-input v-model="listQuery.code" placeholder="请输入库位编码" clearable @keyup.enter="handleFilter" />
        </el-form-item>
        <el-form-item label="所属库区">
          <el-select v-model="listQuery.area" placeholder="请选择库区" clearable>
            <el-option label="A区" value="Area A" />
            <el-option label="B区" value="Area B" />
            <el-option label="C区" value="Area C" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleFilter">查询</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-container" shadow="never">
      <div slot="header" class="clearfix">
        <el-button type="primary" icon="Plus" @click="handleAdd">新增库位</el-button>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column label="库位编码" prop="code" align="center" />
        <el-table-column label="所属库区" prop="area" align="center" />
        <el-table-column label="货架号" prop="shelf" align="center" />
        <el-table-column label="货位号" prop="bin" align="center" />
        <el-table-column label="状态" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="备注" prop="remark" align="center" />
        <el-table-column label="操作" align="center" width="200">
          <template #default="scope">
            <el-button link type="primary" icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="danger" icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          :current-page="listQuery.page"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="listQuery.limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px">
      <el-form ref="dataFormRef" :model="temp" :rules="rules" label-width="100px" style="width: 400px;">
        <el-form-item label="库位编码" prop="code">
          <el-input v-model="temp.code" placeholder="如: A-01-01" />
        </el-form-item>
        <el-form-item label="所属库区" prop="area">
          <el-input v-model="temp.area" placeholder="如: Area A" />
        </el-form-item>
        <el-form-item label="货架号" prop="shelf">
          <el-input v-model="temp.shelf" placeholder="如: 01" />
        </el-form-item>
        <el-form-item label="货位号" prop="bin">
          <el-input v-model="temp.bin" placeholder="如: 01" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="temp.status" placeholder="请选择状态">
            <el-option label="空置" :value="1" />
            <el-option label="部分占用" :value="2" />
            <el-option label="满载" :value="3" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="temp.remark" type="textarea" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmData">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getLocationList, createLocation, updateLocation, deleteLocation } from '@/api/basic'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  code: undefined,
  area: undefined
})

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
  code: [{ required: true, message: '库位编码是必填项', trigger: 'blur' }],
  area: [{ required: true, message: '所属库区是必填项', trigger: 'blur' }]
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
  handleFilter()
}

const handleSizeChange = (val: number) => {
  listQuery.limit = val
  getList()
}

const handleCurrentChange = (val: number) => {
  listQuery.page = val
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
  await dataFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (temp._id) {
          await updateLocation(temp._id, temp)
          ElMessage.success('更新成功')
        } else {
          await createLocation(temp)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        getList()
      } catch (error) {
        console.error(error)
      }
    }
  })
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm('确认删除该库位吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await deleteLocation(row._id)
    ElMessage.success('删除成功')
    getList()
  })
}

const getStatusType = (status: number) => {
  const map: any = {
    1: 'info',
    2: 'warning',
    3: 'success',
    0: 'danger'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: number) => {
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
.app-container {
  padding: 20px;
}
.filter-container {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
}
</style>
