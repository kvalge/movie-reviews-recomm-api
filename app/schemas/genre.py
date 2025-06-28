from pydantic import BaseModel, Field, field_validator


class GenreBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    @field_validator('name')
    def name_must_not_contain_digits(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError('Name must not contain digits')
        return v


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=500)

    @field_validator('name')
    def name_must_not_contain_digits(cls, v):
        if v is not None and any(char.isdigit() for char in v):
            raise ValueError('Name must not contain digits')
        return v


class GenreOut(GenreBase):
    id: int

    class Config:
        orm_mode = True
