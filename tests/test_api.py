
from .client import Client

from config import reconfigure_values_for_tests

reconfigure_values_for_tests()

client = Client()
client.set_base_url('http://0.0.0.0:8000')

def test_sign_up():
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_sign-up', params=params)
    assert response.status_code == 200

def test_sign_in():
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_log-in', params=params)
    print(response.content)
    assert response.status_code == 200

def test_get_entities_no_params():
    response = client.get('/_get_entities')
    entities = response.json()
    assert type(entities['entities']) is list
    assert response.status_code == 200

def test_make_dir_in_storage():
    url = '/make-dir-in-storage'
    params = {'name':'test_dir'}
    response = client.post(url, params)
    assert response.status_code == 200
    response = client.get('/_get_entities')
    entities = response.json()
    assert '/test_dir' in entities['entities']



def test_download_entity():
    url = '/download-entity'
    params = {'entity_path_in_storage':'test_dir'}
    response = client.get(url, params)
    print(response.headers)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/zip'

def test_delete_dir_in_storage():
    url = '/delete-entity-in-storage'
    params = {'password':'123', 'path_in_storage':'test_dir'}
    response = client.delete(url, params)
    assert response.status_code == 200
    response = client.get('/_get_entities')
    entities = response.json()
    assert '/test_dir' not in entities['entities']