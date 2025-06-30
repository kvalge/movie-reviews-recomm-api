<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { GenreService } from '../services/GenreService'
import type { Genre, GenreResponse } from '../domain/genre'

const genreService = new GenreService()

const genres = ref<GenreResponse[]>([])
const newGenre = ref<Genre>({ name: '', description: '' })
const search = ref('')
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)

const loadGenres = async () => {
  const response = await genreService.getAll()
  genres.value = response.data || []
}

const addGenre = async () => {
  const response = await genreService.add(newGenre.value)
  if (response.data) {
    genres.value.push(response.data)
    newGenre.value = { name: '', description: '' }
    successMessage.value = 'Genre created successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors?.[0] || 'Add failed'
  }
}

const editGenre = async (genre: GenreResponse) => {
  const response = await genreService.update(genre.id, genre)
  if (response.data) {
    const index = genres.value.findIndex(g => g.id === genre.id)
    if (index !== -1) {
      genres.value[index] = response.data
    }
    successMessage.value = 'Genre updated successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors?.[0] || 'Update failed'
  }
}

const deleteGenre = async (id: number) => {
  const response = await genreService.delete(id)
  if (!response.errors) {
    genres.value = genres.value.filter(g => g.id !== id)
    successMessage.value = 'Genre deleted successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors[0] || 'Delete failed'
  }
}

const filteredGenres = computed(() =>
  genres.value.filter(g =>
    g.name.toLowerCase().includes(search.value.toLowerCase())
  )
)

onMounted(loadGenres)
</script>

<template>
  <div class="genre-container">
    <h2>Genres</h2>

    <div class="mb-4">
      <button data-test="add-genre-button" class="btn btn-primary" @click="newGenre = { name: '', description: '' }">
        Add New Genre
      </button>
    </div>

    <form @submit.prevent="addGenre" class="mb-4">
      <div class="mb-3">
        <input 
          data-test="genre-name-input"
          v-model="newGenre.name" 
          class="form-control" 
          placeholder="Name" 
          required 
        />
      </div>
      <div class="mb-3">
        <input 
          data-test="genre-description-input"
          v-model="newGenre.description" 
          class="form-control" 
          placeholder="Description" 
        />
      </div>
      <button data-test="save-genre-button" type="submit" class="btn btn-success">
        Save Genre
      </button>
    </form>

    <input 
      v-model="search" 
      class="form-control mb-4" 
      placeholder="Search by name..." 
    />

    <div data-test="genres-list" class="list-group">
      <div 
        v-for="genre in filteredGenres" 
        :key="genre.id"
        data-test="genre-item" 
        class="list-group-item"
      >
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ genre.name }}</strong>
            <p class="mb-0">{{ genre.description }}</p>
          </div>
          <div>
            <button 
              data-test="edit-genre-button"
              class="btn btn-sm btn-warning me-2"
              @click="editGenre(genre)"
            >
              Edit
            </button>
            <button 
              data-test="delete-genre-button"
              class="btn btn-sm btn-danger"
              @click="deleteGenre(genre.id)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div 
      v-if="successMessage" 
      data-test="success-message" 
      class="alert alert-success mt-3"
    >
      {{ successMessage }}
    </div>

    <div 
      v-if="error" 
      class="alert alert-danger mt-3"
    >
      {{ error }}
    </div>
  </div>
</template>

<style scoped>
.genre-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>
