<script setup lang="ts">
import { useEntityManagement } from '../composables/useEntityManagement'
import type { EntityConfig } from '../composables/useEntityManagement'

interface FieldConfig {
  name: string
  label: string
  type: 'text' | 'textarea' | 'date' | 'url'
  placeholder?: string
  required?: boolean
  rows?: number
}

interface Props {
  title: string
  entityConfig: EntityConfig<any, any>
  fields: FieldConfig[]
  getDisplayName: (entity: any) => string
  testPrefix: string
}

const props = defineProps<Props>()

const {
  newEntity,
  selectedEntity,
  searchText,
  error,
  successMessage,
  showDropdown,
  isEditing,
  filteredEntities,
  addEntity,
  updateEntity,
  deleteEntity,
  selectEntity,
  onSearchFocus,
  onSearchInput,
  onSearchBlur,
  clearSelection,
  startEditing,
  cancelEditing,
  clearNewEntity
} = useEntityManagement(props.entityConfig)
</script>

<template>
  <div class="page-container">
    <h3>{{ title }}</h3>
    
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
            :data-test="`${testPrefix}-search-input`"
          />
          
          <div v-if="showDropdown" class="custom-dropdown-menu">
            <div
              v-for="entity in filteredEntities"
              :key="entity.id"
              @mousedown.prevent="selectEntity(entity)"
              :data-test="`dropdown-${testPrefix}-item`"
              class="custom-dropdown-item dropdown-item-hover"
            >
              <strong>{{ getDisplayName(entity) }}</strong>
            </div>
            <div v-if="filteredEntities.length === 0" class="dropdown-no-results">
              No {{ title.toLowerCase() }} found
            </div>
          </div>
        </div>

        <div v-if="selectedEntity" class="selected-item" :data-test="`selected-${testPrefix}`">
          <div v-if="!isEditing">
            <h4>{{ getDisplayName(selectedEntity) }}</h4>

            <div v-for="field in fields" :key="`display-${field.name}`">
              <p v-if="selectedEntity[field.name]">
                <strong>{{ field.label }}:</strong> {{ selectedEntity[field.name] }}
              </p>
            </div>
            
            <div class="action-buttons">
              <button 
                @click="startEditing"
                class="btn btn-warning btn-sm"
                :data-test="`edit-${testPrefix}-button`"
              >
                Edit
              </button>
              <button 
                @click="deleteEntity"
                class="btn btn-danger btn-sm"
                :data-test="`delete-${testPrefix}-button`"
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
            <div v-for="field in fields" :key="`edit-${field.name}`" class="form-group">
              <label class="form-label">{{ field.label }}</label>
              
              <input 
                v-if="field.type !== 'textarea'"
                v-model="selectedEntity[field.name]"
                :type="field.type === 'url' ? 'text' : field.type"
                class="form-control"
                :data-test="`edit-${testPrefix}-${field.name.replace('_', '-')}-input`"
              />
              
              <textarea 
                v-else
                v-model="selectedEntity[field.name]"
                class="form-control"
                :rows="field.rows || 3"
                :data-test="`edit-${testPrefix}-${field.name.replace('_', '-')}-input`"
              ></textarea>
            </div>
            
            <div class="action-buttons">
              <button 
                @click="updateEntity"
                class="btn btn-warning btn-sm"
                :data-test="`update-${testPrefix}-button`"
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
        
        <form @submit.prevent="addEntity">
          <div v-for="field in fields" :key="`new-${field.name}`" 
               :class="field.type === 'textarea' ? 'form-group-large' : 'form-group'">
            <label :for="`${testPrefix}-${field.name}`" class="form-label">{{ field.label }}</label>
            
            <input 
              v-if="field.type !== 'textarea'"
              :id="`${testPrefix}-${field.name}`"
              v-model="newEntity[field.name]"
              :type="field.type === 'url' ? 'text' : field.type"
              class="form-control"
              :placeholder="field.placeholder"
              :required="field.required"
              :data-test="`new-${testPrefix}-${field.name.replace('_', '-')}-input`"
            />
            
            <textarea 
              v-else
              :id="`${testPrefix}-${field.name}`"
              v-model="newEntity[field.name]"
              class="form-control"
              :placeholder="field.placeholder"
              :rows="field.rows || 3"
              :data-test="`new-${testPrefix}-${field.name.replace('_', '-')}-input`"
            ></textarea>
          </div>
          
          <div class="action-buttons">
            <button 
              type="submit" 
              class="btn"
              :data-test="`save-new-${testPrefix}-button`"
            >
              Save New {{ entityConfig.entityName }}
            </button>
            <button 
              type="button" 
              class="btn btn-secondary"
              @click="clearNewEntity"
              :data-test="`clear-new-${testPrefix}-button`"
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