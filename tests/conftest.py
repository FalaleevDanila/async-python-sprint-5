import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="session")
async def auth_async_client(test_app):
    test_user = 'test1'
    test_password = '123'
    async with AsyncClient(app=test_app, base_url='http://0.0.0.0:9000/') as ac:
        await ac.post(
            'users/register',
            json={
                'username': test_user,
                'password': test_password
            }
        )
        response = await ac.post(
            'users/auth',
            json={
                'username': test_user,
                'password': test_password
            }
        )
        token = response.json()['token']
        ac.headers = {'Authorization': token}
        yield ac
