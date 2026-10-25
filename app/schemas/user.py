from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str


class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    email: str | None = None
