from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.author_model import Author
    from app.models.borrow_model import Borrow


class Book(Base):
    """
    Модель книги.

    Attributes:
        title (str): Название книги.
        description (str): Описание книги.
        author_id (int): Идентификатор автора.
        available (int): Количество доступных экземпляров книги.
        author (Author): Автор, связанный с книгой.
        borrows (list[Borrow]): Выдачи, связанные с книгой.
    """

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(500))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))
    available: Mapped[int]

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("title", "author_id"),)

    def __str__(self):
        return self.title
