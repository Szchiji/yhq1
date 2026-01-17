/**
 * API 接口定义
 */
import request from './request'

// 认证相关
export const authAPI = {
  login: (data) => request.post('/auth/login', data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  getMe: () => request.get('/auth/me'),
  register: (data) => request.post('/auth/register', data)
}

// 仪表盘
export const dashboardAPI = {
  getStats: () => request.get('/dashboard/stats')
}

// 菜单管理
export const menuAPI = {
  list: (params) => request.get('/menus/', { params }),
  get: (id) => request.get(`/menus/${id}`),
  create: (data) => request.post('/menus/', data),
  update: (id, data) => request.put(`/menus/${id}`, data),
  delete: (id) => request.delete(`/menus/${id}`)
}

// 流程管理
export const flowAPI = {
  list: (params) => request.get('/flows/', { params }),
  get: (id) => request.get(`/flows/${id}`),
  create: (data) => request.post('/flows/', data),
  update: (id, data) => request.put(`/flows/${id}`, data),
  delete: (id) => request.delete(`/flows/${id}`)
}

// 模板管理
export const templateAPI = {
  list: (params) => request.get('/templates/', { params }),
  get: (id) => request.get(`/templates/${id}`),
  create: (data) => request.post('/templates/', data),
  update: (id, data) => request.put(`/templates/${id}`, data),
  delete: (id) => request.delete(`/templates/${id}`)
}

// 审核管理
export const submissionAPI = {
  list: (params) => request.get('/submissions/', { params }),
  get: (id) => request.get(`/submissions/${id}`),
  update: (id, data) => request.put(`/submissions/${id}`, data),
  approve: (id, note) => request.post(`/submissions/${id}/approve`, { note }),
  reject: (id, note) => request.post(`/submissions/${id}/reject`, { note })
}

// 用户管理
export const userAPI = {
  list: (params) => request.get('/users/', { params }),
  get: (id) => request.get(`/users/${id}`),
  getStats: () => request.get('/users/stats'),
  block: (id) => request.post(`/users/${id}/block`),
  unblock: (id) => request.post(`/users/${id}/unblock`)
}

// 系统设置
export const settingsAPI = {
  get: () => request.get('/settings/'),
  getInfo: () => request.get('/settings/info')
}
