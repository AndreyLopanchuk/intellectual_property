from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import db
from app.services.book_service import BookService


async def get_book_service(session: AsyncSession = Depends(db.session_getter)) -> BookService:
    """
    Depends зависимость для создания экземпляра сервиса работы с книгами.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        BookService: Экземпляр сервиса для работы с книгами.
    """
    return BookService(async_session=session)


async def get_book_service_with_obj_by_id(
    book_id: Annotated[int, Path], book_service: BookService = Depends(get_book_service)
) -> BookService:
    """
    Depends зависимость для получания экземпляра сервиса работы с книги,
    Экземпляр сервиса сохраняет в атрибуте класса объект базы данных полученный по входящему ID.

    Args:
        book_id (int): ID книги.
        book_service (BookService): Экземпляр сервиса для работы с книгами.

    Returns:
        BookService: Экземпляр сервиса для работы с книгами.
    """
    await book_service.store_obj_db_by_id_or_404(book_id)
    return book_service
