import datetime
from typing import Type, Callable, Any
from unittest.mock import AsyncMock

import pytest

from tests.unit_tests.mock_services import BaseMokService

test_data_full = [
    {"id": 1, "first_name": "Иван2", "last_name": "asdas", "birth_date": str(datetime.date(2024, 12, 16))},
]


@pytest.fixture
async def mock_dependency():
    return AsyncMock()


@pytest.fixture(scope="function")
async def override_services_dependencies(mock_dependency, test_app, request):
    service_class: Type[BaseMokService] = request.param["service_class"]
    dependency_function: Callable[..., Any] = request.param["dependency_function"]
    test_method_name: str = request.param["test_method_name"]
    service_instance = service_class(
        dependency=mock_dependency, test_method_name=test_method_name, test_data=test_data_full
    )

    def override_dependency(q: str | None = None):
        return service_instance

    test_app.dependency_overrides[dependency_function] = override_dependency
    yield service_instance
