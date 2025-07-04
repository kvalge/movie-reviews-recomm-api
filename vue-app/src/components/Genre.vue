<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { GenreService } from '../services/GenreService'
import type { Genre, GenreResponse } from '../domain/genre'

const genreService = new GenreService()

const genres = ref<GenreResponse[]>([])
const newGenre = ref<Genre>({ name: '', description: '' })
const selectedGenre = ref<GenreResponse | null>(null)
const searchText = ref('')
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const showDropdown = ref(false)
const isEditing = ref(false)

const loadGenres = async () => {
  try {
    const response = await genreService.getAll()
    genres.value = response.data || []
  } catch (err) {
    console.error('Error loading genres:', err)
    error.value = 'Failed to load genres'
  }
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

const updateGenre = async () => {
  if (!selectedGenre.value) return
  
  const response = await genreService.update(selectedGenre.value.id, selectedGenre.value)
  if (response.data) {
    const index = genres.value.findIndex(g => g.id === selectedGenre.value!.id)
    if (index !== -1) {
      genres.value[index] = response.data
      selectedGenre.value = response.data
    }
    isEditing.value = false
    successMessage.value = 'Genre updated successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors?.[0] || 'Update failed'
  }
}

const deleteGenre = async () => {
  if (!selectedGenre.value) return
  
  const response = await genreService.delete(selectedGenre.value.id)
  if (!response.errors) {
    genres.value = genres.value.filter(g => g.id !== selectedGenre.value!.id)
    selectedGenre.value = null
    searchText.value = ''
    isEditing.value = false
    successMessage.value = 'Genre deleted successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors[0] || 'Delete failed'
  }
}

const filteredGenres = computed(() => {
  if (!searchText.value.trim()) {
    return genres.value
  }
  
  return genres.value.filter(g =>
    g.name.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

const selectGenre = (genre: GenreResponse) => {
  selectedGenre.value = { ...genre }
  searchText.value = genre.name
  showDropdown.value = false
  isEditing.value = false
}

const onSearchFocus = () => {
  showDropdown.value = true
}

const onSearchInput = () => {
  showDropdown.value = true
  if (!searchText.value.trim()) {
    selectedGenre.value = null
    isEditing.value = false
  }
}

const onSearchBlur = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 300)
}

const clearSelection = () => {
  selectedGenre.value = null
  searchText.value = ''
  showDropdown.value = false
  isEditing.value = false
}

const startEditing = () => {
  isEditing.value = true
}

const cancelEditing = () => {
  if (selectedGenre.value) {
    const original = genres.value.find(g => g.id === selectedGenre.value!.id)
    if (original) {
      selectedGenre.value = { ...original }
    }
  }
  isEditing.value = false
}

onMounted(loadGenres)
</script>

<template>
  <div class="page-container">
    <h3>Genres</h3>
    
    <div class="split-container">
      <div class="left-panel">
        <h3 class="panel-title">Select</h3>
        
        <div class="dropdown-container">
          <input
            v-model="searchText"
            @input="onSearchInput"
            @focus="onSearchFocus"
            @click="onSearchFocus"
            @blur="onSearchBlur"
            class="form-control"
            placeholder="Click to select or start typing to search..."
            data-test="genre-search-input"
          />
          
          <div v-if="showDropdown" class="custom-dropdown-menu">
            <div
              v-for="genre in filteredGenres"
              :key="genre.id"
              @mousedown.prevent="selectGenre(genre)"
              data-test="dropdown-genre-item"
              class="custom-dropdown-item dropdown-item-hover"
            >
              <strong>{{ genre.name }}</strong>
            </div>
            <div v-if="filteredGenres.length === 0" class="dropdown-no-results">
              No genres found
            </div>
          </div>
        </div>

        <div v-if="selectedGenre" class="selected-item" data-test="selected-genre">
          <div v-if="!isEditing">
            <h4>{{ selectedGenre.name }}</h4>
            <p>{{ selectedGenre.description }}</p>
            
            <div class="action-buttons">
              <button 
                @click="startEditing"
                class="btn btn-warning btn-sm"
                data-test="edit-genre-button"
              >
                Edit
              </button>
              <button 
                @click="deleteGenre"
                class="btn btn-danger btn-sm"
                data-test="delete-genre-button"
              >
                Delete
              </button>
              <button 
                @click="clearSelection"
                class="btn btn-secondary"
                data-test="clear-selection-button"
              >
                Clear
              </button>
            </div>
          </div>
          
          <div v-else>
            <div class="form-group">
              <label class="form-label">Name</label>
              <input 
                v-model="selectedGenre.name"
                class="form-control"
                data-test="edit-genre-name-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea 
                v-model="selectedGenre.description"
                class="form-control"
                rows="3"
                data-test="edit-genre-description-input"
              ></textarea>
            </div>
            
            <div class="action-buttons">
              <button 
                @click="updateGenre"
                class="btn btn-warning btn-sm"
                data-test="update-genre-button"
              >
                Save
              </button>
              <button 
                @click="cancelEditing"
                class="btn btn-sm"
                data-test="cancel-edit-button"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="right-panel">
        <h3 class="panel-title">Add New</h3>
        
        <form @submit.prevent="addGenre">
          <div class="form-group">
            <label for="genre-name" class="form-label">Name</label>
            <input 
              id="genre-name"
              v-model="newGenre.name" 
              class="form-control" 
              placeholder="Enter genre name" 
              required 
              data-test="new-genre-name-input"
            />
          </div>
          
          <div class="form-group-large">
            <label for="genre-description" class="form-label">Description</label>
            <textarea 
              id="genre-description"
              v-model="newGenre.description" 
              class="form-control" 
              placeholder="Enter genre description"
              rows="3"
              data-test="new-genre-description-input"
            ></textarea>
          </div>
          
          <div class="action-buttons">
            <button 
              type="submit" 
              class="btn"
              data-test="save-new-genre-button"
            >
              Save New Genre
            </button>
            <button 
              type="button" 
              class="btn btn-secondary"
              @click="newGenre = { name: '', description: '' }"
              data-test="clear-new-genre-button"
            >
              Clear
            </button>
          </div>
        </form>
      </div>
    </div>

    <div 
      v-if="successMessage" 
      class="alert alert-success"
      data-test="success-message"
    >
      {{ successMessage }}
    </div>

    <div 
      v-if="error" 
      class="alert alert-danger"
      data-test="error-message"
    >
      {{ error }}
    </div>
  </div>
</template>

