import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient

from task_11_2.main import app, reset_state


fake = Faker("ru_RU")


@pytest.fixture(autouse=True)
def clear_state():
    reset_state()
    yield
    reset_state()


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    payload = {
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=60),
    }

    response = await async_client.post("/users", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]


@pytest.mark.asyncio
async def test_get_existing_user(async_client: AsyncClient):
    payload = {
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=60),
    }

    created = await async_client.post("/users", json=payload)
    user_id = created.json()["id"]
    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["username"] == payload["username"]


@pytest.mark.asyncio
async def test_get_missing_user(async_client: AsyncClient):
    response = await async_client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_delete_existing_user(async_client: AsyncClient):
    payload = {
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=60),
    }

    created = await async_client.post("/users", json=payload)
    user_id = created.json()["id"]

    response = await async_client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.text == ""


@pytest.mark.asyncio
async def test_delete_same_user_twice(async_client: AsyncClient):
    payload = {
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=60),
    }

    created = await async_client.post("/users", json=payload)
    user_id = created.json()["id"]

    first_delete = await async_client.delete(f"/users/{user_id}")
    second_delete = await async_client.delete(f"/users/{user_id}")

    assert first_delete.status_code == 204
    assert second_delete.status_code == 404
    assert second_delete.json() == {"detail": "User not found"}
