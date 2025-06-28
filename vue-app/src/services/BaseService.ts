import axios from 'axios'

export abstract class BaseService {
  protected static axios = axios.create({
    baseURL: '/api/',
    headers: {
      common: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    },
  })
}
