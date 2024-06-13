from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)


def test_get_id():
    response = client.get('/memes/78/')

    assert response.status_code == status.HTTP_200_OK
    assert "url" in response.json().keys()


def test_post_json():
    filepath = "test/test.json"
    with open(file=filepath, mode='r') as file:
        response = client.post('/memes/', files=file)
        assert response.status_code != status.HTTP_200_OK

def test_get_all():
    response = client.get('/memes/')

    assert response.status_code == status.HTTP_200_OK
    # assert "items" in response.json().keys()