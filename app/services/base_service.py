from typing import List, TypeVar

from fastapi import HTTPException, status

from app.models.base import Base
from app.repository.base_repository import BaseRepository, DeleterRepository

DB = TypeVar("DB", bound=Base)


class BaseService:
    """
    Базовый сервисный класс.

    Attributes:
        repository (BaseRepository): Репозиторий для операций.
        obj_message (str): Название объекта.
        obj_db_by_id (DB | None): Объект базы данных, полученный по входящему идентификатору.
    """

    def __init__(self, repository: BaseRepository, obj_message: str, obj_db_by_id: DB | None):
        self.repository = repository
        self.obj_message = obj_message
        self.obj_db_by_id = obj_db_by_id

    async def store_obj_db_by_id_or_404(self, obj_id: int):
        """
        Сохраняет объект базы данных полученный по входящему идентификатору или вызывает исключение 404.

        Args:
            obj_id (int): Идентификатор объекта.

        Returns:
            DB: Объект базы данных.

        Raises:
            HTTPException: Если объект не найден.
        """
        self.obj_db_by_id = await self.repository.get_one(obj_id=obj_id)
        if self.obj_db_by_id:
            return self.obj_db_by_id

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.obj_message} {obj_id} not found")

    async def get_one(self, obj_id: int) -> DB:
        """
        Получает один объект базы данных по идентификатору.

        Args:
            obj_id (int): Идентификатор объекта.

        Returns:
            DB: Объект базы данных.
        """
        return await self.repository.get_one(obj_id)

    async def get_all(self) -> List[DB]:
        """
        Получает все объекты базы данных.

        Returns:
            List[DB]: Список объектов базы данных.
        """
        return await self.repository.get_all()


class DeleterService:
    """
    Сервисный класс для удаления.

    Attributes:
        repository (DeleterRepository): Репозиторий для операций удаления.
        obj_db_by_id (DB | None): Объект базы данных полученный по входящему идентификатору.
    """

    def __init__(self, repository: DeleterRepository, obj_db_by_id: DB | None):
        self.repository: DeleterRepository = repository
        self.obj_db_by_id: DB | None = obj_db_by_id

    async def delete(self) -> None:
        """
        Удаляет объект базы данных.

        Returns:
            None
        """
        return await self.repository.delete(obj_db=self.obj_db_by_id)
