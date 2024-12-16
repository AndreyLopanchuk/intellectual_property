from pydantic import BaseModel, conint


class BookCreate(BaseModel):
    title: str
    description: str
    author_id: int
    available: conint(ge=0)


class BookUpdate(BookCreate):
    pass


class BookFull(BookCreate):
    id: int
