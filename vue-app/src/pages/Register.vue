<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { IdentityService } from '../services/IdentityService'

const username = ref('')
const email = ref('')
const password = ref('')

const errors = ref<{ [key: string]: string[] }>({})

const router = useRouter()

const register = async () => {
  errors.value = {}

  try {
    const result = await IdentityService.register(
      username.value,
      email.value,
      password.value
    )

    if (result.errorsByField) {
      errors.value = result.errorsByField
    } else if (result.errors) {
      errors.value._general = result.errors
    }

    if (result.data) {
      errors.value = {}
      await router.push('/login')
    }
  } catch (err) {
    errors.value._general = ['Registration failed']
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
          <div v-if="errors.username" class="text-danger mt-1">
            <div v-for="(msg, i) in errors.username" :key="i">{{ msg }}</div>
          </div>
        </div>

        <div class="form-group mb-3">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" class="form-control" />
          <div v-if="errors.email" class="text-danger mt-1">
            <div v-for="(msg, i) in errors.email" :key="i">{{ msg }}</div>
          </div>
        </div>

        <div class="form-group mb-3">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" class="form-control" />
          <div v-if="errors.password" class="text-danger mt-1">
            <div v-for="(msg, i) in errors.password" :key="i">{{ msg }}</div>
          </div>
        </div>

        <button type="submit" class="btn w-100">Register</button>

        <div v-if="errors._general" class="text-danger mt-3 text-center">
          <div v-for="(msg, i) in errors._general" :key="i">{{ msg }}</div>
        </div>
      </form>
    </div>
  </div>
</template>
