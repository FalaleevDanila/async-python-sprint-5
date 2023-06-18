from http import HTTPStatus
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_ping():
    response = client.get(app.url_path_for('ping_db'))
    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert len(result) == 1


def test_list_file():
    response = client.get(app.url_path_for('info'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    result = response.json()
    assert len(result) == 1
    assert result.get("detail") == "Unauthorized"


def test_files_upload():
    response = client.post(app.url_path_for('upload'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    result = response.json()
    assert len(result) == 1
    assert result.get("detail") == "Unauthorized"


def test_files_download():
    response = client.get(app.url_path_for('download'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    result = response.json()
    assert len(result) == 1
    assert result.get("detail") == "Unauthorized"


def test_work():
    response = client.post(app.url_path_for('register'), json={"name": "test1", "password": "123"})
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(app.url_path_for('authentication'), json={"name": "test1", "password": "123"})
    assert response.status_code == HTTPStatus.OK


def test_get_list_file_work(auth_async_client):
    response = client.get(app.url_path_for('info'), headers=auth_async_client.headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    result = response.json()
    assert len(result) == 1
    assert result.get("detail") == "Unauthorized"




