from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_model import Book
from app.repository.base_repository import BaseRepository, DeleterRepository
from app.repository.repository_errors import crud_error_handler


class BookRepository(BaseRepository, DeleterRepository):
    """
    Репозиторий для операций с книгами.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Book)
        self.session = session

    @crud_error_handler
    async def update_available(self, book_id: int, delta: int) -> None:
        """
        Обновляет количество доступных книг. без commit, для rollback в случае ошибки выдачи или возврата

        Args:
            book_id (int): Идентификатор книги.
            delta (int): Изменение количества доступных книг.

        Returns:
            None
        """
        stmt = update(Book).where(Book.id == book_id).values(available=Book.available + delta)
        await self.session.execute(stmt)
