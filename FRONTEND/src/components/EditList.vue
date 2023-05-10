<template>
    <h2>Edit your title:</h2>
    <input v-model='new_task_title'/>
    <button v-on:click="edit_list">OK</button>
</template>

<script>
export default{
    props:['l_id'],
    data(){
        return{
            new_task_title:''
        }
    },
    methods:{
        edit_list(){
            if(this.new_task_title == ''){
                alert('field required !')
            }
            else{
            fetch(`http://127.0.0.1:5050/list/put/${this.l_id}`,{
                method:'PUT',
                headers:{
                'Content-Type': 'application/json',
                "Authentication-Token": sessionStorage.getItem('Authentication-Token')
                },
                body: JSON.stringify({'title': this.new_task_title})
            })
            .then((data)=> data.json())
            .then((response)=> console.log(response))
            .catch(e=>console.log(e))

            this.$router.go(-1)
        }
    }
    }


}
</script>
