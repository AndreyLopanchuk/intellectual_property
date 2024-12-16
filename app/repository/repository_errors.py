from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.log_config import logger


def crud_error_handler(func):
    """
    Обработчик ошибок для CRUD-операций.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            """
            Обработка ошибок целостности данных.
            """
            if args[0].__class__.__name__ == "BookRepository":
                if func.__name__ in ["create", "update"]:
                    book_in = kwargs.get("obj_in")
                    session = args[0].session
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"The {book_in.title} book"
                        f" with the author ID {book_in.author_id} is already in the database",
                    )

            if args[0].__class__.__name__ == "AuthorRepository":
                if func.__name__ in ["create", "update"]:
                    author_in = kwargs.get("obj_in")
                    session = args[0].session
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"The author {author_in.first_name} {author_in.last_name} is already in the database",
                    )

        except Exception as exc:
            """
            Обработка общих ошибок.
            """
            logger.error("%s:\nARGS: %s\nKWARGS: %s\n EXC: %s", func.__name__, args, kwargs, exc)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )

    return wrapper
