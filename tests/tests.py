from httpx import AsyncClient
from http import HTTPStatus


async def test_ping(client: AsyncClient):
    response = await client.get('/api/v1/ping')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status_db': 1}
