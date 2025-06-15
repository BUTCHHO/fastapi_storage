from fastapi import UploadFile
from fastapi.testclient import TestClient


from main import app
client = TestClient(app)

def test_view_root_storage():
    url = '/storage'
    params = {"user_id": 1}
    response = client.get(url=url, params=params)
    json = response.json()
    assert response.status_code == 200
    assert 'entities' in json

def test_view_storage():
    url = '/storage/music%2Fletov?user_id=1'
    params = {"user_id": 1}
    response = client.get(url=url, params=params)
    assert  response.status_code == 200
    assert 'entities' in response.json()

def test_download_dir():
    url = '/download-entity'
    params = {"user_id": 1, "entity_path_in_storage": 'music/nirvana'}
    response = client.get(url=url, params=params)
    headers = response.headers
    content_len = int(headers['content-length'])
    assert response.status_code == 200
    assert content_len > 0

def test_download_file():
    url = '/download-entity'
    params = {"user_id": 1, "entity_path_in_storage": 'images/Desert.jpg'}
    response = client.get(url=url, params=params)
    headers = response.headers
    content_len = int(headers['content-length'])
    status_code = response.status_code
    assert status_code == 200
    assert content_len > 0

def test_upload_entity():
    print('not_impl')