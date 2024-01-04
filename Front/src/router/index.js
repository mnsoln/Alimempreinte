import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ManualInput from '../views/ManualInput.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'public home',
      component: HomeView
    },
    {
      path: '/admin/',
      name: 'admin home',
      component: HomeView
    },
    {
      path: '/crous/',
      name: 'crous home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
    path:'/manual-input',
    name: 'manualInput',
    component : ManualInput
  },
  {
    path:'/manual-input/admin/',
    name: 'admin manualInput',
    component : ManualInput
  },
  {
    path:'/manual-input/crous/',
    name: 'crous manualInput',
    component : ManualInput
  },
  ]
})

export default router
