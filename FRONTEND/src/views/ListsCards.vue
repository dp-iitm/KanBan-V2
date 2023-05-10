<template>
    <h5 padding="10px">hello {{ user_name }} this your lists and cards </h5>
    <input v-model="new_list" placeholder="enter a task"><button type="button" v-on:click="add_list">ADD TASK</button><br/><br/>
<div class="container">
  <div class="row align-items-start">
    <div class="col gx-3" v-for="task,index in tasks " :key="task">
        <div class="p-2 border border-warning border-4" style="max-width: 22rem;"><h3>{{ task.title }}</h3>
           <i class="bi bi-box-arrow-in-down" v-on:click="export_card(task.id)"  ></i> | 
            <router-link :to="`/edit/list/${task.id}`"><i class="bi bi-pencil-fill" ></i></router-link> |
                    <router-link :to="`/create/card/${task.id}`"><i class="bi bi-plus-square"></i></router-link> |
                <i class="bi bi-trash3" v-on:click="delete_list(task.id,index)" ></i>

            </div>
            <br />


           <div v-for="x, index  in cards" :key="x">
            <CardComponent v-if="x.l_id==task.id" 
            :task_card=x :tasks=tasks 
            @delete_card="delete_card(index)" 
            @shift="shift_card" />

          </div>
          </div>
          </div>
         
          </div>

          
</template>

<script>
import CustomFetch from '@/CustomeFetch.js'
import CardComponent from '@/components/CardVue.vue'

export default {
    props:['user_name'],
    components:{
      CardComponent
    },
    data(){
        return { 
        tasks: '',
        cards:'',
        error: null,
        new_list:'',
        isEmpty:0,
        selected:'',
        file:''
    }
},
mounted(){
    CustomFetch(`http://127.0.0.1:5050/list/get/${this.user_name}`,{
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": sessionStorage.getItem('Authentication-Token'),
      }
    },
    )
      .then((data) => {
          this.tasks=(data)
          console.log(this.tasks)         
    }
      )
      .catch((err) => {
        this.error = err.message
        
        this.$router.push('/error')
        //alert(this.error)
        console.log(err)
      }) 
  
          CustomFetch(`http://127.0.0.1:5050/cards/get/${this.user_name}`,{
          headers: {
          "Content-Type": "application/json",
          "Authentication-Token": sessionStorage.getItem('Authentication-Token'),
      }
    })
          .then((c_data)=>{
            this.cards=c_data
            }
        )
        .catch((e)=>console.log(e))  
          },      


methods:{
      //add a new task
      add_list(){
        //alert(this.new_list)
        if(this.new_list==''){alert('list name cant be empty !')}
        else{
        CustomFetch(`http://127.0.0.1:5050/list/post/${this.user_name}`,{
        method:'POST',
        headers: {
        'Content-Type': 'application/json',
        "Authentication-Token": sessionStorage.getItem('Authentication-Token')
        },
        body: JSON.stringify({'title': this.new_list})
      }).then((data) => {
        console.log(data)
      
        this.$router.go(0)
      })
      .catch((err) => {
        this.error = err.message
        //this.$router.push('/error')
        alert(this.error)
        console.log(err)
      })
    }},
    
    //export cards of a particular list
    export_card(task_id){
      alert('cards info for the list exported !')
      CustomFetch(`http://127.0.0.1:5050/export/card/${task_id}`,{
        method:'GET',
        headers: {
        'Content-Type': 'application/json',
        "Authentication-Token": sessionStorage.getItem('Authentication-Token')
        },
      }).then((data) => {
        console.log(data)
      })
      .catch((err) => {
        this.error = err.message
        //this.$router.push('/error')
        alert(this.error)
        console.log(err)
      })

      //download data from the endpoint
        setTimeout(() => {
          window.location.href="http://localhost:5050/download/cards/csv"
        }, 2000);

    },


    //delete a list/task
    delete_list(id,index){
      
      for(let c of this.cards){
        console.log(c)         
          if(c.l_id==id){
            this.isEmpty = 1
            console.log(this.isEmpty)
          }

        }
        //console.log(this.isEmpty)
      
      if(this.isEmpty == 0){      
       CustomFetch(`http://127.0.0.1:5050/list/delete/${id}`, {
         method: 'DELETE',
         headers: {
                'Content-Type': 'application/json',
                "Authentication-Token": sessionStorage.getItem('Authentication-Token')
            }
       })
         .then(() => {
           this.tasks.splice(index, 1)
           console.log("done")
         })
         .catch((err) => {
           alert(err.message)
         })
     }
     else{
      if(confirm("do you want to delete the entire list with cards?")){
        CustomFetch(`http://127.0.0.1:5050/delete_all/${id}`,{
          'method':'DELETE',
          headers:{
          'Authentication-Token':sessionStorage.getItem('Authentication-Token')
        }})
        .then(d=>console.log(d))
        .catch(e=>console.log(e))

        this.$router.go()

      }
      
        


      }
      },

    


    // delete a particular card emit
     delete_card(index){
       //alert('sdsd')
       this.cards.splice(index,1)
           
      },

      //shift a card to another list emit
      shift_card(list, card_id){

        let l_id=0
        for(let l of this.tasks){
          if(l.title == list){
            l_id=l.id
          }
        }
        for(let c of this.cards){
          if(c.id == card_id){
            c.l_id=l_id
            //console.log(this.cards)
          }
        }

      }
    }
  }
        


  

</script>

<style scoped>
i{
  cursor: pointer;
}
</style>
