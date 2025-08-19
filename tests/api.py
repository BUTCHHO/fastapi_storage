
from .client import Client

from config import Config

Config.reconfigure_values_for_tests()

client = Client()
client.set_base_url('http://0.0.0.0:8000')


def test_get_entities_no_params_no_login():
    response = client.get('/_get_entities')
    assert response.status_code == 401

def test_sign_up():
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_sign-up', params=params)
    assert response.status_code == 200

def test_sign_up_alreade_existing_user():
    params = {'name':'tester1', 'password':'123'}
    response = client.post('/_sign-up', params)
    assert response.status_code == 409

def test_sign_in():
    params = {'name': 'tester1', 'password': '123'}
    response = client.post('/_log-in', params=params)
    assert response.status_code == 200

def test_sign_in_already_signed_in():
    params = {'name':'tester1', 'password':'123'}
    response = client.post('/_log-in', params=params)
    assert response.status_code == 200

def test_get_entities_no_params():
    response = client.get('/_get_entities')
    entities = response.json()
    assert type(entities['entities']) is list
    assert response.status_code == 200

def test_get_entities_dont_exist():
    params = {"path_in_storage":'this/dir/dont/exists'}
    url = '/_get_entities'
    response = client.get(url, params)
    assert response.status_code == 404
    assert response.json()['detail']['code'] == 'entity_does_not_exists'

def test_make_dir_in_storage():
    url = '/make-dir-in-storage'
    params = {'name':'test_dir'}
    response = client.post(url, params)
    assert response.status_code == 200
    response = client.get('/_get_entities')
    entities = response.json()
    assert '/test_dir' in entities['entities']

def test_make_already_existing_dir():
    url = '/make-dir-in-storage'
    params = {'name':'test_dir'}
    response = client.post(url, params)
    assert response.status_code == 409
    assert response.json()['detail']['code'] == 'directory_already_exists'

def test_make_nested_dir():
    url = '/make-dir-in-storage'
    params = {'name':'nested_dir', 'path_in_storage':'test_dir'}
    response = client.post(url, params)
    assert response.status_code == 200
    response = client.get('/_get_entities', {'path_in_storage':'test_dir'})
    json = response.json()
    assert '/nested_dir' in json['entities']

def test_get_entity():
    url = '/_get_entities'
    params = {'path_in_storage':'test_dir'}
    response = client.get(url, params)
    assert response.status_code == 200
    assert response.json()['entities'] is not []

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

def test_login_incorrect_password():
    url = '/_log-in'
    params = {'name':'tester1','password':'wrong osw'}
    response = client.post(url, params)
    assert response.status_code == 401

def test_delete_acc():
    response_login = client.post('/_log-in', {'name':'tester1', 'password':'123'})
    assert response_login.status_code == 200
    params = {'password':'123'}
    response = client.delete('/settings/delete_acc', params)
    assert response.status_code == 200
    response_login = client.post('/_log-in', {'name':'tester1', 'password':'123'})
    assert response_login.status_code == 404

def test_login_to_not_existing_acc():
    params = {'name':'i_dont_exists', 'password':'wrong'}
    url = '_log-in'
    response = client.post(url, params)
    assert response.status_code == 404
    assert response.json()['detail']['code'] == "user_dont_exists"
