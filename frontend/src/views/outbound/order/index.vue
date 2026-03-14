<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="never">
      <el-form :inline="true" :model="listQuery" class="demo-form-inline">
        <el-form-item label="出库单号">
          <el-input v-model="listQuery.order_no" placeholder="请输入出库单号" clearable @keyup.enter="handleFilter" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="listQuery.type" placeholder="请选择类型" clearable>
            <el-option label="销售出库" value="销售出库" />
            <el-option label="领用出库" value="领用出库" />
            <el-option label="其他出库" value="其他出库" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="listQuery.status" placeholder="请选择状态" clearable>
            <el-option label="待审核" :value="1" />
            <el-option label="待复核" :value="2" />
            <el-option label="待发货" :value="3" />
            <el-option label="已完成" :value="4" />
            <el-option label="已取消" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleFilter">查询</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-container" shadow="never">
      <template #header>
        <div class="card-header">
          <el-button type="primary" icon="Plus" @click="handleAdd">新增出库单</el-button>
        </div>
      </template>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%;"
      >
        <el-table-column label="出库单号" prop="order_no" align="center" width="180" />
        <el-table-column label="类型" prop="type" align="center" width="120" />
        <el-table-column label="客户/部门" prop="customer_name" align="center" />
        <el-table-column label="状态" align="center" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_at" align="center">
          <template #default="scope">
            {{ formatTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="备注" prop="remark" align="center" />
        <el-table-column label="操作" align="center" width="220">
          <template #default="scope">
            <el-button v-if="scope.row.status === 1" link type="primary" icon="Check" @click="handleAudit(scope.row)">审核</el-button>
            <el-button link type="primary" icon="View" @click="handleDetail(scope.row)">详情</el-button>
            <el-button v-if="scope.row.status === 1" link type="primary" icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button v-if="scope.row.status === 1" link type="danger" icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
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
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="800px">
      <el-form ref="dataFormRef" :model="temp" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出库类型" prop="type">
              <el-select v-model="temp.type" placeholder="请选择出库类型" style="width: 100%">
                <el-option label="销售出库" value="销售出库" />
                <el-option label="领用出库" value="领用出库" />
                <el-option label="其他出库" value="其他出库" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="客户/部门" prop="customer_name">
              <el-input v-model="temp.customer_name" placeholder="请输入客户或部门名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="temp.remark" type="textarea" placeholder="请输入备注" />
        </el-form-item>
        
        <div style="margin-top: 20px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: bold;">货品明细</span>
            <el-button type="primary" link icon="Plus" @click="addItem">添加货品</el-button>
          </div>
          <el-table :data="temp.items" border style="width: 100%">
            <el-table-column label="货品" min-width="200">
              <template #default="scope">
                <el-select v-model="scope.row.goods_id" placeholder="选择货品" @change="(val) => handleGoodsChange(val, scope.$index)" style="width: 100%">
                  <el-option v-for="item in goodsOptions" :key="item._id" :label="`${item.name} (${item.sku})`" :value="item._id" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="SKU" prop="sku" width="150" align="center" />
            <el-table-column label="计划出库量" width="120" align="center">
              <template #default="scope">
                <el-input-number v-model="scope.row.planned_quantity" :min="1" size="small" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80" align="center">
              <template #default="scope">
                <el-button link type="danger" icon="Delete" @click="removeItem(scope.$index)" />
              </template>
            </el-table-column>
          </el-table>
        </div>
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
import { getOutboundOrders, createOutboundOrder, updateOutboundOrder, auditOutboundOrder } from '@/api/outbound'
import { getGoodsList } from '@/api/basic'
import { ElMessage, ElMessageBox } from 'element-plus'

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

const dialogVisible = ref(false)
const dialogTitle = ref('')
const dataFormRef = ref()
const temp = reactive({
  _id: undefined,
  type: '销售出库',
  customer_name: '',
  items: [] as any[],
  remark: ''
})

const goodsOptions = ref<any[]>([])

const rules = {
  type: [{ required: true, message: '出库类型是必填项', trigger: 'change' }],
  customer_name: [{ required: true, message: '客户名称是必填项', trigger: 'blur' }]
}

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getOutboundOrders({
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
  const goodsRes: any = await getGoodsList({ limit: 1000 })
  goodsOptions.value = goodsRes
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
    type: '销售出库',
    customer_name: '',
    items: [],
    remark: ''
  })
}

const handleAdd = () => {
  resetTemp()
  dialogTitle.value = '新增出库单'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  Object.assign(temp, row)
  dialogTitle.value = '编辑出库单'
  dialogVisible.value = true
}

const handleAudit = (row: any) => {
  ElMessageBox.confirm('确认审核该出库单吗? 审核后将进入复核阶段。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(async () => {
    await auditOutboundOrder(row._id)
    ElMessage.success('审核成功')
    getList()
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
  await dataFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      if (temp.items.length === 0) {
        ElMessage.warning('请添加至少一个货品明细')
        return
      }
      try {
        if (temp._id) {
          await updateOutboundOrder(temp._id, temp)
          ElMessage.success('更新成功')
        } else {
          await createOutboundOrder(temp)
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
  ElMessageBox.confirm('确认删除该出库单吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    ElMessage.info('删除功能暂未开放')
  })
}

const handleDetail = (row: any) => {
  ElMessage.info('详情查看功能开发中...')
}

const getStatusType = (status: number) => {
  const map: any = {
    1: 'warning',
    2: 'primary',
    3: 'info',
    4: 'success',
    0: 'danger'
  }
  return map[status] || 'info'
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
  return new Date(time).toLocaleString()
}

onMounted(() => {
  getList()
  loadOptions()
})
</script>

<style scoped lang="scss">
.filter-container {
  margin-bottom: 16px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
