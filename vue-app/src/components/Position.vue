<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { PositionService } from '../services/PositionService'
import type { Position, PositionResponse } from '../domain/position'

const positionService = new PositionService()

const positions = ref<PositionResponse[]>([])
const newPosition = ref<Position>({ name: '', description: '' })
const selectedPosition = ref<PositionResponse | null>(null)
const searchText = ref('')
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const showDropdown = ref(false)
const isEditing = ref(false)

const loadPositions = async () => {
  try {
    const response = await positionService.getAll()
    positions.value = response.data || []
  } catch (err) {
    console.error('Error loading positions:', err)
    error.value = 'Failed to load positions'
  }
}

const addPosition = async () => {
  const response = await positionService.add(newPosition.value)
  if (response.data) {
    positions.value.push(response.data)
    newPosition.value = { name: '', description: '' }
    successMessage.value = 'Position created successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors?.[0] || 'Add failed'
  }
}

const updatePosition = async () => {
  if (!selectedPosition.value) return

  const response = await positionService.update(selectedPosition.value.id, selectedPosition.value)
  if (response.data) {
    const index = positions.value.findIndex(p => p.id === selectedPosition.value!.id)
    if (index !== -1) {
      positions.value[index] = response.data
      selectedPosition.value = response.data
    }
    isEditing.value = false
    successMessage.value = 'Position updated successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors?.[0] || 'Update failed'
  }
}

const deletePosition = async () => {
  if (!selectedPosition.value) return

  const response = await positionService.delete(selectedPosition.value.id)
  if (!response.errors) {
    positions.value = positions.value.filter(p => p.id !== selectedPosition.value!.id)
    selectedPosition.value = null
    searchText.value = ''
    isEditing.value = false
    successMessage.value = 'Position deleted successfully'
    setTimeout(() => successMessage.value = null, 3000)
  } else {
    error.value = response.errors[0] || 'Delete failed'
  }
}

const filteredPositions = computed(() => {
  if (!searchText.value.trim()) {
    return positions.value
  }

  return positions.value.filter(p =>
    p.name.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

const selectPosition = (position: PositionResponse) => {
  selectedPosition.value = { ...position }
  searchText.value = position.name
  showDropdown.value = false
  isEditing.value = false
}

const onSearchFocus = () => {
  showDropdown.value = true
}

const onSearchInput = () => {
  showDropdown.value = true
  if (!searchText.value.trim()) {
    selectedPosition.value = null
    isEditing.value = false
  }
}

const onSearchBlur = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 300)
}

const clearSelection = () => {
  selectedPosition.value = null
  searchText.value = ''
  showDropdown.value = false
  isEditing.value = false
}

const startEditing = () => {
  isEditing.value = true
}

const cancelEditing = () => {
  if (selectedPosition.value) {
    const original = positions.value.find(p => p.id === selectedPosition.value!.id)
    if (original) {
      selectedPosition.value = { ...original }
    }
  }
  isEditing.value = false
}

onMounted(loadPositions)
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
              @click="newPosition = { name: '', description: '' }"
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

