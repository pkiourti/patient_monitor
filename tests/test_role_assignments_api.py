import requests

BASE = "http://127.0.0.1:5000/"

def test_role_assignment_api():
    # test post request
    json_data = {}
    json_data['user_id'] = "0"
    json_data['user_role_id'] = "0"
    response = requests.post(BASE + 'user_role_assignments', data=json_data)
    print(response.json())
    role_assignment_id = response.json()['role_assignment_id']
    assert response.status_code == 200
    assert role_assignment_id.isdecimal()

    # test put request
    json_data['user_role_id'] = "1"
    response = requests.put(BASE + 'user_role_assignments/'+role_assignment_id, data=json_data)
    assert response.status_code == 200
    assert role_assignment_id == response.json()
    print(response.json())

    # test get request
    response = requests.get(BASE + 'user_role_assignments/'+role_assignment_id)
    assert response.status_code == 200
    assert response.json()['role_assignment_id'] == role_assignment_id
    assert response.json()['user_id'] == json_data['user_id']
    assert response.json()['user_role_id'] == json_data['user_role_id']
    print(response.json())

    # test delete request
    response = requests.delete(BASE + 'user_role_assignments/'+role_assignment_id)
    assert response.json() == role_assignment_id
    print(response.json())

    # test get request
    response = requests.get(BASE + 'user_role_assignments')
    assert response.status_code == 200
    print(response)
