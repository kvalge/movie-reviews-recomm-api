from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class PositionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

class PositionCreate(PositionBase):
    pass

class PositionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class PositionOut(PositionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
