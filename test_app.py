import pytest
import json
from app import app, collection


@pytest.fixture(scope="session")
def client():
    with app.test_client() as client:
        collection.delete_many({})
        yield client


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Hello, Docusketch!"


def test_create_key_value(client):
    data = {"key": "test_key", "value": "test_value"}
    response = client.post('/api/keyvalue', json=data)
    assert response.status_code == 201


def test_create_duplicate_key(client):
    data = {"key": "test_key", "value": "test_value"}
    client.post('/api/keyvalue', json=data)
    response = client.post('/api/keyvalue', json=data)
    assert response.status_code == 409


def test_create_invalid_request(client):
    response = client.post('/api/keyvalue', json={})
    assert response.status_code == 400


def test_update_key_value(client):
    data = {"value": "updated_value"}
    response = client.put('/api/keyvalue/test_key', json=data)
    assert response.status_code == 200


def test_update_invalid_request(client):
    response = client.put('/api/keyvalue/test_key', json={})
    assert response.status_code == 400


def test_get_key_value(client):
    response = client.get('/api/keyvalue/test_key')
    assert response.status_code == 200
    assert json.loads(response.data) == {"key": "test_key", "value": "updated_value"}


def test_get_key_value_not_found(client):
    response = client.get('/api/keyvalue/non_existing_key')
    assert response.status_code == 404
