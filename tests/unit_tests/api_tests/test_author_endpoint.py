import pytest

from app.api.authors.dependencies import get_author_service
from app.schemas.author_schema import AuthorFull
from tests.unit_tests.mock_services import AuthorService
from tests.unit_tests.mok_fixtures import test_data_full, override_services_dependencies, mock_dependency


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "override_services_dependencies",
    [
        {"service_class": AuthorService, "dependency_function": get_author_service, "test_method_name": "get_all"},
    ],
    indirect=True,
)
async def test_get_authors_endpoint(override_services_dependencies: AuthorFull, test_client):
    response = await test_client.get("/authors/")
    assert response.status_code == 200
    for i in range(len(test_data_full)):
        assert sorted(response.json()[i]) == sorted(test_data_full[i])
