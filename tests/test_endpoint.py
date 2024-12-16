import datetime
from unittest.mock import AsyncMock

import pytest

from app.api.authors.dependencies import get_author_service


""" в среду добавлю тестов 
    это не окончательный вариант, разбирался как работает
    тестирование методов класса через depends зависимость,
    поэтому всё привязано к тесту. сделаю более динамическими. 
"""


test_data_create = {"first_name": "й1", "last_name": "st3", "birth_date": "2024-12-16"}
test_data_full = [
    {"id": 1, "first_name": "Иван2", "last_name": "asdas", "birth_date": datetime.date(2024, 12, 16)},
]


class AuthorService:
    def __init__(self, dependency):
        self.dependency = dependency

    async def get_all(self):
        return await self.dependency.some_method(test_data_full)


@pytest.fixture
async def mock_dependency():
    return AsyncMock()


@pytest.fixture
async def author_service(mock_dependency):
    return AuthorService(mock_dependency)


@pytest.fixture
async def override_author_service_dependency(author_service, main_app):
    def override_dependency(q: str | None = None):
        return author_service

    main_app.dependency_overrides[get_author_service] = override_dependency
    yield
    del main_app.dependency_overrides[get_author_service]


@pytest.mark.asyncio
async def test_get_authors_endpoint(mock_dependency, override_author_service_dependency, test_client):
    mock_dependency.some_method.return_value = test_data_full

    response = await test_client.get("/authors/")
    assert response.status_code == 200
    for i in range(len(test_data_full) - 1):
        assert response.json()[i] == test_data_full[i]


@pytest.mark.asyncio
async def test_create_author_endpoint(test_client) -> None:
    response = await test_client.post("/authors/", json=test_data_create)
    assert response.status_code == 201
    data = response.json()
    data.pop("id")
    assert data == test_data_create
