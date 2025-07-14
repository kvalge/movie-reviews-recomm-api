<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { CastAndCrewService } from '../services/CastAndCrewService'
import { CountryService } from '../services/CountryService'
import EntityManager from './EntityManager.vue'
import type { CastAndCrew, CastAndCrewResponse } from '../domain/cast_and_crew'
import type { CountryResponse } from '../domain/country'

const castAndCrewService = new CastAndCrewService()
const countryService = new CountryService()
const countries = ref<CountryResponse[]>([])

const loadCountries = async () => {
  try {
    const response = await countryService.getAll()
    if (response.data) {
      countries.value = response.data
    }
  } catch (err) {
    console.error('Error loading countries:', err)
  }
}

const entityConfig = {
  service: castAndCrewService,
  entityName: 'Cast and Crew Member',
  searchFields: ['first_name', 'last_name', 'stage_name'] as (keyof CastAndCrewResponse)[],
  createEmptyEntity: (): CastAndCrew => ({
    first_name: '',
    last_name: '',
    stage_name: '',
    birth_date: '',
    image_url: '',
    description: '',
    country_ids: []
  })
}

const fields = computed(() => [
  { name: 'first_name', label: 'First Name', type: 'text' as const, placeholder: 'Enter first name' },
  { name: 'last_name', label: 'Last Name', type: 'text' as const, placeholder: 'Enter last name' },
  { name: 'stage_name', label: 'Stage Name', type: 'text' as const, placeholder: 'Enter stage name' },
  { name: 'birth_date', label: 'Birth Date', type: 'date' as const },
  { name: 'image_url', label: 'Image URL', type: 'url' as const, placeholder: 'Enter image URL' },
  { name: 'description', label: 'Description', type: 'textarea' as const, placeholder: 'Enter description', rows: 3 },
  { 
    name: 'country_ids', 
    label: 'Countries', 
    type: 'multiselect' as const, 
    options: countries.value,
    optionLabel: 'name',
    optionValue: 'id'
  }
])

const getDisplayName = (member: CastAndCrewResponse) => {
  return member.stage_name || `${member.first_name} ${member.last_name}`
}

onMounted(loadCountries)
</script>

<template>
  <EntityManager
    title="Cast and Crew"
    :entity-config="entityConfig"
    :fields="fields"
    :get-display-name="getDisplayName"
    test-prefix="cast-and-crew"
  />
</template>

