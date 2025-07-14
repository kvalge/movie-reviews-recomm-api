import type { CountryResponse } from './country'

export interface CastAndCrew{
    first_name: string,
    last_name: string,
    stage_name: string,
    birth_date: string,
    image_url: string,
    description: string,
    country_ids?: number[]
}

export interface CastAndCrewResponse{
    id:number,
    first_name: string,
    last_name: string,
    stage_name: string,
    birth_date: string,
    image_url: string,
    description: string,
    countries: CountryResponse[]
}
