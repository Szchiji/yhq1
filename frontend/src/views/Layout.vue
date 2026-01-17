<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <h3>机器人管理</h3>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        router
        class="menu"
      >
        <el-menu-item index="/">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        
        <el-menu-item index="/menus">
          <el-icon><Menu /></el-icon>
          <span>菜单管理</span>
        </el-menu-item>
        
        <el-menu-item index="/flows">
          <el-icon><Connection /></el-icon>
          <span>流程管理</span>
        </el-menu-item>
        
        <el-menu-item index="/templates">
          <el-icon><Document /></el-icon>
          <span>消息模板</span>
        </el-menu-item>
        
        <el-menu-item index="/submissions">
          <el-icon><Finished /></el-icon>
          <span>审核管理</span>
        </el-menu-item>
        
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><Avatar /></el-icon>
              {{ userStore.userInfo?.username || '管理员' }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  color: #fff;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1f2d3d;
  color: #fff;
}

.logo h3 {
  margin: 0;
  font-size: 18px;
}

.menu {
  border-right: none;
  background-color: #304156;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
