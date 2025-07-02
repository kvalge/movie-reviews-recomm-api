from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional

def validate_name_no_digits(v: str) -> str:
    if any(char.isdigit() for char in v):
        raise ValueError('Name must not contain digits')
    return v

class GenreBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    @field_validator('name')
    def name_validator(cls, v):
        return validate_name_no_digits(v)

class GenreCreate(GenreBase):
    pass

class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    @field_validator('name')
    def name_validator(cls, v):
        if v is None:
            return v
        return validate_name_no_digits(v)

class GenreOut(GenreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
