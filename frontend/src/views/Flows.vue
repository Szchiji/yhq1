<template>
  <div>
    <h2>流程管理</h2>
    <el-button type="primary" style="margin: 20px 0">
      <el-icon><Plus /></el-icon> 新建流程
    </el-button>
    <el-table :data="flowList" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="流程名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small">编辑</el-button>
          <el-button size="small" type="danger">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { flowAPI } from '@/api'

const flowList = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    flowList.value = await flowAPI.list()
  } finally {
    loading.value = false
  }
})
</script>
