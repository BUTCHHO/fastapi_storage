from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_sign_up():
    url = '/_sign-up'
    params = {'name':'tester', 'password':'123'}
    response = client.post(url, params=params)
    assert response.status_code == 200