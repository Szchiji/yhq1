<template>
  <div>
    <h2>审核管理</h2>
    <el-table :data="submissionList" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="user_id" label="用户ID" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="提交时间" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" type="success" v-if="row.status === 'pending'">通过</el-button>
          <el-button size="small" type="danger" v-if="row.status === 'pending'">拒绝</el-button>
          <el-button size="small">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { submissionAPI } from '@/api'

const submissionList = ref([])
const loading = ref(false)

const getStatusType = (status) => {
  const types = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return types[status] || 'info'
}

onMounted(async () => {
  loading.value = true
  try {
    submissionList.value = await submissionAPI.list()
  } finally {
    loading.value = false
  }
})
</script>
