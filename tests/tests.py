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




