import requests

BASE = "http://127.0.0.1:5000/"

def same_list(l1, l2):
    for el in l1:
        if el not in l2:
            return False
    return True

def test_session_api():
    # test post request
    json_data = {}
    json_data['device_id'] = "1"
    json_data['participants'] = ['user1', 'user2']
    response = requests.post(BASE + 'sessions', json=json_data)
    print(response.json())
    session_id = response.json()['session_id']
    assert response.status_code == 200
    assert session_id.isdecimal()

    # test put request
    json_data['participants'] = ['11', '12']
    response = requests.put(BASE + 'sessions/'+session_id, json=json_data)
    assert response.status_code == 200
    assert session_id == response.json()
    print(response.json())

    # test get request
    response = requests.get(BASE + 'sessions/'+session_id)
    assert response.status_code == 200
    assert response.json()['session_id'] == session_id
    assert response.json()['device_id'] == json_data['device_id']
    assert same_list(response.json()['participants'], json_data['participants'])
    print(response.json())

    # test delete request
    response = requests.delete(BASE + 'sessions/'+session_id)
    assert response.json() == session_id
    print(response.json())

    # test get request
    response = requests.get(BASE + 'sessions')
    assert response.status_code == 200
    print(response)
