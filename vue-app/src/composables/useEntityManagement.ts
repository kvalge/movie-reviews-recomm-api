import { ref, computed, onMounted, nextTick } from 'vue'
import type { BaseEntityService } from '../services/BaseEntityService'

export interface EntityConfig<T, TResponse> {
  service: BaseEntityService<T, TResponse>
  entityName: string
  searchFields: (keyof TResponse)[]
  createEmptyEntity: () => T
}

export function useEntityManagement<T, TResponse extends { id: number }>(
  config: EntityConfig<T, TResponse>
) {
  const entities = ref<TResponse[]>([])
  const newEntity = ref<T>(config.createEmptyEntity())
  const selectedEntity = ref<TResponse | null>(null)
  const searchText = ref('')
  const error = ref<string | null>(null)
  const successMessage = ref<string | null>(null)
  const showDropdown = ref(false)
  const isEditing = ref(false)

  const loadEntities = async () => {
    try {
      const response = await config.service.getAll()
      entities.value = response.data || []
    } catch (err) {
      console.error(`Error loading ${config.entityName}:`, err)
      error.value = `Failed to load ${config.entityName}`
    }
  }

  const addEntity = async () => {
    error.value = null
    const dataToSend = { ...newEntity.value }
    Object.keys(dataToSend).forEach(key => {
      if (typeof (dataToSend as any)[key] === 'string' && (dataToSend as any)[key].trim() === '') {
        (dataToSend as any)[key] = null
      }
    })
    
    const response = await config.service.add(dataToSend)
    if (response.data) {
      entities.value.push(response.data as any)
      newEntity.value = config.createEmptyEntity() as any
      showSuccessMessage(`${config.entityName} created successfully`)
    } else {
      // Handle validation errors by field or general errors
      if (response.errorsByField) {
        const fieldErrors = Object.values(response.errorsByField).flat()
        error.value = fieldErrors[0] || 'Add failed'
      } else {
        error.value = response.errors?.[0] || 'Add failed'
      }
    }
  }

  const updateEntity = async () => {
    if (!selectedEntity.value) return
    
    error.value = null
    const dataToSend = { ...selectedEntity.value }

    delete (dataToSend as any).id
    
    Object.keys(dataToSend).forEach(key => {
      if (typeof (dataToSend as any)[key] === 'string' && (dataToSend as any)[key].trim() === '') {
        (dataToSend as any)[key] = null
      }
    })
    
    const response = await config.service.update(selectedEntity.value.id, dataToSend)
    if (response.data) {
      const index = entities.value.findIndex(e => e.id === selectedEntity.value!.id)
      if (index !== -1) {
        entities.value[index] = response.data as any
        selectedEntity.value = response.data as TResponse
      }
      isEditing.value = false
      showSuccessMessage(`${config.entityName} updated successfully`)
    } else {
      if (response.errorsByField) {
        const fieldErrors = Object.values(response.errorsByField).flat()
        error.value = fieldErrors[0] || 'Update failed'
      } else {
        error.value = response.errors?.[0] || 'Update failed'
      }
    }
  }

  const deleteEntity = async () => {
    if (!selectedEntity.value) return
    
    error.value = null
    const response = await config.service.delete(selectedEntity.value.id)
    if (!response.errors) {
      entities.value = entities.value.filter(e => e.id !== selectedEntity.value!.id)
      selectedEntity.value = null
      searchText.value = ''
      isEditing.value = false
      showSuccessMessage(`${config.entityName} deleted successfully`)
    } else {
      error.value = response.errors[0] || 'Delete failed'
    }
  }

  const filteredEntities = computed(() => {
    if (!searchText.value.trim()) {
      return entities.value
    }
    
    return entities.value.filter(entity =>
      config.searchFields.some(field => {
        const value = (entity as any)[field]
        return value && String(value).toLowerCase().includes(searchText.value.toLowerCase())
      })
    )
  })

  const selectEntity = (entity: TResponse) => {
    selectedEntity.value = { ...entity } as TResponse
    const searchField = config.searchFields[0] // Use first search field for display
    searchText.value = String(entity[searchField])
    showDropdown.value = false
    isEditing.value = false
  }

  const onSearchFocus = () => {
    showDropdown.value = true
  }

  const onSearchInput = () => {
    showDropdown.value = true
    error.value = null // Clear error when user starts typing
    if (!searchText.value.trim()) {
      selectedEntity.value = null
      isEditing.value = false
    }
  }

  const onSearchBlur = () => {
    setTimeout(() => {
      showDropdown.value = false
    }, 300)
  }

  const clearSelection = async () => {
    selectedEntity.value = null
    searchText.value = ''
    showDropdown.value = false
    isEditing.value = false
    error.value = null
    successMessage.value = null
    // Force reactivity update
    await nextTick()
  }

  const startEditing = () => {
    isEditing.value = true
    error.value = null // Clear error when starting to edit
  }

  const cancelEditing = () => {
    if (selectedEntity.value) {
      const original = entities.value.find(e => e.id === selectedEntity.value!.id)
      if (original) {
        selectedEntity.value = { ...original }
      }
    }
    isEditing.value = false
  }

  const clearNewEntity = async () => {
    newEntity.value = config.createEmptyEntity()
    error.value = null
    successMessage.value = null
    await nextTick()
  }

  const showSuccessMessage = (message: string) => {
    successMessage.value = message
    setTimeout(() => successMessage.value = null, 3000)
  }

  onMounted(loadEntities)

  return {
    entities,
    newEntity,
    selectedEntity,
    searchText,
    error,
    successMessage,
    showDropdown,
    isEditing,
    filteredEntities,
    loadEntities,
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
  }
} 