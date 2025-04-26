import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue'
import RoomsView from '@/views/RoomsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: DashboardView,
    },
    {
      path: '/rooms',
      name: 'Rooms',
      component: RoomsView,
    },
  ],
})

export default router
