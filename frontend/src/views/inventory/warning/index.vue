<template>
  <div class="app-container">
    <el-card class="table-container" shadow="never">
      <template #header>
        <div class="card-header">
          <span>库存预警列表</span>
          <el-button type="primary" link icon="Refresh" @click="getList">刷新</el-button>
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
        <el-table-column label="货品名称" prop="goods_name" align="center" />
        <el-table-column label="SKU编码" prop="sku" align="center" />
        <el-table-column label="当前库存" prop="current_stock" align="center">
          <template #default="scope">
            <span class="text-danger">{{ scope.row.current_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column label="安全库存" prop="min_stock" align="center" />
        <el-table-column label="状态" align="center">
          <template #default="scope">
            <el-tag type="danger">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="150">
          <template #default="scope">
            <el-button link type="primary" icon="Plus" @click="handleRestock(scope.row)">去补货</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getInventoryWarning } from '@/api/inventory'
import { useRouter } from 'vue-router'

const router = useRouter()
const list = ref([])
const listLoading = ref(true)

const getList = async () => {
  listLoading.value = true
  try {
    const response: any = await getInventoryWarning()
    list.value = response
  } catch (error) {
    console.error(error)
  } finally {
    listLoading.value = false
  }
}

const handleRestock = (row: any) => {
  router.push('/inbound/order')
}

onMounted(() => {
  getList()
})
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.text-danger {
  color: #f56c6c;
  font-weight: bold;
}
</style>
