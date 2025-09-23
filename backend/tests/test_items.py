from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Modular Boilerplate!"}

def test_create_item():
    response = client.post(
        "/api/v1/items/",
        json={
            "name": "Test Item",
            "description": "This is a test item."
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Item",
        "description": "This is a test item."
    }

def test_read_items():
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_single_item():
    # First create an item
    client.post(
        "/api/v1/items/",
        json={
            "name": "Another Item",
            "description": "Another test item."
        }
    )
    response = client.get("/api/v1/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_nonexistent_item():
    response = client.get("/api/v1/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
