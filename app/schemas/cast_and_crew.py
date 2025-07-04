from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, HttpUrl, field_validator
from datetime import date

class CastAndCrewBase(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    stage_name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None, description="Date of birth in YYYY-MM-DD format")
    image_url: Optional[str] = Field(None, description="Public URL to an image")
    description: Optional[str] = Field(None, max_length=500)

    @field_validator('image_url', mode='before')
    def validate_image_url(cls, v):
        if v is None:
            return v
        # Convert HttpUrl to string if it's a valid URL
        if isinstance(v, str):
            # Basic URL validation
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('URL must start with http:// or https://')
            return v
        return str(v)

class CastAndCrewCreate(CastAndCrewBase):
    pass

class CastAndCrewUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    stage_name: Optional[str] = Field(None, min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None, description="Date of birth in YYYY-MM-DD format")
    image_url: Optional[str] = Field(None, description="Public URL to an image")
    description: Optional[str] = Field(None, max_length=500)

    @field_validator('image_url', mode='before')
    def validate_image_url(cls, v):
        if v is None:
            return v
        # Convert HttpUrl to string if it's a valid URL
        if isinstance(v, str):
            # Basic URL validation
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('URL must start with http:// or https://')
            return v
        return str(v)

class CastAndCrewOut(CastAndCrewBase):
    id: int
    model_config = ConfigDict(from_attributes=True)