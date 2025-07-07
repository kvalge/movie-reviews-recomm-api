<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {IdentityService} from '../services/IdentityService.ts'
import {useAuthStore} from '../stores/authStore.ts'

const router = useRouter()
const authStore = useAuthStore()

const identifier = ref('')
const password = ref('')
const errors = ref<{ [key: string]: string[] }>({})

const clearErrors = () => {
  errors.value = {}
}

const login = async () => {
  clearErrors()

  try {
    const result = await IdentityService.login(identifier.value, password.value)

    if (result.data) {
      authStore.setAuth(result.data.access_token, result.data.user)
      await router.push('/')
    } else {
      if (result.errors) {
        errors.value._general = result.errors
      } else if (result.errorsByField) {
        errors.value = result.errorsByField
      } else {
        errors.value._general = ['Login failed. Please try again.']
      }
    }
  } catch (e) {
    errors.value._general = ['Login failed. Please try again.']
  }
}
</script>

<template>
  <div class="container d-flex justify-content-center min-vh-100">
    <div class="w-100 register-box">
      <h1 class="text-center mb-4">Login</h1>
      <form @submit.prevent="login">

        <div class="form-group mb-3">
          <label for="identifier">Username or email</label>
          <input id="identifier" v-model="identifier" type="text" class="form-control"/>
        </div>

        <div class="form-group mb-3">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" class="form-control"/>
        </div>

        <button type="submit" class="btn w-100">Login</button>

        <button type="button" class="btn btn-outline-secondary mt-2 w-100"
                @click="() => { identifier = ''; password = ''; clearErrors() }">
          Reset
        </button>


        <div v-if="errors._general" class="alert alert-danger mt-3 w-100 text-center" role="alert">
          <div v-for="(msg, i) in errors._general" :key="i">{{ msg }}</div>
        </div>

      </form>
    </div>
  </div>
</template>

