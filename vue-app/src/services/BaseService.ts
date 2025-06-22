import axios from 'axios'

export abstract class BaseService {
  protected static axios = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
      common: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    },
  })
}
