<template>
  <div>
    <h2>菜单管理</h2>
    <el-button type="primary" style="margin: 20px 0" @click="dialogVisible = true">
      <el-icon><Plus /></el-icon> 新建菜单
    </el-button>
    
    <el-table :data="menuList" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="icon" label="图标" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="order" label="排序" width="100" />
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-dialog v-model="dialogVisible" title="菜单配置" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="菜单名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="form.icon" placeholder="如: 📝" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.order" :min="0" />
        </el-form-item>
        <el-form-item label="每行按钮数">
          <el-input-number v-model="form.buttons_per_row" :min="1" :max="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { menuAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const menuList = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const form = ref({ name: '', icon: '', order: 0, buttons_per_row: 2 })

const loadMenus = async () => {
  loading.value = true
  try {
    menuList.value = await menuAPI.list()
  } finally {
    loading.value = false
  }
}

const handleEdit = (row) => {
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除此菜单？', '提示')
  await menuAPI.delete(row.id)
  ElMessage.success('删除成功')
  loadMenus()
}

const handleSave = async () => {
  if (form.value.id) {
    await menuAPI.update(form.value.id, form.value)
  } else {
    await menuAPI.create(form.value)
  }
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadMenus()
}

onMounted(loadMenus)
</script>
