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
    mockGetAll.mockResolvedValue({ data: [] })
    mockAdd.mockResolvedValue({ data: { id: 1, name: 'Test', description: 'Test' } })
  })

  it('should mount without errors', () => {
    const wrapper = mount(Genre)
    expect(wrapper.exists()).toBe(true)
  })

  it('should call genre service on mount', () => {
    mount(Genre)
    expect(mockGetAll).toHaveBeenCalled()
  })
}) 