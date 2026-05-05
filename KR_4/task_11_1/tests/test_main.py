from fastapi.testclient import TestClient

from task_11_1.main import app, reset_state


client = TestClient(app)


def setup_function():
    reset_state()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_success():
    response = client.post(
        "/users",
        json={
            "username": "student1",
            "email": "student1@example.com",
            "age": 21,
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == "student1"
    assert response.json()["email"] == "student1@example.com"


def test_create_user_duplicate():
    payload = {
        "username": "student1",
        "email": "student1@example.com",
        "age": 21,
    }

    client.post("/users", json=payload)
    response = client.post("/users", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_get_user_not_found():
    response = client.get("/users/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_validation_error_response():
    response = client.post(
        "/users",
        json={
            "username": "ab",
            "email": "wrong-email",
            "age": 16,
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["message"] == "Validation error"
    assert len(body["errors"]) >= 1
