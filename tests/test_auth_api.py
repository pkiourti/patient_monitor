import requests
import time

BASE = "http://127.0.0.1:5000/"

def test_auth_api():
    # test post request
    json_data = {}
    json_data['email'] = "admin"
    json_data['password'] = "admin"
    response = requests.post(BASE + 'auth', data=json_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()
