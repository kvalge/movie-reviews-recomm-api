<script setup lang="ts">
import { CastAndCrewService } from '../services/CastAndCrewService'
import { useEntityManagement } from '../composables/useEntityManagement'
import type { CastAndCrew, CastAndCrewResponse } from '../domain/cast_and_crew'

const castAndCrewService = new CastAndCrewService()

const config = {
  service: castAndCrewService,
  entityName: 'Cast and Crew Member',
  searchFields: ['first_name', 'last_name', 'stage_name'] as (keyof CastAndCrewResponse)[],
  createEmptyEntity: (): CastAndCrew => ({
    first_name: '',
    last_name: '',
    stage_name: '',
    birth_date: '',
    image_url: '',
    description: ''
  })
}

const {
  entities: castAndCrew,
  newEntity: newCastAndCrew,
  selectedEntity: selectedCastAndCrew,
  searchText,
  error,
  successMessage,
  showDropdown,
  isEditing,
  filteredEntities: filteredCastAndCrew,
  addEntity: addCastAndCrew,
  updateEntity: updateCastAndCrew,
  deleteEntity: deleteCastAndCrew,
  selectEntity: selectCastAndCrew,
  onSearchFocus,
  onSearchInput,
  onSearchBlur,
  clearSelection,
  startEditing,
  cancelEditing,
  clearNewEntity: clearNewCastAndCrew
} = useEntityManagement(config)

const getDisplayName = (member: CastAndCrewResponse) => {
  return member.stage_name || `${member.first_name} ${member.last_name}`
}
</script>

<template>
  <div class="page-container">
    <h3>Cast and Crew</h3>
    
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
            data-test="cast-and-crew-search-input"
          />
          
          <div v-if="showDropdown" class="custom-dropdown-menu">
            <div
              v-for="member in filteredCastAndCrew"
              :key="member.id"
              @mousedown.prevent="selectCastAndCrew(member)"
              data-test="dropdown-cast-and-crew-item"
              class="custom-dropdown-item dropdown-item-hover"
            >
              <strong>{{ getDisplayName(member) }}</strong>
            </div>
            <div v-if="filteredCastAndCrew.length === 0" class="dropdown-no-results">
              No cast and crew members found
            </div>
          </div>
        </div>

        <div v-if="selectedCastAndCrew" class="selected-item" data-test="selected-cast-and-crew">
          <div v-if="!isEditing">
            <h4>{{ getDisplayName(selectedCastAndCrew) }}</h4>
            <p><strong>Name:</strong> {{ selectedCastAndCrew.first_name }} {{ selectedCastAndCrew.last_name }}</p>
            <p v-if="selectedCastAndCrew.stage_name"><strong>Stage Name:</strong> {{ selectedCastAndCrew.stage_name }}</p>
            <p v-if="selectedCastAndCrew.birth_date"><strong>Birth Date:</strong> {{ selectedCastAndCrew.birth_date }}</p>
            <p v-if="selectedCastAndCrew.image_url"><strong>Image URL:</strong> {{ selectedCastAndCrew.image_url }}</p>
            <p v-if="selectedCastAndCrew.description"><strong>Description:</strong> {{ selectedCastAndCrew.description }}</p>
            
            <div class="action-buttons">
              <button 
                @click="startEditing"
                class="btn btn-warning btn-sm"
                data-test="edit-cast-and-crew-button"
              >
                Edit
              </button>
              <button 
                @click="deleteCastAndCrew"
                class="btn btn-danger btn-sm"
                data-test="delete-cast-and-crew-button"
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
              <label class="form-label">First Name</label>
              <input 
                v-model="selectedCastAndCrew.first_name"
                class="form-control"
                data-test="edit-cast-and-crew-first-name-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Last Name</label>
              <input 
                v-model="selectedCastAndCrew.last_name"
                class="form-control"
                data-test="edit-cast-and-crew-last-name-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Stage Name</label>
              <input 
                v-model="selectedCastAndCrew.stage_name"
                class="form-control"
                data-test="edit-cast-and-crew-stage-name-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Birth Date</label>
              <input 
                v-model="selectedCastAndCrew.birth_date"
                type="date"
                class="form-control"
                data-test="edit-cast-and-crew-birth-date-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Image URL</label>
              <input 
                v-model="selectedCastAndCrew.image_url"
                class="form-control"
                data-test="edit-cast-and-crew-image-url-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea 
                v-model="selectedCastAndCrew.description"
                class="form-control"
                rows="3"
                data-test="edit-cast-and-crew-description-input"
              ></textarea>
            </div>
            
            <div class="action-buttons">
              <button 
                @click="updateCastAndCrew"
                class="btn btn-warning btn-sm"
                data-test="update-cast-and-crew-button"
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
        
        <form @submit.prevent="addCastAndCrew">
          <div class="form-group">
            <label for="cast-and-crew-first-name" class="form-label">First Name</label>
            <input 
              id="cast-and-crew-first-name"
              v-model="newCastAndCrew.first_name" 
              class="form-control" 
              placeholder="Enter first name" 
              data-test="new-cast-and-crew-first-name-input"
            />
          </div>
          
          <div class="form-group">
            <label for="cast-and-crew-last-name" class="form-label">Last Name</label>
            <input 
              id="cast-and-crew-last-name"
              v-model="newCastAndCrew.last_name" 
              class="form-control" 
              placeholder="Enter last name"
              data-test="new-cast-and-crew-last-name-input"
            />
          </div>
          
          <div class="form-group">
            <label for="cast-and-crew-stage-name" class="form-label">Stage Name</label>
            <input 
              id="cast-and-crew-stage-name"
              v-model="newCastAndCrew.stage_name" 
              class="form-control" 
              placeholder="Enter stage name"
              data-test="new-cast-and-crew-stage-name-input"
            />
          </div>
          
          <div class="form-group">
            <label for="cast-and-crew-birth-date" class="form-label">Birth Date</label>
            <input 
              id="cast-and-crew-birth-date"
              v-model="newCastAndCrew.birth_date" 
              type="date"
              class="form-control"
              data-test="new-cast-and-crew-birth-date-input"
            />
          </div>
          
          <div class="form-group">
            <label for="cast-and-crew-image-url" class="form-label">Image URL</label>
            <input 
              id="cast-and-crew-image-url"
              v-model="newCastAndCrew.image_url" 
              class="form-control" 
              placeholder="Enter image URL"
              data-test="new-cast-and-crew-image-url-input"
            />
          </div>
          
          <div class="form-group-large">
            <label for="cast-and-crew-description" class="form-label">Description</label>
            <textarea 
              id="cast-and-crew-description"
              v-model="newCastAndCrew.description" 
              class="form-control" 
              placeholder="Enter description"
              rows="3"
              data-test="new-cast-and-crew-description-input"
            ></textarea>
          </div>
          
          <div class="action-buttons">
            <button 
              type="submit" 
              class="btn"
              data-test="save-new-cast-and-crew-button"
            >
              Save New Cast/Crew Member
            </button>
            <button 
              type="button" 
              class="btn btn-secondary"
              @click="clearNewCastAndCrew"
              data-test="clear-new-cast-and-crew-button"
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
