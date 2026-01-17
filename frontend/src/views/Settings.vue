<template>
  <div>
    <h2>系统设置</h2>
    <el-card>
      <el-descriptions title="系统信息" :column="1" border>
        <el-descriptions-item label="应用名称">{{ info.app_name }}</el-descriptions-item>
        <el-descriptions-item label="版本">{{ info.version }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { settingsAPI } from '@/api'

const info = ref({})

onMounted(async () => {
  info.value = await settingsAPI.getInfo()
})
</script>
