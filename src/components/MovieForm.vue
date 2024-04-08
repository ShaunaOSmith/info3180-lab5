<template>
  <form @submit.prevent="saveMovie" id="movieForm">
    <div class="form-group mb-3">
      <label for="title" class="form-label">Movie Title</label>
      <input type="text" id="title" v-model="formData.title" class="form-control" required>
    </div>
    <div class="form-group mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea id="description" v-model="formData.description" class="form-control" required></textarea>
    </div>
    <div class="form-group mb-3">
      <label for="poster" class="form-label">Poster</label>
      <input type="file" id="poster" @change="handleFileChange" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const formData = ref({
  title: '',
  description: '',
  poster: null
});

const csrfToken = ref('');

// Fetch CSRF token
const fetchCsrfToken = () => {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrfToken.value = data.csrf_token;
    })
    .catch(error => {
      console.error('Error fetching CSRF token:', error.message);
    });
};

fetchCsrfToken();


const saveMovie = () => {
  const movieForm = document.getElementById('movieForm');
  const formData = new FormData(movieForm);

  fetch('/api/v1/movies', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrfToken.value
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to add movie');
    }
    return response.json();
  })
  .then(data => {
    // Display a success message
    console.log(data);
  })
  .catch(error => {
    console.error('Error adding movie:', error.message);
  });
};

</script>

<style scoped>
/* Add your component-specific styles here */
.form-group {
  margin-bottom: 20px;
}
</style>