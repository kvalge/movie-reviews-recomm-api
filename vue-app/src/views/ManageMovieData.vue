<script setup lang="ts">
import Genre from "@/components/Genre.vue"
import Position from "@/components/Position.vue";
import CastAndCrew from "@/components/CastAndCrew.vue";
</script>

<template>
  <div class="container min-vh-100 py-4">
    <div >
      <Genre />
      <div class="mt-4"></div>
      <Position/>
      <div class="mt-4"></div>
      <CastAndCrew/>
    </div>
  </div>
</template>

