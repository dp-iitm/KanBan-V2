<template>
    <DashboardNavBar/>
    
    
    <br />

</template>

<script>
//import CustomFetch from '@/CustomeFetch.js'
import DashboardNavBar from '@/components/DashboardNavBar.vue'
//import ListsCards from '@/components/ListsCards.vue'
export default {
data(){
    return{
        user: this.$route.params.user_name,
        tasks:'helloo',
        error: ''
    }
},
components:{
   DashboardNavBar,
},
// mounted(){
// //alert('mounting!')
// CustomFetch(`http://127.0.0.1:5050/dashboard/${this.user}`)
//   .then((data) => {
//     this.tasks = data
//     console.log(data)
//   })
//   .catch((err) => {
//     this.error = err.message
    
//     this.$router.push('/error')
//     //alert(this.error)
//     console.log(err)
//   })
//fetch(`http://127.0.0.1:5050/login/${this.user}`).then((res)=>res.json()).
//then((data)=>this.tasks=data.lists[0])

}

</script>