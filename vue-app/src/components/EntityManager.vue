<script setup lang="ts">
import { useEntityManagement } from '../composables/useEntityManagement'
import type { EntityConfig } from '../composables/useEntityManagement'

interface FieldConfig {
  name: string
  label: string
  type: 'text' | 'textarea' | 'date' | 'url' | 'multiselect'
  placeholder?: string
  required?: boolean
  rows?: number
  options?: any[]
  optionLabel?: string
  optionValue?: string
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

const handleMultiselectUpdate = () => {
  if (selectedEntity.value) {
    props.fields.forEach(field => {
      if (field.type === 'multiselect') {
        const displayFieldName = field.name.replace('_ids', 's')
        const multiselectValue = (selectedEntity.value as any)[displayFieldName]
        if (Array.isArray(multiselectValue) && multiselectValue.length > 0) {
          if (typeof multiselectValue[0] === 'object') {
            ;(selectedEntity.value as any)[field.name] = multiselectValue.map(item => item[field.optionValue || 'id'])
          }
        } else {
          ;(selectedEntity.value as any)[field.name] = []
        }
      }
    })
  }
}

const updateEntityWithMultiselect = async () => {
  handleMultiselectUpdate()
  await updateEntity()
}
</script>

<template>
  <div class="page-container">
    <h4 class="text-center mb-4 mt-5">{{ title }}</h4>
    
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
              <p v-if="field.type === 'multiselect' && selectedEntity[field.name.replace('_ids', 's')] && selectedEntity[field.name.replace('_ids', 's')].length > 0">
                <strong>{{ field.label }}:</strong> 
                <span v-for="(item, index) in selectedEntity[field.name.replace('_ids', 's')]" :key="item[field.optionValue || 'id']">
                  {{ item[field.optionLabel || 'name'] }}<span v-if="index < selectedEntity[field.name.replace('_ids', 's')].length - 1">, </span>
                </span>
              </p>
              <p v-else-if="field.type !== 'multiselect' && selectedEntity[field.name]">
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
                v-if="field.type !== 'textarea' && field.type !== 'multiselect'"
                v-model="selectedEntity[field.name]"
                :type="field.type === 'url' ? 'text' : field.type"
                class="form-control"
                :data-test="`edit-${testPrefix}-${field.name.replace('_', '-')}-input`"
              />
              
              <select
                v-else-if="field.type === 'multiselect'"
                v-model="selectedEntity[field.name.replace('_ids', 's')]"
                multiple
                class="form-control"
                :data-test="`edit-${testPrefix}-${field.name.replace('_', '-')}-select`"
              >
                <option 
                  v-for="option in field.options" 
                  :key="option[field.optionValue || 'id']" 
                  :value="option"
                >
                  {{ option[field.optionLabel || 'name'] }}
                </option>
              </select>
              
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
                @click="updateEntityWithMultiselect"
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
              v-if="field.type !== 'textarea' && field.type !== 'multiselect'"
              :id="`${testPrefix}-${field.name}`"
              v-model="newEntity[field.name]"
              :type="field.type === 'url' ? 'text' : field.type"
              class="form-control"
              :placeholder="field.placeholder"
              :required="field.required"
              :data-test="`new-${testPrefix}-${field.name.replace('_', '-')}-input`"
            />
            
            <select
              v-else-if="field.type === 'multiselect'"
              :id="`${testPrefix}-${field.name}`"
              v-model="newEntity[field.name]"
              multiple
              class="form-control"
              :data-test="`new-${testPrefix}-${field.name.replace('_', '-')}-select`"
            >
              <option 
                v-for="option in field.options" 
                :key="option[field.optionValue || 'id']" 
                :value="option[field.optionValue || 'id']"
              >
                {{ option[field.optionLabel || 'name'] }}
              </option>
            </select>
            
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

<style scoped>
select[multiple] {
  height: 150px;
}
</style> 