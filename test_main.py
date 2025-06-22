from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201

def test_duplicate_register():
    client.post("/register", json={"username": "testuser2", "password": "testpass"})
    response = client.post("/register", json={"username": "testuser2", "password": "testpass"})
    assert response.status_code == 400
