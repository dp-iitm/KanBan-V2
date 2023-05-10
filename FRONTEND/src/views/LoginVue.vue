<template>
  <label>Login Page </label>
  <h3>Enter username</h3>
  <input type="text" v-model="name">
  <h3>Enter email: </h3>
  <input type="text" v-model="email"><br />
  <h3>Enter password</h3>
  <input type="password" v-model="password"><br />

  <button v-on:click="login_user">OK</button>
</template>

<script>
import CustomFetch from '@/CustomeFetch';

export default{
  name:'loginView',
  data(){
      return{
          email: '',
          password:'',
          name:sessionStorage.getItem('user_name')
      }
  },
  methods:{
      login_user(){
      CustomFetch(`http://localhost:5050/login?include_auth_token`, {
      method: 'POST',
      body: JSON.stringify({email:this.email, password : this.password}),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((data) => {
        console.log(data);
        sessionStorage.setItem(
          'Authentication-Token',
          data.response.user['authentication_token']
          
        )
        this.$router.push(`/dashboard/${this.name}`)

        //console.log(sessionStorage.getItem('Authentication-Token'))
      })
      .catch((err) => {
        alert('please provide correct credentials !')
        console.log(err)
      })
      }

  }
}
</script>
