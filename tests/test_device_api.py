import requests
import time
import json

BASE = "http://127.0.0.1:5000/"

def test_device_api():
    # test post request
    json_data = {}
    json_data['device_type_id'] = "2"
    json_data['serial_number'] = "1234"
    json_data['sw_version'] = "1.0"
    json_data['mac_address'] = "00:00:5e:ff:12:34"
    json_data['purchased_on'] = str(time.time())
    response = requests.post(BASE + 'devices', data=json_data)
    print(response.json())
    device_id = response.json()['device_id']
    assert response.status_code == 200
    assert device_id.isdecimal()

    # test put request
    json_data['sw_version'] = "2.0"
    response = requests.put(BASE + 'devices/'+device_id, data=json_data)
    assert response.status_code == 200
    assert device_id == response.json()
    print(response.json())

    # test get request
    response = requests.get(BASE + 'devices/'+device_id)
    assert response.status_code == 200
    assert response.json()['device_id'] == device_id
    assert response.json()['serial_number'] == json_data['serial_number']
    assert response.json()['device_type_id'] == json_data['device_type_id']
    assert response.json()['sw_version'] == json_data['sw_version']
    assert response.json()['mac_address'] == json_data['mac_address']
    assert response.json()['purchased_on'] == json_data['purchased_on']
    print(response.json())

    # test delete request
    response = requests.delete(BASE + 'devices/'+device_id)
    assert response.json() == device_id
    print(response.json())

    # test get request
    response = requests.get(BASE + 'devices')
    assert response.status_code == 200
    print(response)
