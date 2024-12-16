from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_model import Book
from app.repository.book_repository import BookRepository
from app.schemas.book_schema import BookCreate
from app.services.author_service import AuthorService
from app.services.base_service import BaseService, DeleterService


class BookService(BaseService, DeleterService):
    """
    Сервис для работы с книгами.

    Attributes:
        session (AsyncSession): Сессия базы данных.
        repository (BookRepository): Репозиторий для работы с книгами.
        obj_db_by_id (Book | None): Атрибут для хранения модели Книги полученной по входящему идентификатору.
    """

    def __init__(self, async_session: AsyncSession):
        self.session = async_session
        self.repository: BookRepository = BookRepository(session=async_session)
        self.obj_db_by_id: Book | None = None
        super().__init__(repository=self.repository, obj_message="Book", obj_db_by_id=self.obj_db_by_id)

    async def create_book(self, book_in: BookCreate) -> Book:
        """
        Добвавление новой книги.

        Args:
            book_in (BookCreate): Данные для новой книги.

        Returns:
            Book: Модель добавленной книги.

        Raises:
            HTTPException: Если автора нет в базе данных.
        """
        await self.author_exist_or_404(author_id=book_in.author_id)
        return await self.repository.create(obj_in=book_in)

    async def update_book(self, book_in: BookCreate) -> Book:
        """
        Обновление данных книги.

        Args:
            book_in (BookCreate): Данные для обновления книги.

        Returns:
            Book: Модель обновлённой книги.

        Raises:
            HTTPException: Если автора нет в базе данных.
        """
        await self.author_exist_or_404(author_id=book_in.author_id)
        return await self.repository.update(obj_db=self.obj_db_by_id, obj_in=book_in)

    async def author_exist_or_404(self, author_id: int):
        """
        Проверка существования автора книги в базе данных.

        Args:
            author_id (int): Идентификатор автора.

        Raises:
            HTTPException: Если автора нет в базе данных.
        """
        author_service = AuthorService(async_session=self.session)
        await author_service.store_obj_db_by_id_or_404(author_id)

    async def update_book_available(self, book_id: int, delta: int) -> None:
        """
        Обновление количеста доступных экземпляров книги.

        Args:
            book_id (int): Идентификатор книги.
            delta (int): Изменение количеста доступных экземпляров книги.
        """
        await self.repository.update_available(book_id=book_id, delta=delta)
