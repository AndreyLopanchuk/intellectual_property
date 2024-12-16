from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.book_model import Book


class Borrow(Base):
    """
    Модель выдачи книг.

    Attributes:
        book_id (int): Идентификатор книги.
        reader_name (str): Имя читателя.
        borrow_date (datetime): Дата взятия книги.
        return_date (datetime | None): Дата возврата книги.
        book (Book): Книга, связанная с выдачей.
    """

    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"))
    reader_name: Mapped[str] = mapped_column(String(50))
    borrow_date: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    return_date: Mapped[datetime | None]

    book: Mapped["Book"] = relationship("Book", back_populates="borrows")
