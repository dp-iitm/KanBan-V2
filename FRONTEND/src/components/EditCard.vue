<template>
    <h3>Edit your card</h3>

    <label>Enter title </label>
    <input type="text" v-model="new_card_title" required><br />

    <label>Enter content </label>
    <textarea type="text" v-model="new_card_content" required/><br />


    <label>Enter deadline </label>
    <input type="datetime-local" v-model="new_deadline" required/><br />


    <input type="radio" id="one" value="Done" v-model="new_picked" />
    <label for="one">Done</label>

    <input type="radio" id="two" value="Not Done" v-model="new_picked" checked="checked"/>
    <label for="two">Not Done</label><br />

    <button v-on:click="edit_card">OK</button>
</template>

<script>
export default {
    props:['card_id'],
    name:'EditCard',
    data(){
        return{
        new_card_title:'',
        new_card_content:'',
        new_deadline:'',
        new_picked:'',
        card_data:''
        
    }
},


mounted(){
    //alert('mounting')
    fetch(`http://127.0.0.1:5050/get/card/${this.card_id}`,{
        'mode':'cors'
    })
    .then(d=>d.json())
    .then(r=>{this.new_card_title=r.title;
            this.new_card_content=r.content;
            this.new_deadline=new Date(r.deadline).toISOString().slice(0,16); 
        console.log(this.card_data)})
    .catch(e=>console.log(e))



},
    methods:{
        edit_card(){
            
            fetch(`http://127.0.0.1:5050/cards/put/${this.card_id}`,{
                method:'PUT',
                headers:{
                    'content-type':'application/json',
                    "Authentication-Token": sessionStorage.getItem('Authentication-Token')
                },
                body:JSON.stringify({
                    "title":this.new_card_title,
                    "content":this.new_card_content,
                    "deadline":this.new_deadline,
                    "completed":this.new_picked
                })
            }).then((data)=>data.json())
            .then((response)=>console.log(response))
            .catch(e=>console.log(e))

            this.$router.go(-1)


        }
    }
    

}
</script>