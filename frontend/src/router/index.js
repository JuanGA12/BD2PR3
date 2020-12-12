import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Error from '../views/Error.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
   
  },
  {
    path: '/*',
    name: 'Error',
    component: Error,
    meta: { layout: 'none' }
   
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
