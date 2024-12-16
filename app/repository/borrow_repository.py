from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.borrow_model import Borrow
from app.repository.base_repository import BaseRepository
from app.repository.repository_errors import crud_error_handler


class BorrowRepository(BaseRepository):
    """
    Репозиторий для операций с выдачами книг.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Borrow)
        self.session = session

    @crud_error_handler
    async def update(self, borrow_db: Borrow) -> Borrow:
        """
        Закрывает выдачу в базе данных.

        Args:
            borrow_db (Borrow): Объект выдачи для закрытия.

        Returns:
            Borrow: Обновленный объект выдачи.

        """
        borrow_db.return_date = datetime.now()
        await self.session.commit()
        return borrow_db
