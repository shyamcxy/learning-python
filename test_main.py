import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client(monkeypatch):
    test_users = [
        {"user_id": 123, "name": "Shyam"},
        {"user_id": 234, "name": "Ram"},
    ]

    monkeypatch.setattr(main, "users", test_users)

    return TestClient(main.app)


def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {"user_id": 123, "name": "Shyam"},
        {"user_id": 234, "name": "Ram"},
    ]
