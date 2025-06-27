export interface UserResponse {
  id: number
  username: string
  email: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: UserResponse
}