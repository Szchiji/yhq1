<template>
  <div class="dashboard">
    <h2>仪表盘</h2>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon total-users">
              <el-icon size="40"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_users || 0 }}</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon today-users">
              <el-icon size="40"><UserFilled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.today_users || 0 }}</div>
              <div class="stat-label">今日新增</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon total-submissions">
              <el-icon size="40"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_submissions || 0 }}</div>
              <div class="stat-label">总提交数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon pending">
              <el-icon size="40"><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pending_submissions || 0 }}</div>
              <div class="stat-label">待审核</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card style="margin-top: 20px" v-loading="loading">
      <template #header>
        <span>提交趋势（最近7天）</span>
      </template>
      <div id="trend-chart" style="height: 400px"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dashboardAPI } from '@/api'
import * as echarts from 'echarts'

const stats = ref({})
const loading = ref(false)

const loadStats = async () => {
  loading.value = true
  try {
    stats.value = await dashboardAPI.getStats()
    renderChart()
  } catch (error) {
    console.error('加载统计数据失败', error)
  } finally {
    loading.value = false
  }
}

const renderChart = () => {
  const chartDom = document.getElementById('trend-chart')
  const myChart = echarts.init(chartDom)
  
  const dates = stats.value.trend_data?.map(item => item.date) || []
  const counts = stats.value.trend_data?.map(item => item.count) || []
  
  const option = {
    xAxis: {
      type: 'category',
      data: dates
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: counts,
        type: 'line',
        smooth: true,
        itemStyle: {
          color: '#409EFF'
        }
      }
    ],
    tooltip: {
      trigger: 'axis'
    }
  }
  
  myChart.setOption(option)
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.total-users {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.today-users {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.total-submissions {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.pending {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  color: #909399;
  margin-top: 5px;
}
</style>
