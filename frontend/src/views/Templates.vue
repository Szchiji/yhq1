<template>
  <div>
    <h2>消息模板</h2>
    <el-table :data="templateList" v-loading="loading" stripe>
      <el-table-column prop="name" label="模板名称" />
      <el-table-column prop="template_type" label="类型" />
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { templateAPI } from '@/api'

const templateList = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    templateList.value = await templateAPI.list()
  } finally {
    loading.value = false
  }
})
</script>
