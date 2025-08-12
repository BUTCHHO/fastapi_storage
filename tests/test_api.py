from httpx import AsyncClient, ASGITransport
import pytest
from config import reconfigure_values_for_tests
reconfigure_values_for_tests()

from config import DATABASE_URL
print('\n', DATABASE_URL, 'HERE IS DATABASE')
from alchemy.async_engine import async_engine
from alchemy.models import Base
import asyncio

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def prepare_tables_for_tests():
    asyncio.run(create_tables())

prepare_tables_for_tests()

from app.main import app

@pytest.fixture()
def client():
    client = AsyncClient(base_url='http://test', transport=ASGITransport(app=app))
    return client



@pytest.mark.asyncio
async def test_sign_up(client):
    params = {'name': 'tester1', 'password': '123'}
    response = await client.post('/_sign-up', params=params)
    print(response.content)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_sign_in(client):
    params = {'name': 'tester1', 'password': '123'}
    response = await client.post('/_log-in', params=params)
    print(response.content)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_view_root_storage(client):
    url = '/storage'
    params = {"user_id": 1}
    response = await client.get(url=url, params=params)
    json = response.json()
    assert response.status_code == 200
    assert 'entities' in json

@pytest.mark.asyncio
async def test_view_storage(client):
    url = '/storage/music%2Fletov?user_id=1'
    params = {"user_id": 1}
    response = await client.get(url=url, params=params)
    assert  response.status_code == 200
    assert 'entities' in response.json()

@pytest.mark.asyncio
async def test_download_dir(client):
    url = '/download-entity'
    params = {"user_id": 1, "entity_path_in_storage": 'music/nirvana'}
    response = await client.get(url=url, params=params)
    headers = response.headers
    content_len = int(headers['content-length'])
    assert response.status_code == 200
    assert content_len > 0

@pytest.mark.asyncio
async def test_download_file(client):
    url = '/download-entity'
    params = {"user_id": 1, "entity_path_in_storage": 'images/Desert.jpg'}
    response = await client.get(url=url, params=params)
    headers = response.headers
    content_len = int(headers['content-length'])
    status_code = response.status_code
    assert status_code == 200
    assert content_len > 0

@pytest.mark.asyncio
async def test_upload_entity(client):
    print('not_impl')