<script setup lang="ts">
import Genre from "@/components/Genre.vue"
import Position from "@/components/Position.vue";
</script>

<template>
  <div class="container min-vh-100 py-4">
    <h1 class="text-center mb-4">Manage Movie Data</h1>

    <div >
      <Genre />
      <div class="mt-4"></div>
      <Position/>
    </div>
  </div>
</template>

