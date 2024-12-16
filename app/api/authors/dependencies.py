from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import db
from app.services.author_service import AuthorService


async def get_author_service(session: AsyncSession = Depends(db.session_getter)) -> AuthorService:
    """
    Depends зависимость для создания экземпляра сервиса работы с авторами.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        AuthorService: Экземпляр сервиса для работы с авторами.
    """
    return AuthorService(async_session=session)


async def get_author_service_with_obj_by_id(
    author_id: Annotated[int, Path], author_service: AuthorService = Depends(get_author_service)
) -> AuthorService:
    """
    Depends зависимость для получания экземпляра сервиса работы с авторами,
    Экземпляр сервиса сохраняет в атрибуте класса объект базы данных полученный по входящему ID.

    Args:
        author_id (int): ID автора.
        author_service (AuthorService): Экземпляр сервиса для работы с авторами.

    Returns:
        AuthorService: Экземпляр сервиса для работы с авторами с объектом автора.
    """
    await author_service.store_obj_db_by_id_or_404(author_id)
    return author_service
