<template>
    <label>Register page </label>
    <h3>Enter username</h3>
    <input type="text" v-model="user_name"/>
    <h3>Enter email: </h3>
    <input type="email" v-model="email" />
    <h3>Enter password: </h3>
    <input type="password" v-model="password" />
    

    <button v-on:click="register_user">ok</button>
</template>

<script>
import CustomFetch from '@/CustomeFetch';
export default{
    data(){
        return{
           user_name:'',
            email:"",
            password:""

        }
    },
    methods:{
        register_user(){
            CustomFetch('http://localhost:5050/register',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json'
                },
                body: JSON.stringify({  "name":this.user_name,
                                        "email": this.email,
                                        "password": this.password})

            })
            .then((data)=>{console.log(data)
                    sessionStorage.setItem('user_name', this.user_name)
                    this.$router.push(`/login`)})
            .catch((e) => alert(e))

    }
}
}

</script>
