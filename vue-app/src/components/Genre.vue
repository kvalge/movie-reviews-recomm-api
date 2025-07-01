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
    <h2>Manage Genres</h2>
    
    <div class="split-container">
      <div class="left-panel">
        <h3 class="panel-title">Select Genre</h3>
        
        <div class="dropdown-container" style="position: relative;">
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
          
          <div 
            v-if="showDropdown"
            style="
              position: absolute;
              top: 100%;
              left: 0;
              right: 0;
              z-index: 9999;
              background: white;
              border: 1px solid #ccc;
              border-radius: 5px;
              max-height: 200px;
              overflow-y: auto;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
              margin-top: 2px;
            "
          >
            <div
              v-for="genre in filteredGenres"
              :key="genre.id"
              @mousedown.prevent="selectGenre(genre)"
              data-test="dropdown-genre-item"
              class="dropdown-item-hover"
              style="
                padding: 0.5rem 1rem;
                cursor: pointer;
                border-bottom: 1px solid #eee;
                transition: background-color 0.2s;
              "
            >
              <strong>{{ genre.name }}</strong>
            </div>
            <div 
              v-if="filteredGenres.length === 0" 
              style="color: #999; font-style: italic; padding: 0.5rem 1rem;"
            >
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
                class="btn btn-sm"
                data-test="clear-selection-button"
              >
                Clear
              </button>
            </div>
          </div>
          
          <div v-else>
            <div style="margin-bottom: 1rem;">
              <label style="display: block; margin-bottom: 0.5rem; color: navy; font-weight: bold;">Name</label>
              <input 
                v-model="selectedGenre.name"
                class="form-control"
                data-test="edit-genre-name-input"
              />
            </div>
            
            <div style="margin-bottom: 1rem;">
              <label style="display: block; margin-bottom: 0.5rem; color: navy; font-weight: bold;">Description</label>
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

      <!-- Right Panel - Add New Genre -->
      <div class="right-panel">
        <h3 class="panel-title">Add New Genre</h3>
        
        <form @submit.prevent="addGenre">
          <div style="margin-bottom: 1rem;">
            <label for="genre-name" style="display: block; margin-bottom: 0.5rem; color: navy; font-weight: bold;">Name</label>
            <input 
              id="genre-name"
              v-model="newGenre.name" 
              class="form-control" 
              placeholder="Enter genre name" 
              required 
              data-test="new-genre-name-input"
            />
          </div>
          
          <div style="margin-bottom: 1.5rem;">
            <label for="genre-description" style="display: block; margin-bottom: 0.5rem; color: navy; font-weight: bold;">Description</label>
            <textarea 
              id="genre-description"
              v-model="newGenre.description" 
              class="form-control" 
              placeholder="Enter genre description"
              rows="3"
              data-test="new-genre-description-input"
            ></textarea>
          </div>
          
          <button 
            type="submit" 
            class="btn"
            data-test="save-new-genre-button"
          >
            Save New Genre
          </button>
        </form>
      </div>
    </div>

    <!-- Messages -->
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

