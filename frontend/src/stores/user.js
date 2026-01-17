/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { authAPI } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    async login(username, password) {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      
      const data = await authAPI.login(formData)
      this.token = data.access_token
      localStorage.setItem('token', data.access_token)
      
      await this.getUserInfo()
    },
    
    async getUserInfo() {
      const data = await authAPI.getMe()
      this.userInfo = data
    },
    
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    }
  }
})
