<template>
  <div>
    <h2>用户管理</h2>
    <el-table :data="userList" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="telegram_id" label="Telegram ID" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="first_name" label="名字" />
      <el-table-column prop="is_blocked" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.is_blocked ? 'danger' : 'success'">
            {{ row.is_blocked ? '已拉黑' : '正常' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button size="small" :type="row.is_blocked ? 'success' : 'danger'">
            {{ row.is_blocked ? '解除' : '拉黑' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { userAPI } from '@/api'

const userList = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    userList.value = await userAPI.list()
  } finally {
    loading.value = false
  }
})
</script>
