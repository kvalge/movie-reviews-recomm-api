import { BaseEntityService } from './BaseEntityService';
import type { Country } from '../domain/country';
import type { CountryResponse } from '../domain/country'

export class CountryService extends BaseEntityService<Country, CountryResponse> {
  protected resourceUrl = 'countries';
}