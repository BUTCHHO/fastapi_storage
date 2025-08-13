
from .client import Client

from config import reconfigure_values_for_tests

reconfigure_values_for_tests()

client = Client()
client.set_base_url('http://0.0.0.0:8000')

def test_get_entities_no_params_no_login():
    response = client.get('/_get_entities')
    assert response.status_code == 401

def test_sign_up():
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_sign-up', params=params)
    assert response.status_code == 200

def test_sign_in():
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_log-in', params=params)
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

def test_make_nested_dir():
    url = '/make-dir-in-storage'
    params = {'name':'nested_dir', 'path_in_storage':'test_dir'}
    response = client.post(url, params)
    assert response.status_code == 200
    response = client.get('/_get_entities', {'path_in_storage':'test_dir'})
    json = response.json()
    assert '/nested_dir' in json['entities']

def test_search_entity():
    url = '/_get_entities/search'
    params = {'pattern':'nes'}
    response = client.get(url, params)
    assert response.status_code == 200
    json = response.json()
    assert '/test_dir/nested_dir' in json['entities']

def test_download_entity():
    url = '/download-entity'
    params = {'entity_path_in_storage':'test_dir'}
    response = client.get(url, params)
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

def test_logout():
    url = '/_logout'
    response = client.get(url)
    assert response.status_code == 200
    print(client.cookies)

def test_delete_acc():
    response_login = client.post('/_log-in', {'name':'tester1', 'password':'123'})
    assert response_login.status_code == 200
    params = {'password':'123'}
    response = client.delete('/settings/delete_acc', params)
    assert response.status_code == 200
    response_login = client.post('/_log-in', {'name':'tester1', 'password':'123'})
    assert response_login.status_code == 404
