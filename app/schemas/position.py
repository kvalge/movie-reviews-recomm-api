from pydantic import BaseModel, Field, ConfigDict


class PositionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=500)


class PositionOut(PositionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)