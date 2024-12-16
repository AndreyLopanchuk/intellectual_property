from typing import List

from fastapi import APIRouter, Depends, status

from app.api.borrows.dependencies import get_borrow_service, get_borrow_service_with_obj_by_id
from app.schemas.borrow_schema import BorrowCreate, BorrowFull, BorrowResponse
from app.services.borrow_service import BorrowService

router = APIRouter(tags=["API для управления выдачами книг."])


@router.post(
    "/",
    summary="Создание записи о выдаче книги",
    response_model=BorrowResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_borrow_endpoint(
    borrow_in: BorrowCreate,
    borrow_service: BorrowService = Depends(get_borrow_service),
):
    """
    ### Создание записи о выдаче книги
    ----------------

    * **POST /borrows/**
    + **Description**: Создает новую запись о выдаче книги.
    + **Request**: `BorrowCreate`
    + **Response**: `BorrowResponse`
    + **Status Code**: 201 Created
    """
    return await borrow_service.create_borrow(borrow_in=borrow_in)


@router.get(
    "/",
    summary="Получение списка всех выдач книг",
    response_model=List[BorrowResponse],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_borrows_endpoint(
    borrow_service: BorrowService = Depends(get_borrow_service),
):
    """
    ### Получение всех выдач книг
    ----------------------

    * **GET /borrows/**
    + **Description**: Возвращает список всех выдач книг.
    + **Response**: `List[BorrowResponse]`
    + **Status Code**: 200 OK
    """
    return await borrow_service.get_all()


@router.get(
    "/{borrow_id}",
    summary="Получение информации о выдаче книги",
    response_model=BorrowResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_borrow_endpoint(
    borrow_service: BorrowService = Depends(get_borrow_service_with_obj_by_id),
):
    """
    ### Получение информации о выдаче книги
    -----------------------------

    * **GET /borrows/{borrow_id}**
    + **Description**: Возвращает информацию о выдаче книги по входящему ID.
    + **Parameters**: `borrow_id`
    + **Response**: `BorrowResponse`
    + **Status Code**: 200 OK
    """
    return borrow_service.obj_db_by_id


@router.patch(
    "/{borrow_id}/return",
    summary="Завершение выдачи книги",
    response_model=BorrowFull,
    status_code=status.HTTP_200_OK,
)
async def borrow_completion_endpoint(
    borrow_service: BorrowService = Depends(get_borrow_service_with_obj_by_id),
):
    """
    ### Завершение выдачи книги
    ------------------------------

    * **PATCH /borrows/{borrow_id}/return**
    + **Description**: Завершает выдачу книги по входящему ID, устанавливает время сдачи.
    + **Parameters**: `borrow_id`
    + **Response**: `BorrowFull`
    + **Status Code**: 200 OK
    """
    return await borrow_service.close_borrow()
