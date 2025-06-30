import { describe, it, expect, vi, beforeEach } from 'vitest'
import { GenreService } from '@/services/GenreService'

vi.mock('@/services/BaseEntityService')

describe('GenreService', () => {
  let genreService: GenreService

  beforeEach(() => {
    genreService = new GenreService()
  })

  it('creates genre service instance', () => {
    expect(genreService).toBeInstanceOf(GenreService)
  })

  it('has correct resource URL', () => {
    expect(genreService['resourceUrl']).toBe('genres')
  })

  it('can get all genres', async () => {
    const mockGenres = [
      { id: 1, name: 'Action', description: 'Action movies' },
      { id: 2, name: 'Comedy', description: 'Comedy movies' }
    ]
    
    vi.spyOn(genreService, 'getAll').mockResolvedValue({
      data: mockGenres,
      status: '200'
    })
    
    const result = await genreService.getAll()
    
    expect(result.data).toEqual(mockGenres)
    expect(genreService.getAll).toHaveBeenCalled()
  })

  it('can get genre by id', async () => {
    const mockGenre = { id: 1, name: 'Action', description: 'Action movies' }
    
    vi.spyOn(genreService, 'getById').mockResolvedValue({
      data: mockGenre,
      status: '200'
    })
    
    const result = await genreService.getById(1)
    
    expect(result.data).toEqual(mockGenre)
    expect(genreService.getById).toHaveBeenCalledWith(1)
  })

  it('can add a genre', async () => {
    const genreData = {
      name: 'Thriller',
      description: 'Thriller movies'
    }
    
    const mockResponse = { id: 3, ...genreData }
    
    vi.spyOn(genreService, 'add').mockResolvedValue({
      data: mockResponse,
      status: '201'
    })
    
    const result = await genreService.add(genreData)
    
    expect(result.data).toEqual(mockResponse)
    expect(genreService.add).toHaveBeenCalledWith(genreData)
  })

  it('can update a genre', async () => {
    const updateData = {
      name: 'Updated Action',
      description: 'Updated description'
    }
    
    const mockResponse = { id: 1, ...updateData }
    vi.spyOn(genreService, 'update').mockResolvedValue({
      data: mockResponse,
      status: '200'
    })
    
    const result = await genreService.update(1, updateData)
    
    expect(result.data).toEqual(mockResponse)
    expect(genreService.update).toHaveBeenCalledWith(1, updateData)
  })

  it('can delete a genre', async () => {
    vi.spyOn(genreService, 'delete').mockResolvedValue({
      status: '204'
    })
    
    const result = await genreService.delete(1)
    
    expect(result.status).toBe('204')
    expect(genreService.delete).toHaveBeenCalledWith(1)
  })
}) 