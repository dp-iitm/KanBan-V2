<template>
    <h3>Your summary across lists </h3>
    <canvas id="myChart" width="400" height="400" ></canvas>

    <br /><hr /> 
   

    <TimeChart :user_name=user_name ></TimeChart>


    <hr />

    <table class="table table-striped">
        <thead>
            <tr>
                <th>LIST NAME</th>
                <th>TOTAL CARDS</th>
                <th>CARDS DONE</th>
                <th>CARDS NOT DONE</th> 
                <th>CARDS CROSSED DEADLINE</th>
                <th>CARD TIMELINE </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="list in lists" :key="list">
                <td>{{list.list_name}} </td>
                <td>{{list.total_cards}}</td>
                <td>
                    {{list.cards_done}}
                </td>
                <td>{{list.cards_not_done}} </td>
                <td>
                    {{list.cards_crossed_deadline }}
                </td>
                <td>{{  list.t }}</td>
       


            </tr>
        </tbody>
    </table>
      
</template>

<script>
import Chart from 'chart.js/auto'
import CustomFetch  from '@/CustomeFetch.js'
import TimeChart from '@/components/TimeChart.vue'
export default{
    props:['user_name'],
    components:{ TimeChart },

    data(){
        return{
            lists:'',
            x_label:[],
            y_label:[],
            time:[],          
        }
    },

     created(){
        
         CustomFetch(`http://localhost:5050/summary/time/${this.user_name}`,{
         headers:{
            'Authentication-Token':sessionStorage.getItem('Authentication-Token')

         }})
         .then(r=>{
             this.lists=r
             this.getData1()

             }
         )
         .catch(e=>console.log(e))

         
            },


methods:{
    getData1(){
        const ctx = document.getElementById('myChart');
        for(let x of this.lists){
            this.x_label.push(x.list_name)
            this.y_label.push(x.cards_done)
            this.time.push(x.t)
            }
        
    // taken from chart.js docs
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
        labels: this.x_label,
        datasets: [{
            label: 'No of cards completed per list',
            data: this.y_label,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: false,
            maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
})
myChart


    }}
}
</script>

<style scoped>
canvas{
    display: block;
    margin: 0 auto;
    padding: 10px;
}
</style>