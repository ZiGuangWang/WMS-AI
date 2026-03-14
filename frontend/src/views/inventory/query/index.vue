<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="never">
      <el-form :inline="true" :model="listQuery" class="demo-form-inline">
        <el-form-item label="货品名称">
          <el-input v-model="listQuery.goods_name" placeholder="请输入货品名称" clearable @keyup.enter="handleFilter" />
        </el-form-item>
        <el-form-item label="SKU编码">
          <el-input v-model="listQuery.sku" placeholder="请输入SKU编码" clearable @keyup.enter="handleFilter" />
        </el-form-item>
        <el-form-item label="库位编码">
          <el-input v-model="listQuery.location_code" placeholder="请输入库位编码" clearable @keyup.enter="handleFilter" />
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
        style="width: 100%;"
      >
        <el-table-column label="货品名称" prop="goods_name" align="center" />
        <el-table-column label="SKU编码" prop="sku" align="center" />
        <el-table-column label="库位编码" prop="location_code" align="center" />
        <el-table-column label="当前库存" prop="quantity" align="center">
          <template #default="scope">
            <span :class="scope.row.quantity === 0 ? 'text-danger' : ''">{{ scope.row.quantity }}</span>
          </template>
        </el-table-column>
        <el-table-column label="最近更新" prop="updated_at" align="center">
          <template #default="scope">
            {{ formatTime(scope.row.updated_at) }}
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getInventoryQuery } from '@/api/inventory'

const list = ref([])
const total = ref(0)
const listLoading = ref(true)
const listQuery = reactive({
  page: 1,
  limit: 20,
  goods_name: undefined,
  sku: undefined,
  location_code: undefined
})

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getInventoryQuery({
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
  listQuery.goods_name = undefined
  listQuery.sku = undefined
  listQuery.location_code = undefined
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

const formatTime = (time: string) => {
  return new Date(time).toLocaleString()
}

onMounted(() => {
  getList()
})
</script>

<style scoped lang="scss">
.filter-container {
  margin-bottom: 16px;
}
.text-danger {
  color: #f56c6c;
  font-weight: bold;
}
</style>
