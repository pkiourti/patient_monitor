import requests
import time
import json

BASE = "http://127.0.0.1:5000/"

def test_measurement_api():
    # test post request
    json_data = {}
    json_data['device_id'] = '0'
    json_data['device_type_id'] = '0'
    json_data['assignment_id'] = '0'
    json_data['measurement'] = '102'
    json_data['timestamp'] = str(time.time())
    response = requests.post(BASE + 'device_measurements', data=json_data)
    measurement_id = response.json()['measurement_id']
    assert response.status_code == 200
    assert measurement_id.isdecimal() 
    print(response.json())

    # test put request
    json_data['measurement'] = '100'
    response = requests.put(BASE + 'device_measurements/'+measurement_id, data=json_data)
    assert response.status_code == 200

    # test get request
    response = requests.get(BASE + 'device_measurements/'+measurement_id)
    print(response.json())
    assert response.status_code == 200
    assert measurement_id == response.json()['measurement_id']
    assert json_data['device_id'] == response.json()['device_id']
    assert json_data['assignment_id'] == response.json()['assignment_id']
    assert json_data['measurement'] == response.json()['measurement']['temperature']
    assert json_data['timestamp'] == response.json()['measurement']['timestamp']
    print(response.json())

    # test get request
    response = requests.get(BASE + 'device_measurements')
    assert response.status_code == 200

    # test delete request
    response = requests.delete(BASE + 'device_measurements/'+measurement_id)
    assert response.status_code == 200
    assert response.json() == measurement_id
