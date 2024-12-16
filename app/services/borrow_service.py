from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.borrow_model import Borrow
from app.repository.borrow_repository import BorrowRepository
from app.schemas.borrow_schema import BorrowCreate
from app.services.base_service import BaseService
from app.services.book_service import BookService


class BorrowService(BaseService):
    """
    Сервисный класс для управления выдачами книг.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
        repository (BorrowRepository): Репозиторий для операций с выдачами книг.
        obj_db_by_id (Borrow): Объект выдачи, полученный по входящему идентификатору.
    """

    def __init__(self, async_session: AsyncSession):
        self.session = async_session
        self.repository: BorrowRepository = BorrowRepository(session=async_session)
        self.obj_db_by_id: Borrow | None = None
        super().__init__(repository=self.repository, obj_message="Borrow", obj_db_by_id=self.obj_db_by_id)

    async def create_borrow(self, borrow_in: BorrowCreate) -> Borrow:
        """
        Создает новую выдачу.

        Args:
            borrow_in (BorrowCreate): Данные для создания выдачи.

        Returns:
            Borrow: Созданный объект выдачи.

        Raises:
            HTTPException: Если нет доступных экземпляров книги.
        """
        book_service: BookService = await self.store_book_db_by_id_or_404(book_id=borrow_in.book_id)
        if book_service.obj_db_by_id and book_service.obj_db_by_id.available <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="There are no copies of the book available"
            )

        await book_service.update_book_available(book_id=borrow_in.book_id, delta=-1)
        return await self.repository.create(obj_in=borrow_in)

    async def close_borrow(self) -> Borrow:
        """
        Закрывает выдачу.

        Returns:
            Borrow: Обновленный объект выдачи.

        Raises:
            HTTPException: Если книга уже возвращена.
        """
        book_service = await self.store_book_db_by_id_or_404(book_id=self.obj_db_by_id.book_id)
        if self.obj_db_by_id.return_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The book has already been returned")

        await book_service.update_book_available(book_id=self.obj_db_by_id.book_id, delta=1)
        return await self.repository.update(borrow_db=self.obj_db_by_id)

    async def store_book_db_by_id_or_404(self, book_id: int) -> BookService:
        """
        Получает книгу по идентификатору или вызывает исключение 404.

        Args:
            book_id (int): Идентификатор книги.

        Returns:
            BookService: Экземпляр сервиса книги.

        Raises:
            HTTPException: Если книга не найдена.
        """
        book_service = BookService(async_session=self.session)
        await book_service.store_obj_db_by_id_or_404(obj_id=book_id)
        return book_service
