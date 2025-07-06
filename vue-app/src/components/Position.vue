<script setup lang="ts">
import { PositionService } from '../services/PositionService'
import EntityManager from './EntityManager.vue'
import type { Position, PositionResponse } from '../domain/position'

const positionService = new PositionService()

const entityConfig = {
  service: positionService,
  entityName: 'Position',
  searchFields: ['name'] as (keyof PositionResponse)[],
  createEmptyEntity: (): Position => ({
    name: '',
    description: ''
  })
}

const fields = [
  { name: 'name', label: 'Name', type: 'text' as const, placeholder: 'Enter position name', required: true },
  { name: 'description', label: 'Description', type: 'textarea' as const, placeholder: 'Enter position description', rows: 3 }
]

const getDisplayName = (position: PositionResponse) => position.name
</script>

<template>
  <EntityManager
    title="Positions"
    :entity-config="entityConfig"
    :fields="fields"
    :get-display-name="getDisplayName"
    test-prefix="position"
  />
</template> 