
from .client import Client

from config import reconfigure_values_for_tests

reconfigure_values_for_tests()

client = Client()
client.set_base_url('http://0.0.0.0:8000')

def test_sign_up():
    print('IN TESTS')
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_sign-up', params=params)
    print(response.content)
    assert response.status_code == 200

def test_sign_in():
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_log-in', params=params)
    print(response.content)
    assert response.status_code == 200

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