import { createRouter, createWebHistory } from 'vue-router'
import LoginVue from '@/views/LoginVue.vue'
import RegisterVue from '@/views/RegisterVue.vue'
import landingPage from '@/views/LandingPage.vue'
import DashboardVue from '@/views/DashboardVue.vue'
//import HomeVue from '@/views/HomeVue.vue'
import ErrorVue from '@/views/ErrorVue.vue'
import SummaryPage from '@/views/SummaryPage.vue'

import EditList from '@/components/EditList.vue'
import EditCard from '@/components/EditCard.vue'
import CreateCard from '@/components/CreateCard.vue'


//import DashboardNavBar from '@/components/DashboardNavBar.vue'

import ListsCards from '@/views/ListsCards.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: landingPage,
    children:[{
      path: '/login',
      component: LoginVue,
      name: 'Login'
    },
    {
      path:'/register',
      name: "register",
      component: RegisterVue
    }
  ]
  },
   {
     path: '/dashboard/:user_name',
     name: 'dashboard',
     component: DashboardVue,
     children:[{
      path: 'summary',
      name:'summary',
      component: SummaryPage,
      props: true
     },
     {
      path: 'view',
      name:'view',
      component: ListsCards,
      props: true
     }
     ],
     props: true
   },
   {
    path:'/edit/list/:l_id',
    name:'EditList',
    component:EditList,
    props:true
   },
   {
    path:'/edit/card/:card_id',
    name:'EditCard',
    component:EditCard,
    props:true
   },
   {
    path:'/create/card/:card_id',
    name:'CreateCard',
    component:CreateCard,
    props:true
   },
   {
    path:'/error',
    name:'errorPage',
    component: ErrorVue,
   }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
