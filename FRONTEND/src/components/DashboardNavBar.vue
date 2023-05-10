<template>
    <nav>
        <RouterLink :to="{name: 'view'}">your dashboard home</RouterLink> |
        <RouterLink :to="{name: 'summary', params:{'user' : user }}">summary page</RouterLink> |      
        <a v-on:click="export_lists">export list</a>
        <i class="bi bi-file-earmark-arrow-down" v-on:click="export_lists"></i> |
        <RouterLink to="" v-on:click="logout">logout</RouterLink> 
    </nav>
    <router-view></router-view>
</template>

<script>

export default {
    props:['user'],
    data(){
        return{
            reponse:'',
            download:false
        }
    },
    methods:{
        logout(){
            fetch('http://localhost:5050/logout',{
                method:'POST',
                headers:{
                    'Content-type':'application/json'
                }
            })
            .then(r=>r.json())
            .then(d=>{console.log(d.code);
            sessionStorage.removeItem('Authentication-Token');
            this.$router.push('/login')})
            
        },
        export_lists(){
            alert('csv generated !') 
            fetch(`http://127.0.0.1:5050/export/lists/${this.$route.params.user_name}`,{
                headers:{
                'Authentication-Token':sessionStorage.getItem('Authentication-Token')

            }})
            .then(r=>r.text())
            .then(d=>{this.response=d; console.log(d)})
            .catch(e=>alert(e))

        //     setTimeout(()=>{fetch('http://127.0.0.1:5050/download/csv',{
                
        //                 })
        //     .then(r=>r.text())
        //     .then(d=>{this.response=d;console.log(d); this.download=true;})
        //     .catch(e=>alert(e))
        // },5000)

        setTimeout(()=>{
            window.location.href='http://127.0.0.1:5050/download/csv'
         
        }, 3000)
        
            
            


            
                
          
        },
    }
}
</script>

<style scoped>
nav{
    padding:15px; 
    background-color:aliceblue;
    font-size :25px;
}

</style>

<style scoped>
i{
    cursor: pointer;
}
</style>