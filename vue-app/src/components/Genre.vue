<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { GenreService } from '../services/GenreService'
import type { Genre, GenreResponse } from '../domain/genre'

const genreService = new GenreService()  // ✅ Create instance

const genres = ref<GenreResponse[]>([])
const newGenre = ref<Genre>({ name: '', description: '' })
const search = ref('')
const error = ref<string | null>(null)

const loadGenres = async () => {
  const response = await genreService.getAll()
  genres.value = response.data || []
}

const addGenre = async () => {
  const response = await genreService.add(newGenre.value)
  if (response.data) {
    genres.value.push(response.data)
    newGenre.value = { name: '', description: '' }
  } else {
    error.value = response.errors?.[0] || 'Add failed'
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

    <form @submit.prevent="addGenre">
      <input v-model="newGenre.name" placeholder="Name" required />
      <input v-model="newGenre.description" placeholder="Description" />
      <button type="submit">Add Genre</button>
    </form>

    <input v-model="search" placeholder="Search by name..." />

    <ul>
      <li v-for="genre in filteredGenres" :key="genre.id">
        <strong>{{ genre.name }}</strong> - {{ genre.description }}
      </li>
    </ul>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>
