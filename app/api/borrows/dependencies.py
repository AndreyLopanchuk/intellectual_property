from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import db
from app.services.borrow_service import BorrowService


async def get_borrow_service(session: AsyncSession = Depends(db.session_getter)) -> BorrowService:
    """
    Depends зависимость для создания экземпляра сервиса работы с выдачами.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        BorrowService: Экземпляр сервиса для работы с выдачами.
    """
    return BorrowService(async_session=session)


async def get_borrow_service_with_obj_by_id(
    borrow_id: Annotated[int, Path], borrow_service: BorrowService = Depends(get_borrow_service)
) -> BorrowService:
    """
    Depends зависимость для получания экземпляра сервиса работы с выдачами,
    Экземпляр сервиса сохраняет в атрибуте класса объект базы данных полученный по входящему ID.

    Args:
        borrow_id (int): ID выдачи.
        borrow_service (BorrowService): Экземпляр сервиса для работы с выдачами.

    Returns:
        BorrowService: Экземпляр сервиса для работы с выдачами.
    """
    await borrow_service.store_obj_db_by_id_or_404(borrow_id)
    return borrow_service
