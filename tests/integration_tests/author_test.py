import pytest

test_data_create = {"first_name": "й1", "last_name": "st3", "birth_date": "2024-12-16"}


@pytest.mark.asyncio
async def test_create_author_endpoint(test_client) -> None:
    response = await test_client.post("/authors/", json=test_data_create)
    assert response.status_code == 201
    data = response.json()
    data.pop("id")
    assert sorted(data) == sorted(test_data_create)
