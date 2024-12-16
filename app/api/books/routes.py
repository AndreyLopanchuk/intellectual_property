from typing import List

from fastapi import APIRouter, Depends, status

from app.api.books.dependencies import get_book_service, get_book_service_with_obj_by_id
from app.schemas.book_schema import BookCreate, BookFull, BookUpdate
from app.services.book_service import BookService

router = APIRouter(tags=["API для управления книгами."])


@router.post(
    "/",
    summary="Добавление книги",
    response_model=BookFull,
    status_code=status.HTTP_201_CREATED,
)
async def create_book_endpoint(
    book_in: BookCreate,
    book_service: BookService = Depends(get_book_service),
):
    """
    ### Добавление книги
    ----------------

    * **POST /books/**
    + **Description**: Добавляет новую книгу в базу данных.
    + **Request**: `BookCreate`
    + **Response**: `BookFull`
    + **Status Code**: 201 Created
    """
    return await book_service.create_book(book_in=book_in)


@router.get(
    "/",
    summary="Получение списка книг",
    response_model=List[BookFull],
    status_code=status.HTTP_200_OK,
)
async def get_books_endpoint(
    book_service: BookService = Depends(get_book_service),
):
    """
    ### Получение всех книг
    ----------------------

    * **GET /books/**
    + **Description**: Возвращает список всех книг.
    + **Response**: `List[BookFull]`
    + **Status Code**: 200 OK
    """
    return await book_service.get_all()


@router.get(
    "/{book_id}",
    summary="Получение информации о книге",
    response_model=BookFull,
    status_code=status.HTTP_200_OK,
)
async def get_book_endpoint(
    book_service: BookService = Depends(get_book_service_with_obj_by_id),
):
    """
    ### Получение информации о книге
    -----------------------------

    * **GET /books/{book_id}**
    + **Description**: Возвращает информацию о книге по входящему ID.
    + **Parameters**: `book_id`
    + **Response**: `BookFull`
    + **Status Code**: 200 OK
    """
    return book_service.obj_db_by_id


@router.put(
    "/{book_id}",
    summary="Обновление информации о книге",
    response_model=BookFull,
    status_code=status.HTTP_200_OK,
)
async def update_book_endpoint(
    book_in: BookUpdate,
    book_service: BookService = Depends(get_book_service_with_obj_by_id),
):
    """
    ### Обновление информации о книге
    ------------------------------

    * **PUT /books/{book_id}**
    + **Description**: Обновляет информацию о книге по входящему ID.
    + **Parameters**: `book_id`, `BookUpdate`
    + **Response**: `BookFull`
    + **Status Code**: 200 OK
    """
    return await book_service.update_book(book_in=book_in)


@router.delete(
    "/{book_id}",
    summary="Удаление книги",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book_endpoint(
    book_service: BookService = Depends(get_book_service_with_obj_by_id),
):
    """
    ### Удаление книги
    ----------------

    * **DELETE /books/{book_id}**
    + **Description**: Удаляет книгу по ее ID.
    + **Parameters**: `book_id`
    + **Status Code**: 204 No Content
    """
    await book_service.delete()
