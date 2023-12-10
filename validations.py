from pydantic import BaseModel


class BagreIn(BaseModel):
    specie: str
    weight: float
    size: int
    color: str


class BagreEdit(BaseModel):
    specie: str|None = None
    weight: float|None = None
    size: int|None = None
    color: str|None = None


class BagreOut(BaseModel):
    id: str
    specie: str
    weight: float
    size: int
    color: str


class UserCredentials(BaseModel):
    username: str
    password: str