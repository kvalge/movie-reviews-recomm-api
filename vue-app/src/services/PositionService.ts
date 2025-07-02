import { BaseEntityService } from './BaseEntityService';
import type { Position } from '../domain/position';
import type { PositionResponse } from '../domain/position';

export class PositionService extends BaseEntityService<Position, PositionResponse> {
  protected resourceUrl = 'positions';
}
