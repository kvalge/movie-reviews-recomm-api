<script setup lang="ts">
import { GenreService } from '../services/GenreService'
import { useEntityManagement } from '../composables/useEntityManagement'
import type { Genre, GenreResponse } from '../domain/genre'

const genreService = new GenreService()

const config = {
  service: genreService,
  entityName: 'Genre',
  searchFields: ['name'] as (keyof GenreResponse)[],
  createEmptyEntity: (): Genre => ({
    name: '',
    description: ''
  })
}

const {
  entities: genres,
  newEntity: newGenre,
  selectedEntity: selectedGenre,
  searchText,
  error,
  successMessage,
  showDropdown,
  isEditing,
  filteredEntities: filteredGenres,
  addEntity: addGenre,
  updateEntity: updateGenre,
  deleteEntity: deleteGenre,
  selectEntity: selectGenre,
  onSearchFocus,
  onSearchInput,
  onSearchBlur,
  clearSelection,
  startEditing,
  cancelEditing,
  clearNewEntity: clearNewGenre
} = useEntityManagement(config)
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
              @click="clearNewGenre"
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

