/**
 * Vue Router 配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: 'menus',
        name: 'Menus',
        component: () => import('@/views/Menus.vue')
      },
      {
        path: 'flows',
        name: 'Flows',
        component: () => import('@/views/Flows.vue')
      },
      {
        path: 'templates',
        name: 'Templates',
        component: () => import('@/views/Templates.vue')
      },
      {
        path: 'submissions',
        name: 'Submissions',
        component: () => import('@/views/Submissions.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/Users.vue')
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
