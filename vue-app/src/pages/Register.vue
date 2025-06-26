<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { IdentityService, type ServiceResponse, type UserResponse } from '../services/IdentityService'
import FormField from '../components/FormField.vue'

interface FormData {
  username: string
  email: string
  password: string
}

interface FormErrors {
  [key: string]: string[]
}

const formData = reactive<FormData>({
  username: '',
  email: '',
  password: ''
})

const errors = ref<FormErrors>({})
const isLoading = ref(false)

const router = useRouter()

const clearErrors = () => {
  errors.value = {}
}

const setErrors = (result: ServiceResponse<UserResponse>) => {
  if (result.errorsByField) {
    errors.value = result.errorsByField
  } else if (result.errors) {
    errors.value._general = result.errors
  }
}

const register = async () => {
  clearErrors()
  isLoading.value = true

  try {
    const result = await IdentityService.register(
      formData.username,
      formData.email,
      formData.password
    )

    if (result.data) {
      clearErrors()
      await router.push('/login')
    } else {
      setErrors(result)
    }
  } catch (err) {
    errors.value._general = ['Registration failed']
    console.error('Registration error:', err)
  } finally {
    isLoading.value = false
  }
}

const resetForm = () => {
  Object.assign(formData, {
    username: '',
    email: '',
    password: ''
  })
  clearErrors()
}
</script>

<template>
  <div class="container d-flex justify-content-center min-vh-100">
    <div class="w-100 register-box">
      <h1 class="text-center mb-4">Create Account</h1>
      
      <form @submit.prevent="register" novalidate>
        <FormField
          id="username"
          label="Username"
          v-model="formData.username"
          type="text"
          :required="true"
          :disabled="isLoading"
          :errors="errors.username"
          placeholder="Enter your username"
        />

        <FormField
          id="email"
          label="Email"
          v-model="formData.email"
          type="email"
          :required="true"
          :disabled="isLoading"
          :errors="errors.email"
          placeholder="Enter your email"
        />

        <FormField
          id="password"
          label="Password"
          v-model="formData.password"
          type="password"
          :required="true"
          :disabled="isLoading"
          :errors="errors.password"
          placeholder="Enter your password"
        />

        <div class="d-grid gap-2">
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
            {{ isLoading ? 'Registering...' : 'Register' }}
          </button>
          
          <button 
            type="button" 
            class="btn btn-outline-secondary"
            @click="resetForm"
            :disabled="isLoading"
          >
            Reset Form
          </button>
        </div>

        <div v-if="errors._general" class="alert alert-danger mt-3">
          <div v-for="(msg, i) in errors._general" :key="i">{{ msg }}</div>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.register-box {
  max-width: 400px;
}
</style>
