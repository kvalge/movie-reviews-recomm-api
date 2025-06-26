<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  id: string
  label: string
  modelValue: string
  type?: 'text' | 'email' | 'password' | 'number'
  required?: boolean
  disabled?: boolean
  errors?: string[]
  placeholder?: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  required: false,
  disabled: false,
  errors: () => [],
  placeholder: ''
})

const emit = defineEmits<Emits>()

const updateValue = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const hasErrors = computed(() => props.errors && props.errors.length > 0)
</script>

<template>
  <div class="form-group mb-3">
    <label :for="id" class="form-label">
      {{ label }}
      <span v-if="required" class="text-danger">*</span>
    </label>
    
    <input 
      :id="id" 
      :type="type"
      :value="modelValue"
      @input="updateValue"
      class="form-control"
      :class="{ 'is-invalid': hasErrors }"
      :disabled="disabled"
      :required="required"
      :placeholder="placeholder"
    />
    
    <div v-if="hasErrors" class="invalid-feedback">
      <div v-for="(error, index) in errors" :key="index">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.invalid-feedback {
  display: block;
}
</style> 