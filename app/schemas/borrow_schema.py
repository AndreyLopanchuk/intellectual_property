from datetime import datetime

from pydantic import BaseModel


class BorrowCreate(BaseModel):
    book_id: int
    reader_name: str


class BorrowUpdate(BorrowCreate):
    id: int
    borrow_date: datetime


class BorrowResponse(BorrowCreate):
    id: int
    borrow_date: datetime
    return_date: datetime | None


class BorrowFull(BorrowCreate):
    id: int
    borrow_date: datetime
    return_date: datetime
