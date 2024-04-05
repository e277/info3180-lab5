<script setup>
import { ref, onMounted } from 'vue';

let movies = ref([]);

onMounted(() => {
    fetchMovies();
});

function fetchMovies() {
    fetch('/api/v1/movies', {
        method: 'GET'
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        movies.value = data.movies;
        console.log(movies.value);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

</script>

<template>
    <div class="m-4">
        <h1>Movies</h1>

        <div class="container m-2">
            <div class="row">
                <div class="col-md-6" v-for="movie in movies" :key="movie.id">
                    <div class="row">
                        <div class="col-md-6 mb-4">
                            <img class="img-fluid" :src="movie.poster" alt="Movie Poster" >
                        </div>
                        <div class="col-md-5">
                            <h6>{{ movie.title }}</h6>
                            <p>{{ movie.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>