<script setup lang="ts">
import { PositionService } from '../services/PositionService'
import { useEntityManagement } from '../composables/useEntityManagement'
import type { Position, PositionResponse } from '../domain/position'

const positionService = new PositionService()

const config = {
  service: positionService,
  entityName: 'Position',
  searchFields: ['name'] as (keyof PositionResponse)[],
  createEmptyEntity: (): Position => ({
    name: '',
    description: ''
  })
}

const {
  entities: positions,
  newEntity: newPosition,
  selectedEntity: selectedPosition,
  searchText,
  error,
  successMessage,
  showDropdown,
  isEditing,
  filteredEntities: filteredPositions,
  addEntity: addPosition,
  updateEntity: updatePosition,
  deleteEntity: deletePosition,
  selectEntity: selectPosition,
  onSearchFocus,
  onSearchInput,
  onSearchBlur,
  clearSelection,
  startEditing,
  cancelEditing,
  clearNewEntity: clearNewPosition
} = useEntityManagement(config)
</script>

<template>
  <div class="page-container">
    <h3>Positions</h3>

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
            data-test="position-search-input"
          />

          <div v-if="showDropdown" class="custom-dropdown-menu">
            <div
              v-for="position in filteredPositions"
              :key="position.id"
              @mousedown.prevent="selectPosition(position)"
              data-test="dropdown-position-item"
              class="custom-dropdown-item dropdown-item-hover"
            >
              <strong>{{ position.name }}</strong>
            </div>
            <div v-if="filteredPositions.length === 0" class="dropdown-no-results">
              No positions found
            </div>
          </div>
        </div>

        <div v-if="selectedPosition" class="selected-item" data-test="selected-position">
          <div v-if="!isEditing">
            <h4>{{ selectedPosition.name }}</h4>
            <p>{{ selectedPosition.description }}</p>

            <div class="action-buttons">
              <button
                @click="startEditing"
                class="btn btn-warning btn-sm"
                data-test="edit-position-button"
              >
                Edit
              </button>
              <button
                @click="deletePosition"
                class="btn btn-danger btn-sm"
                data-test="delete-position-button"
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
                v-model="selectedPosition.name"
                class="form-control"
                data-test="edit-position-name-input"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea
                v-model="selectedPosition.description"
                class="form-control"
                rows="3"
                data-test="edit-position-description-input"
              ></textarea>
            </div>

            <div class="action-buttons">
              <button
                @click="updatePosition"
                class="btn btn-warning btn-sm"
                data-test="update-position-button"
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

        <form @submit.prevent="addPosition">
          <div class="form-group">
            <label for="position-name" class="form-label">Name</label>
            <input
              id="position-name"
              v-model="newPosition.name"
              class="form-control"
              placeholder="Enter position name"
              required
              data-test="new-position-name-input"
            />
          </div>

          <div class="form-group-large">
            <label for="position-description" class="form-label">Description</label>
            <textarea
              id="position-description"
              v-model="newPosition.description"
              class="form-control"
              placeholder="Enter position description"
              rows="3"
              data-test="new-position-description-input"
            ></textarea>
          </div>

          <div class="action-buttons">
            <button
              type="submit"
              class="btn"
              data-test="save-new-position-button"
            >
              Save New Position
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              @click="clearNewPosition"
              data-test="clear-new-position-button"
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

