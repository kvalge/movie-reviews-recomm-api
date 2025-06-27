<script setup lang="ts">
import {RouterLink} from 'vue-router'
import {useAuthStore} from '../../stores/authStore'
import {useRouter} from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}

</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <RouterLink class="navbar-brand" to="/">Movies</RouterLink>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item active">
          <RouterLink class="nav-link" to="/">Home</RouterLink>
        </li>
      </ul>

      <ul class="navbar-nav ms-auto">
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <RouterLink class="nav-link" to="/register">Register</RouterLink>
        </li>
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <RouterLink class="nav-link" to="/login">Login</RouterLink>
        </li>
        <li class="nav-item" v-if="auth.isAuthenticated">
          <a class="nav-link" href="#" @click.prevent="handleLogout">Logout</a>
        </li>

      </ul>
    </div>
  </nav>
</template>
