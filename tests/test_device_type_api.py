import requests

BASE = "http://127.0.0.1:5000/"

def test_device_type_api():
    # test post request
    json_data = {}
    json_data['device_type'] = "oximeter1"
    response = requests.post(BASE + 'device_types', data=json_data)
    device_type_id = response.json()['device_type_id']
    assert response.status_code == 200
    assert device_type_id.isdecimal()
    print(response.json())

    # test put request
    json_data['device_type'] = "oximeter2"
    response = requests.put(BASE + 'device_types/' + device_type_id, data=json_data)
    assert response.status_code == 200
    assert response.json() == device_type_id
    print(response.json())
    
    # test get request
    response = requests.get(BASE + 'device_types/' + device_type_id)
    assert response.status_code == 200
    assert response.json()['device_type_id'] == device_type_id
    assert response.json()['device_type'] == json_data['device_type']
    print(response.json())

    # test get request
    response = requests.get(BASE + 'device_types')
    assert response.status_code == 200
    print(response.json())

    # test delete request
    response = requests.delete(BASE + 'device_types/' + device_type_id)
    assert response.status_code == 200
    assert response.json() == device_type_id
    print(response.json())
