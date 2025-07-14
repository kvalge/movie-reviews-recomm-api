from pydantic import BaseModel, ConfigDict


class CountryBase(BaseModel):
    code: str
    name: str


class CountryOut(CountryBase):
    id: int
    model_config = ConfigDict(from_attributes=True) 