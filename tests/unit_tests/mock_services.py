from typing import Any
from unittest.mock import AsyncMock


class BaseMokService:
    def __init__(self, dependency: AsyncMock, test_method_name: str, test_data: Any = None):
        self._dependency = dependency
        self._dependency.some_method.return_value = test_data

        async def method():
            return await self._dependency.some_method()

        setattr(self, test_method_name, method)


class AuthorService(BaseMokService):
    pass
