<template>
  <div :class="color" style="max-width: 22rem;"  >
        <div class="card-header"><h5>{{ task_card.title }}</h5>
          <router-link :to="`/edit/card/${task_card.id}`"><i class="bi bi-pencil-fill"></i></router-link> |
          <i class="bi bi-trash3" v-on:click="delete_card(task_card.id)"></i> |
            <select v-model="selected" v-on:change="shift(selected, task_card.id)">
              <option disabled value="">shift</option>
              <option v-for="list in tasks" :key="list" >
                {{ list.title }}
              </option>
              
          </select></div>
        <div class="card-header">DEADLINE : {{ task_card.deadline.slice(0,22) }}</div>

        <div class="card-body">
          <!-- <h5 class="card-title">{{card.content}}</h5> -->
          <p class="card-text">{{ task_card.content }}</p>
          <p class="card-text"><small>created on:-{{ task_card.time_created.slice(0,22) }}</small></p>

          <p class="card-text"><small>updated on:-{{ task_card.time_updated.slice(0,22) }}</small></p>
          <div class="card-footer bg-transparent border-info">
            
              <p v-if="(task_card.time_completed)" >
                <i class="bi bi-check2-circle" style="color:limegreen;"></i> {{ task_card.time_completed.slice(0,22) }}
              </p>
          </div>
        </div>
        </div>
    

</template>

<script>

export default{
    name: "CardComponent",
    data(){
      return{
        selected:'',
        color:"card border-info mb-2",

          }
    },
    props: ["task_card", "tasks"],
    methods:{
      delete_card(id){
        if(confirm('do you want to delete the card ?')){
        this.$emit('delete_card')

        fetch(`http://127.0.0.1:5050/cards/delete/${id}`, {
          method:'DELETE',
          headers: {
                'Content-Type': 'application/json',
                "Authentication-Token": sessionStorage.getItem('Authentication-Token')
            }
        }).then(d=>d.json())
        .then(r=>console.log(r))
        .catch(e=>console.log(e))
      }
      //this.$router.go()
    },
    shift(title,card_id){
      console.log(title,card_id)
      this.selected=''
      this.$emit('shift', title, card_id )
      fetch(`http://127.0.0.1:5050/card/${card_id}/move/${title}/${this.$route.params.user_name}`,{
      headers: {
                'Content-Type': 'application/json',
                "Authentication-Token": sessionStorage.getItem('Authentication-Token')
            }})
      .then(d=>console.log(d))
      .catch(e=>console.log(e))

      //this.$router.go()
    },

    
  }
}

</script>

<style scoped>
i{
  cursor:pointer;
  color:darkblue
}


</style>
