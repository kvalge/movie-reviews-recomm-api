import { BaseEntityService } from './BaseEntityService';
import type { Genre } from '../domain/genre';
import type { GenreResponse } from '../domain/genre';

export class GenreService extends BaseEntityService<Genre, GenreResponse> {
  protected resourceUrl = 'genres';
}
