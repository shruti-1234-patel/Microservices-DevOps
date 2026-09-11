from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_get_user():
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Shruti"


def test_user_not_found():
    response = client.get("/users/999")

    assert response.status_code == 404