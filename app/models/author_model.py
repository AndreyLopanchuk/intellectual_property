from typing import TYPE_CHECKING

from sqlalchemy import Date, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.book_model import Book


class Author(Base):
    """
    Модель автора.

    Attributes:
        first_name (str): Имя автора.
        last_name (str): Фамилия автора.
        birth_date (Date): Дата рождения автора.
        books (list[Book]): Книги, связанные с автором.
    """

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[Date] = mapped_column(Date)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("first_name", "last_name", "birth_date"),)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
