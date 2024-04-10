<template> 
    <div class="container">
      <h1>Movies</h1>
      <div class="movies-container">
        <div v-for="m in movies" :key="m.id" class="row">
            <div class="movie-card col-sm">
              <div class="poster">
                <img :src="m.poster" alt="movie.poster"  class="card-img img-fluid"/>
              </div>
              <div class="m-body">
                    <h5 class="m-title">{{ m.title }}</h5>
                    <p class="m-description">{{ m.description }}</p>
              </div>
            </div>
        </div>
       </div>
    </div>
  </template>




<script setup>
    import { ref, onMounted } from "vue";

    let movies = ref([]);

    const fetchMovies = () => {
        fetch("/api/v1/movies", {
            method: 'GET',
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            movies.value=data.movies
      
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
    }

    onMounted(fetchMovies);

</script>

<style scoped>



.movies-container{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.movie-card{
    display: flex;
    margin: 30px;
    border-style: solid;
    border-color: rgb(189, 187, 187);
    border-radius: 15px;
    align-items: center;
}

.poster img{
    max-height: 100%;
    width: 400px;
    border-radius: 10px;

}

.poster{
    margin: 0; 
    padding: 0;
}

.m-body{
    padding: 15px;
}



</style>

