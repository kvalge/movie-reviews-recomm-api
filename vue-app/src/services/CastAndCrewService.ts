import { BaseEntityService } from './BaseEntityService';
import type { CastAndCrew } from '../domain/cast_and_crew';
import type { CastAndCrewResponse } from '../domain/cast_and_crew';

export class CastAndCrewService extends BaseEntityService<CastAndCrew, CastAndCrewResponse> {
  protected resourceUrl = 'cast_and_crew';
} 