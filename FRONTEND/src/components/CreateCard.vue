<template>
    <h3>Create your card</h3>

    <label>Enter title </label>
    <input v-model="card_title"/><br /><br />

    <label>Enter content </label>
    <textarea type="text" v-model="card_content"/><br /><br />

    <label>Enter deadline </label>
    <input type="datetime-local" v-model="deadline" /><br /><br />

    <input type="radio" id="one" value="Done" v-model="picked" />
    <label for="one">Done</label>

    <input type="radio" id="two" value="Not Done" v-model="picked" checked="checked"/>
    <label for="two">Not Done</label><br />

    <button v-on:click="add_card">ADD CARD</button>
    
</template>

<script>

export default {
    props:['card_id'],
    data(){
        return{
            card_title:'',
            card_content:'',
            deadline:'',
            picked:'',

        }
    },
    methods:{
    add_card(){
        if(this.deadline == '' || this.card_title=='' || this.card_content == ''){
            alert('ALL FIELDS ARE REQUIRED !')
        }
        else{
        fetch(`http://127.0.0.1:5050/cards/post/${this.card_id}`,{
            method:'POST',
            headers:{
                'content-type':'application/json',
                "Authentication-Token": sessionStorage.getItem('Authentication-Token')
            },
            body:JSON.stringify({
                "title":this.card_title,
                "content":this.card_content,
                "deadline":this.deadline,
                "completed":this.picked
            })
        }).
        then(d=>d.json()).
        then(r=>console.log(r))
        .catch(e=>alert(e))
        this.$router.go(-1)
    }
}
}
}
</script>