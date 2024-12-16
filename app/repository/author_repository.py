from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author_model import Author
from app.repository.base_repository import BaseRepository, DeleterRepository


class AuthorRepository(BaseRepository, DeleterRepository):
    """
    Репозиторий для операций с авторами.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Author)
