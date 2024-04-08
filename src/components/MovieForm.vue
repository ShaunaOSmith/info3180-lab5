<template>
    <div>

        <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
            {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
            {{ errorMessage }}
        </div>
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

        
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const formData = ref({
  title: '',
  description: '',
  poster: null
});

const csrfToken = ref('');
const successMessage = ref('');
const errorMessage = ref('');


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

    onMounted(() => {
        fetchCsrfToken();
    }); 
};


const saveMovie = () => {
  const movieForm = document.getElementById('movieForm');
  const form_Data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: 'POST',
    body: form_Data,
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
    // Display success message
    successMessage.value = 'Movie added successfully!';
    // Clear form data
    formData.title = '';
    formData.description = '';
    formData.poster = null;
  })
  .catch(error => {
     // Display error message
    errorMessage.value = 'Failed to add movie';
    console.error('Error adding movie:', error.message);
  });
};

</script>

<style scoped>

.form-group {
  margin-bottom: 20px;
  margin-left: 20px;
}

.form-label {
  font-weight: bold;
}

.form-control {
  width: 100%;
  max-width: 400px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 20px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 5px;
  margin-left: 20px;
}

.success-message {
  color: green;
  font-size: 14px;
  margin-top: 5px;
  margin-left: 20px;
}
</style>