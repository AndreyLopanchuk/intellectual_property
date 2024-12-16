from typing import List

from fastapi import APIRouter, Depends, status

from app.api.authors.dependencies import get_author_service, get_author_service_with_obj_by_id
from app.schemas.author_schema import AuthorCreate, AuthorFull, AuthorUpdate
from app.services.author_service import AuthorService

router = APIRouter(tags=["API для управления авторами."])


@router.post(
    "/",
    summary="Создание автора",
    response_model=AuthorFull,
    status_code=status.HTTP_201_CREATED,
)
async def create_author_endpoint(
    author_in: AuthorCreate,
    author_service: AuthorService = Depends(get_author_service),
):
    """
    ### Добавление автора
    ----------------

    * **POST /authors/**
    + **Description**: Добавляет нового автора в базу данных.
    + **Request**: `AuthorCreate`
    + **Response**: `AuthorFull`
    + **Status Code**: 201 Created
    """
    return await author_service.create_author(author_in=author_in)


@router.get(
    "/",
    summary="Получение всех авторов",
    response_model=List[AuthorFull],
    status_code=status.HTTP_200_OK,
)
async def get_authors_endpoint(
    author_service: AuthorService = Depends(get_author_service),
):
    """
    ### Получение всех авторов
    ----------------------

    * **GET /authors/**
    + **Description**: Возвращает список всех авторов из базы данных.
    + **Response**: `List[AuthorFull]`
    + **Status Code**: 200 OK
    """
    return await author_service.get_all()


@router.get(
    "/{author_id}",
    summary="Получение информации об авторе",
    response_model=AuthorFull,
    status_code=status.HTTP_200_OK,
)
async def get_author_endpoint(
    author_service: AuthorService = Depends(get_author_service_with_obj_by_id),
):
    """
    ### Получение информации об авторе
    -----------------------------

    * **GET /authors/{author_id}**
    + **Description**: Возвращает информацию об авторе по входящему ID.
    + **Parameters**: `author_id`
    + **Response**: `AuthorFull`
    + **Status Code**: 200 OK
    """
    return author_service.obj_db_by_id


@router.put(
    "/{author_id}",
    summary="Обновление информации об авторе",
    response_model=AuthorFull,
    status_code=status.HTTP_200_OK,
)
async def update_author_endpoint(
    author_in: AuthorUpdate,
    author_service: AuthorService = Depends(get_author_service_with_obj_by_id),
):
    """
    ### Обновление информации об авторе
    ------------------------------

    * **PUT /authors/{author_id}**
    + **Description**: Обновляет информацию об авторе по входящему ID.
    + **Parameters**: `author_id`, `AuthorUpdate`
    + **Response**: `AuthorFull`
    + **Status Code**: 200 OK
    """
    return await author_service.update_author(author_in=author_in)


@router.delete(
    "/{author_id}",
    summary="Удаление автора",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_author_endpoint(
    author_service: AuthorService = Depends(get_author_service_with_obj_by_id),
):
    """
     ### Удаление автора
    ----------------

    * **DELETE /authors/{author_id}**
    + **Description**: Удаляет автора по входящему ID.
    + **Parameters**: `author_id`
    + **Status Code**: 204 No Content
    """
    await author_service.delete()
