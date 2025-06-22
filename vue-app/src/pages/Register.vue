<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { IdentityService } from '../services/IdentityService'

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

const router = useRouter()

const register = async () => {
  try {
    const result = await IdentityService.register(
      username.value,
      email.value,
      password.value
    )

    if (result.errors) {
      error.value = result.errors.join(', ')
    } else {
      console.log('Registration successful:', result.data)
      error.value = ''
      await router.push('/')
    }
  } catch (err) {
    error.value = 'Registration failed'
    console.error(err)
  }
}
</script>


<template>
  <div class="container d-flex justify-content-center min-vh-100">
    <div class="w-100 register-box">
      <h1 class="text-center mb-4">Create Account</h1>
      <form @submit.prevent="register">
        <div class="form-group mb-3">
          <label for="username">Username</label>
          <input id="username" v-model="username" type="text" class="form-control" />
        </div>

        <div class="form-group mb-3">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" class="form-control" />
        </div>

        <div class="form-group mb-3">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" class="form-control" />
        </div>

        <button type="submit" class="btn w-100">Register</button>

        <div v-if="error" class="text-danger mt-3 text-center">{{ error }}</div>
      </form>
    </div>
  </div>
</template>


