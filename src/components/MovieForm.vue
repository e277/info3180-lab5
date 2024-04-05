<script setup>

import { ref, onMounted, reactive } from 'vue';

let csrf_token = ref("")
let feedback = reactive({
    successMessage: "",
    errorMessages: []
})

onMounted(() => {
    getCsrfToken();
});

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        // console.log(data);
        csrf_token.value = data.csrf_token;
    })
}

function saveMovie() {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
        method: "POST",
        body: form_data,
        headers: {
            "X-CSRFToken": csrf_token.value
        }
    })
    .then(function(response) {
        if (!response.ok) {
            throw response;
        }
        return response.json();
    })
    .then(function(data) {
        feedback.successMessage = data.message;
        feedback.errorMessages = [];
    })
    .catch(function(error) {
        error.json().then((errorMessage) => {
            feedback.errorMessages = errorMessage.errors;
            feedback.successMessage = "";
        });
    });
}

</script>

<template>
    <form @submit.prevent="saveMovie" id="movieForm" class="form-group mb-3 col-md-6">
        <p v-if="feedback.successMessage" class="alert alert-success">{{ feedback.successMessage }}</p>
        <ul v-if="feedback.errorMessages.length" class="alert alert-danger">
            <li v-for="(error, index) in feedback.errorMessages" :key="index">{{ error }}</li>
        </ul>

        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" placeholder="Enter movie title" />
        <label for="description" class="form-label">Description</label>
        <textarea name="description" class="form-control" placeholder="Enter movie description"></textarea>
        <label for="poster" class="form-label">Poster</label>
        <input type="file" name="poster" class="form-control" />
        <button type="submit" class="btn btn-primary">Add movie</button>
    </form>
</template>