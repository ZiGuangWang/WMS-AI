<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="never">
      <el-form :inline="true" :model="listQuery" class="demo-form-inline">
        <el-form-item label="入库单号">
          <el-input v-model="listQuery.order_no" placeholder="请输入入库单号" clearable @keyup.enter="handleFilter" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleFilter">查询</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-container" shadow="never">
      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column label="入库单号" prop="order_no" align="center" width="180" />
        <el-table-column label="类型" prop="type" align="center" width="120" />
        <el-table-column label="供应商" prop="supplier_name" align="center" />
        <el-table-column label="状态" align="center" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="220">
          <template #default="scope">
            <el-button v-if="scope.row.status === 2" link type="primary" icon="Box" @click="handleCheck(scope.row)">验收货物</el-button>
            <el-button v-if="scope.row.status === 3" link type="success" icon="Position" @click="handleShelve(scope.row)">确认上架</el-button>
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

    <!-- 验收弹窗 -->
    <el-dialog title="货物验收" v-model="checkDialogVisible" width="800px">
      <el-form :model="temp" label-width="100px">
        <el-descriptions title="单据信息" :column="2" border>
          <el-descriptions-item label="入库单号">{{ temp.order_no }}</el-descriptions-item>
          <el-descriptions-item label="供应商">{{ temp.supplier_name }}</el-descriptions-item>
        </el-descriptions>
        
        <div style="margin-top: 20px;">
          <div style="font-weight: bold; margin-bottom: 10px;">货品验收明细</div>
          <el-table :data="temp.items" border style="width: 100%">
            <el-table-column label="货品" prop="goods_name" min-width="150" />
            <el-table-column label="SKU" prop="sku" width="120" align="center" />
            <el-table-column label="计划数量" prop="planned_quantity" width="100" align="center" />
            <el-table-column label="实收数量" width="150" align="center">
              <template #default="scope">
                <el-input-number v-model="scope.row.received_quantity" :min="0" :max="scope.row.planned_quantity" size="small" />
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="checkDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCheck">完成验收</el-button>
      </template>
    </el-dialog>

    <!-- 上架弹窗 -->
    <el-dialog title="货物上架" v-model="shelveDialogVisible" width="900px">
      <el-form :model="temp" label-width="100px">
        <el-descriptions title="单据信息" :column="2" border>
          <el-descriptions-item label="入库单号">{{ temp.order_no }}</el-descriptions-item>
          <el-descriptions-item label="供应商">{{ temp.supplier_name }}</el-descriptions-item>
        </el-descriptions>
        
        <div style="margin-top: 20px;">
          <div style="font-weight: bold; margin-bottom: 10px;">货品上架明细</div>
          <el-table :data="temp.items" border style="width: 100%">
            <el-table-column label="货品" prop="goods_name" min-width="150" />
            <el-table-column label="SKU" prop="sku" width="120" align="center" />
            <el-table-column label="实收数量" prop="received_quantity" width="100" align="center" />
            <el-table-column label="上架库位" width="250" align="center">
              <template #default="scope">
                <el-select v-model="scope.row.location_id" placeholder="选择上架库位" @change="(val) => handleLocationChange(val, scope.$index)" style="width: 100%">
                  <el-option v-for="loc in locationOptions" :key="loc._id" :label="loc.code" :value="loc._id" />
                </el-select>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="shelveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmShelve">完成上架</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getInboundOrders, receiveInboundGoods, shelveInboundGoods, updateInboundOrder } from '@/api/inbound'
import { getLocationList } from '@/api/basic'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  order_no: undefined
})

const checkDialogVisible = ref(false)
const shelveDialogVisible = ref(false)
const locationOptions = ref<any[]>([])
const temp = reactive<any>({
  _id: undefined,
  order_no: '',
  supplier_name: '',
  items: []
})

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getInboundOrders({
      ...listQuery,
      skip: (listQuery.page - 1) * listQuery.limit
    })
    // 过滤掉待审核(1)和已完成(4)的单据
    list.value = response.filter((o: any) => o.status === 2 || o.status === 3)
    total.value = list.value.length
  } catch (error) {
    console.error(error)
  } finally {
    listLoading.value = false
  }
}

const loadLocations = async () => {
  const response: any = await getLocationList({ limit: 1000 })
  locationOptions.value = response
}

const handleFilter = () => {
  listQuery.page = 1
  getList()
}

const resetQuery = () => {
  listQuery.order_no = undefined
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

const handleCheck = (row: any) => {
  Object.assign(temp, JSON.parse(JSON.stringify(row)))
  checkDialogVisible.value = true
}

const handleShelve = (row: any) => {
  Object.assign(temp, JSON.parse(JSON.stringify(row)))
  shelveDialogVisible.value = true
}

const handleLocationChange = (val: string, index: number) => {
  const loc = locationOptions.value.find(l => l._id === val)
  if (loc) {
    temp.items[index].location_code = loc.code
  }
}

const confirmCheck = async () => {
  try {
    await receiveInboundGoods(temp._id, temp.items)
    ElMessage.success('验收完成')
    checkDialogVisible.value = false
    getList()
  } catch (error) {
    console.error(error)
  }
}

const confirmShelve = async () => {
  // Check if all items have location assigned
  const missingLocation = temp.items.some((i: any) => !i.location_id)
  if (missingLocation) {
    ElMessage.warning('请为所有货品分配上架库位')
    return
  }
  
  try {
    // First update the order items with location IDs and codes
    await updateInboundOrder(temp._id, { items: temp.items })
    // Then call shelve
    await shelveInboundGoods(temp._id)
    ElMessage.success('上架完成，库存已更新')
    shelveDialogVisible.value = false
    getList()
  } catch (error) {
    console.error(error)
  }
}

const getStatusType = (status: number) => {
  const map: any = {
    2: 'primary',
    3: 'info'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: number) => {
  const map: any = {
    2: '待验收',
    3: '待上架'
  }
  return map[status] || '未知'
}

onMounted(() => {
  getList()
  loadLocations()
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
