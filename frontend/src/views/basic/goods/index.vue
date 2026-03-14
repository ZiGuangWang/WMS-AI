<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="never">
      <el-form :inline="true" :model="listQuery" class="demo-form-inline">
        <el-form-item label="货品名称">
          <el-input v-model="listQuery.name" placeholder="请输入货品名称" clearable @keyup.enter="handleFilter" />
        </el-form-item>
        <el-form-item label="SKU编码">
          <el-input v-model="listQuery.sku" placeholder="请输入SKU编码" clearable @keyup.enter="handleFilter" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleFilter">查询</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-container" shadow="never">
      <div slot="header" class="clearfix">
        <el-button type="primary" icon="Plus" @click="handleAdd">新增货品</el-button>
        <el-button type="success" icon="Download" @click="handleExport">导出</el-button>
        <el-button type="warning" icon="Upload" @click="handleImport">导入</el-button>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column label="货品名称" prop="name" align="center" />
        <el-table-column label="SKU编码" prop="sku" align="center" />
        <el-table-column label="条码" prop="barcode" align="center" />
        <el-table-column label="分类" prop="category" align="center" />
        <el-table-column label="单位" prop="unit" align="center" />
        <el-table-column label="规格" prop="spec" align="center" />
        <el-table-column label="安全库存" prop="min_stock" align="center" />
        <el-table-column label="状态" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
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
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form ref="dataFormRef" :model="temp" :rules="rules" label-width="100px" style="width: 450px; margin-left:50px;">
        <el-form-item label="货品名称" prop="name">
          <el-input v-model="temp.name" placeholder="请输入货品名称" />
        </el-form-item>
        <el-form-item label="SKU编码" prop="sku">
          <el-input v-model="temp.sku" placeholder="请输入SKU编码" />
        </el-form-item>
        <el-form-item label="条码" prop="barcode">
          <el-input v-model="temp.barcode" placeholder="请输入条码" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="temp.category" placeholder="请输入分类" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="temp.unit" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="规格" prop="spec">
          <el-input v-model="temp.spec" placeholder="请输入规格" />
        </el-form-item>
        <el-form-item label="安全库存" prop="min_stock">
          <el-input-number v-model="temp.min_stock" :min="0" />
        </el-form-item>
        <el-form-item label="单价" prop="price">
          <el-input-number v-model="temp.price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="temp.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
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
import { getGoodsList, createGoods, updateGoods, deleteGoods } from '@/api/basic'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  name: undefined,
  sku: undefined
})

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
  name: [{ required: true, message: '货品名称是必填项', trigger: 'blur' }],
  sku: [{ required: true, message: 'SKU编码是必填项', trigger: 'blur' }],
  unit: [{ required: true, message: '单位是必填项', trigger: 'blur' }]
}

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getGoodsList({
      ...listQuery,
      skip: (listQuery.page - 1) * listQuery.limit
    })
    list.value = response
    // For simplicity, we'll use list length as total or handle total in backend later
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
  await dataFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (temp._id) {
          await updateGoods(temp._id, temp)
          ElMessage.success('更新成功')
        } else {
          await createGoods(temp)
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
  ElMessageBox.confirm('确认删除该货品吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await deleteGoods(row._id)
    ElMessage.success('删除成功')
    getList()
  })
}

const handleExport = () => {
  ElMessage.info('功能开发中...')
}

const handleImport = () => {
  ElMessage.info('功能开发中...')
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
