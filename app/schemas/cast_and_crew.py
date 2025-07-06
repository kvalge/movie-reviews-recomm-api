from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date

class CastAndCrewBase(BaseModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    stage_name: Optional[str] = Field(default=None)
    birth_date: Optional[date] = Field(default=None, description="Date of birth in YYYY-MM-DD format")
    image_url: Optional[str] = Field(default=None, description="Public URL to an image")
    description: Optional[str] = Field(default=None)

    @field_validator('first_name', 'last_name', 'stage_name', 'description', mode='before')
    def empty_str_to_none(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        return v

    @field_validator('birth_date', mode='before')
    def empty_date_to_none(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        return v

    @field_validator('image_url', mode='before')
    def validate_image_url(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        if isinstance(v, str) and not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v.strip()

class CastAndCrewCreate(CastAndCrewBase):
    pass

class CastAndCrewUpdate(CastAndCrewBase):
    pass

class CastAndCrewOut(CastAndCrewBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
