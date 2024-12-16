from datetime import date

from pydantic import BaseModel


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date


class AuthorUpdate(AuthorCreate):
    pass


class AuthorFull(AuthorCreate):
    id: int
