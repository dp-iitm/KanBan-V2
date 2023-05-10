<template>
    
    
    <div class="nav">
        <NavBar></NavBar>
        
            <HomeVue />
        
        <RouterView></RouterView>
    </div>
    
    
    
</template>

<script>
import NavBar from '@/components/HomeNavBar.vue';
import HomeVue from './HomeVue.vue';

export default{
    components: { NavBar , HomeVue}
}
</script>

<style scoped>
.nav{
    background-image: url('@/assets/background.jpg');
    display: inline-block;
    color: white;
    position:fixed;
    padding:0;
    margin:0;

    top:0;
    left:0;

    width: 100%;
    height: 100%;
    font-size: 30px;

    
    
}


</style>