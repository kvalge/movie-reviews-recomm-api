import re

from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator('username')
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('Username is required.')
        v = v.strip()
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be between 3 and 20 characters.')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can contain only letters, numbers, and underscores.')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password is required.')
        v = v.strip()
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must include at least one uppercase letter.')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must include at least one number.')
        return v

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
