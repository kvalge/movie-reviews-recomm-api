<script setup lang="ts">
import { GenreService } from '../services/GenreService'
import EntityManager from './EntityManager.vue'
import type { Genre, GenreResponse } from '../domain/genre'

const genreService = new GenreService()

const entityConfig = {
  service: genreService,
  entityName: 'Genre',
  searchFields: ['name'] as (keyof GenreResponse)[],
  createEmptyEntity: (): Genre => ({
    name: '',
    description: ''
  })
}

const fields = [
  { name: 'name', label: 'Name', type: 'text' as const, placeholder: 'Enter genre name', required: true },
  { name: 'description', label: 'Description', type: 'textarea' as const, placeholder: 'Enter genre description', rows: 3 }
]

const getDisplayName = (genre: GenreResponse) => genre.name
</script>

<template>
  <EntityManager
    title="Genres"
    :entity-config="entityConfig"
    :fields="fields"
    :get-display-name="getDisplayName"
    test-prefix="genre"
  />
</template> 