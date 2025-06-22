<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from './layout/Header.vue'
</script>

<template>
  <div class="app-wrapper">
    <Header />
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>
