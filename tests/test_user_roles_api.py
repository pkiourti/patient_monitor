import requests

BASE = "http://127.0.0.1:5000/"

def test_user_roles_api():
    # test post request
    json_data = {}
    json_data['user_role'] = "staff"
    response = requests.post(BASE + 'user_roles', data=json_data)
    print(response.json())
    user_role_id = response.json()['user_role_id']
    assert response.status_code == 200
    assert user_role_id.isdecimal()

    # test put request
    json_data['user_role'] = "CEO"
    response = requests.put(BASE + 'user_roles/'+user_role_id, data=json_data)
    assert response.status_code == 200
    assert user_role_id == response.json()
    print(response.json())

    # test get request
    response = requests.get(BASE + 'user_roles/'+user_role_id)
    assert response.status_code == 200
    assert response.json()['user_role_id'] == user_role_id
    assert response.json()['user_role'] == json_data['user_role']
    print(response.json())

    # test delete request
    response = requests.delete(BASE + 'user_roles/'+user_role_id)
    assert response.json() == user_role_id
    print(response.json())

    # test get request
    response = requests.get(BASE + 'user_roles')
    assert response.status_code == 200
    print(response)
