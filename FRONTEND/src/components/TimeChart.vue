<template>
    <h3>Time series </h3>
    <canvas id="index1" height="300" width="600" />
</template>

<script>
import Chart from 'chart.js/auto'
import CustomFetch  from '@/CustomeFetch.js'
export default{
    props:['user_name'],

    data(){
        return{
            chart_data:[],
            data:'',
            list_name:[],
            x_label:[],
            y_label:'',
            cards:'',
            
        }
    },
     created(){
        //alert()
         CustomFetch(`http://localhost:5050/summary/${this.user_name}`,{
            'Authentication-Token':sessionStorage.getItem('Authentication-Token')

         })
         .then(r=>{
             this.data= r   
             console.log(r)
             this.getData2()
         }        

             
         )
         .catch(e=>console.log(e))

         
            },


 methods:{
    getData2(){
        //alert('method')
         const ctx = document.getElementById('index1')
             
        // taken from chart.js docs
    for(let x of this.data){
        this.x_label = Object.keys(x['time'])
        this.y_label =Object.values(x['time'])
    }
    
     const myChart = new Chart(ctx, {
         type: 'bar',
         data: {
         labels: this.x_label,
         datasets: [{
             label: 'completed cards',
             data: this.y_label,
             backgroundColor: [
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


     }}}
    

</script>

<style scoped>
canvas{
    display: block;
    margin: 0 auto;
    padding: 10px;
}
</style>