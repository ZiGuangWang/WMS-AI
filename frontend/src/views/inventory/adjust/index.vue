<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="never">
      <template #header>
        <div class="card-header">
          <span>库存调整</span>
          <el-button type="primary" icon="Plus" @click="handleAdd">新增调整单</el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="listQuery" class="demo-form-inline">
        <el-form-item label="操作类型">
          <el-select v-model="listQuery.type" placeholder="请选择类型" clearable>
            <el-option label="入库" value="入库" />
            <el-option label="出库" value="出库" />
            <el-option label="调整" value="调整" />
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
        <span>变动记录</span>
      </template>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%;"
      >
        <el-table-column label="货品名称" prop="goods_name" align="center" />
        <el-table-column label="SKU编码" prop="sku" align="center" />
        <el-table-column label="单据号" prop="order_no" align="center" width="180" />
        <el-table-column label="类型" prop="type" align="center" width="100" />
        <el-table-column label="库位" prop="location_code" align="center" width="120" />
        <el-table-column label="变动数量" align="center" width="100">
          <template #default="scope">
            <span :class="scope.row.change_quantity > 0 ? 'text-success' : 'text-danger'">
              {{ scope.row.change_quantity > 0 ? '+' : '' }}{{ scope.row.change_quantity }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="变动后数量" prop="after_quantity" align="center" width="100" />
        <el-table-column label="操作人" prop="operator" align="center" width="100" />
        <el-table-column label="操作时间" prop="created_at" align="center">
          <template #default="scope">
            {{ formatTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="备注" prop="remark" align="center" show-overflow-tooltip />
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

    <!-- 调整弹窗 -->
    <el-dialog title="新增库存调整" v-model="dialogVisible" width="500px">
      <el-form ref="dataFormRef" :model="temp" :rules="rules" label-width="100px">
        <el-form-item label="货品" prop="goods_id">
          <el-select v-model="temp.goods_id" placeholder="请选择货品" style="width: 100%">
            <el-option v-for="item in goodsOptions" :key="item._id" :label="`${item.name} (${item.sku})`" :value="item._id" />
          </el-select>
        </el-form-item>
        <el-form-item label="库位" prop="location_id">
          <el-select v-model="temp.location_id" placeholder="请选择库位" style="width: 100%">
            <el-option v-for="loc in locationOptions" :key="loc._id" :label="loc.code" :value="loc._id" />
          </el-select>
        </el-form-item>
        <el-form-item label="调整数量" prop="adjust_quantity">
          <el-input-number v-model="temp.adjust_quantity" placeholder="正数为增，负数为减" style="width: 100%" />
        </el-form-item>
        <el-form-item label="调整原因" prop="remark">
          <el-input v-model="temp.remark" type="textarea" placeholder="请输入调整原因" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAdjust">确认调整</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getInventoryLogs, adjustInventory } from '@/api/inventory'
import { getGoodsList, getLocationList } from '@/api/basic'
import { ElMessage } from 'element-plus'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  type: undefined
})

const dialogVisible = ref(false)
const dataFormRef = ref()
const temp = reactive({
  goods_id: '',
  location_id: '',
  adjust_quantity: 0,
  remark: ''
})

const goodsOptions = ref<any[]>([])
const locationOptions = ref<any[]>([])

const rules = {
  goods_id: [{ required: true, message: '请选择货品', trigger: 'change' }],
  location_id: [{ required: true, message: '请选择库位', trigger: 'change' }],
  adjust_quantity: [{ required: true, message: '请输入调整数量', trigger: 'blur' }]
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
  const [goodsRes, locationRes]: any = await Promise.all([
    getGoodsList({ limit: 1000 }),
    getLocationList({ limit: 1000 })
  ])
  goodsOptions.value = goodsRes
  locationOptions.value = locationRes
}

const handleFilter = () => {
  listQuery.page = 1
  getList()
}

const resetQuery = () => {
  listQuery.type = undefined
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

const handleAdd = () => {
  Object.assign(temp, {
    goods_id: '',
    location_id: '',
    adjust_quantity: 0,
    remark: ''
  })
  dialogVisible.value = true
}

const confirmAdjust = async () => {
  await dataFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      if (temp.adjust_quantity === 0) {
        ElMessage.warning('调整数量不能为0')
        return
      }
      try {
        await adjustInventory(temp)
        ElMessage.success('调整成功')
        dialogVisible.value = false
        getList()
      } catch (error) {
        console.error(error)
      }
    }
  })
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
.text-success {
  color: #67c23a;
  font-weight: bold;
}
.text-danger {
  color: #f56c6c;
  font-weight: bold;
}
</style>
