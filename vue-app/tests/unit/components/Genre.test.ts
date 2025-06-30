import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Genre from '@/components/Genre.vue'

const mockGetAll = vi.fn()
const mockAdd = vi.fn()

vi.mock('@/services/GenreService', () => ({
  GenreService: vi.fn().mockImplementation(() => ({
    getAll: mockGetAll,
    add: mockAdd
  }))
}))

describe('Genre Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetAll.mockResolvedValue({
      data: [
        { id: 1, name: 'Action', description: 'Action movies' },
        { id: 2, name: 'Comedy', description: 'Comedy movies' }
      ]
    })
    mockAdd.mockResolvedValue({
      data: { id: 3, name: 'Drama', description: 'Drama movies' }
    })
  })

  it('renders genre management interface', () => {
    const wrapper = mount(Genre)
    
    expect(wrapper.find('h2').text()).toBe('Genres')
    expect(wrapper.find('input[placeholder="Name"]').exists()).toBe(true)
    expect(wrapper.find('input[placeholder="Description"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Save Genre')
    expect(wrapper.find('input[placeholder="Search by name..."]').exists()).toBe(true)
  })

  it('displays genres list', async () => {
    const wrapper = mount(Genre)

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0)) // Wait for async operations
    
    expect(wrapper.text()).toContain('Action')
    expect(wrapper.text()).toContain('Comedy')
    expect(wrapper.text()).toContain('Action movies')
    expect(wrapper.text()).toContain('Comedy movies')
  })

  it('adds new genre', async () => {
    const wrapper = mount(Genre)

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    await wrapper.find('input[placeholder="Name"]').setValue('Drama')
    await wrapper.find('input[placeholder="Description"]').setValue('Drama movies')

    await wrapper.find('form').trigger('submit')

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(mockAdd).toHaveBeenCalledWith({ name: 'Drama', description: 'Drama movies' })
  })

  it('filters genres by search', async () => {
    const wrapper = mount(Genre)

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    await wrapper.find('input[placeholder="Search by name..."]').setValue('Action')

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Action')
    expect(wrapper.text()).not.toContain('Comedy')
  })
}) 