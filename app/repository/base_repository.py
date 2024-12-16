from typing import List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.repository.repository_errors import crud_error_handler

DB = TypeVar("DB", bound=Base)
P = TypeVar("P", bound=BaseModel)


class BaseRepository:
    """
    Базовый репозиторий для работы с данными в базе данных.

    Attributes:
        session (AsyncSession): Сессия базы данных.
        model (Type[DB]): Модель данных.
    """

    def __init__(self, session: AsyncSession, model: Type[DB]):
        self.session = session
        self.model = model

    @crud_error_handler
    async def get_one(self, obj_id: int) -> DB | None:
        """
        Получение одной записи из базы данных по идентификатору.

        Args:
            obj_id (int): Идентификатор записи.

        Returns:
            DB: Объект из базы данных.
        """
        return await self.session.get(self.model, obj_id)

    @crud_error_handler
    async def get_all(self) -> List[DB]:
        """
        Получение всех объектов из базы данных.

        Returns:
            List[DB]: Список объектов из базы данных.
        """
        stmt = select(self.model).order_by(self.model.id)
        obj_db = await self.session.scalars(stmt)
        return list(obj_db)

    @crud_error_handler
    async def create(self, obj_in: P) -> DB:
        """
        Создание новой записи в базе данных.

        Args:
            obj_in (P): Данные для создания новой записи.

        Returns:
            DB: Созданный объект.
        """
        obj = self.model(**obj_in.model_dump())
        self.session.add(obj)
        await self.session.flush()
        await self.session.commit()
        return obj

    @crud_error_handler
    async def update(self, obj_db: DB, obj_in: P) -> DB:
        """
        Обновление существующей записи в базе данных.

        Args:
            obj_db (DB): Существующая запись.
            obj_in (P): Данные для обновления записи.

        Returns:
            DB: Обновленная запись.
        """
        for key, value in obj_in.model_dump().items():
            setattr(obj_db, key, value)
        await self.session.commit()
        return obj_db


class DeleterRepository:
    """
    Репозиторий для удаления записей из базы данных.

    Attributes:
        session (AsyncSession): Сессия базы данных.
        model (Type[DB]): Модель данных.
    """

    def __init__(self, session: AsyncSession, model: Type[DB]):
        self.session = session
        self.model = model

    @crud_error_handler
    async def delete(self, obj_db: DB) -> None:
        """
        Удаление записи из базы данных.

        Args:
            obj_db (DB): Запись для удаления.
        """
        await self.session.delete(obj_db)
        await self.session.commit()
