import requests

BASE = "http://127.0.0.1:5000/"

def test_device_assignment_api():
    # test post request
    json_data = {}
    json_data['device_id'] = '12'
    json_data['assignee'] = '10'
    json_data['assigned_by'] = '4'
    response = requests.post(BASE + 'device_assignments', data=json_data)
    assignment_id = response.json()['assignment_id']
    assert response.status_code == 200
    assert assignment_id.isdecimal()
    print(response.json())
    
    # test put request
    json_data['assigned_by'] = '5'
    response = requests.put(BASE + 'device_assignments/'+assignment_id, data=json_data)
    assert response.status_code == 200
    assert response.json() == assignment_id
    print(response.json())
    
    # test get request
    response = requests.get(BASE + 'device_assignments/'+assignment_id)
    assert response.status_code == 200
    assert response.json()['assignment_id'] == assignment_id
    assert response.json()['device_id'] == json_data['device_id']
    assert response.json()['user_id'] == json_data['assignee']
    assert response.json()['assigned_by'] == json_data['assigned_by']
    print(response.json())
    
    # test get request
    response = requests.get(BASE + 'device_assignments')
    assert response.status_code == 200
    print(response.json())
    
    # test delete request
    response = requests.delete(BASE + 'device_assignments/'+assignment_id)
    assert response.status_code == 200
    assert response.json() == assignment_id
    print(response.json())
