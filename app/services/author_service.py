from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author_model import Author
from app.repository.author_repository import AuthorRepository
from app.schemas.author_schema import AuthorCreate
from app.services.base_service import BaseService, DeleterService


class AuthorService(BaseService, DeleterService):
    """
    Сервис для работы с авторами.

    Attributes:
        session (AsyncSession): Сессия базы данных.
        repository (AuthorRepository): Репозиторий для работы с авторами.
        obj_db_by_id (Author | None): Атрибут для хранения модели Автора полученной по входящему идентификатору.
    """

    def __init__(self, async_session: AsyncSession):
        self.session = async_session
        self.repository: AuthorRepository = AuthorRepository(session=async_session)
        self.obj_db_by_id: Author | None = None
        super().__init__(repository=self.repository, obj_message="Author", obj_db_by_id=self.obj_db_by_id)

    async def create_author(self, author_in: AuthorCreate) -> Author:
        """
        Добавление нового автора.

        Args:
            author_in (AuthorCreate): Данные для нового автора.

        Returns:
            Author: Добавленная модель автора.
        """
        return await self.repository.create(obj_in=author_in)

    async def update_author(self, author_in: AuthorCreate) -> Author:
        """
        Обновление данных автора.

        Args:
            author_in (AuthorCreate): Данные для обновления автора.

        Returns:
            Author: Обновленная модель автор.
        """
        return await self.repository.update(obj_db=self.obj_db_by_id, obj_in=author_in)
