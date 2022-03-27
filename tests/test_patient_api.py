import requests

BASE = "http://127.0.0.1:5000/"

def test_patient_api():
    # test post request
    json_data = {}
    json_data['emergency_contact_id'] = "0"
    json_data['user_id'] = "1"
    json_data['patient_history'] = {"heart_disease": "Yes"}
    response = requests.post(BASE + 'patients', json=json_data)
    print(response.json())
    patient_id = response.json()['patient_id']
    assert response.status_code == 200
    assert patient_id.isdecimal()

    # test put request
    json_data['patient_history'] = {"diabetes": "Yes"}
    response = requests.put(BASE + 'patients/'+patient_id, json=json_data)
    assert response.status_code == 200
    assert patient_id == response.json()
    print(response.json())

    # test get request
    response = requests.get(BASE + 'patients/'+patient_id)
    assert response.status_code == 200
    assert response.json()['patient_id'] == patient_id
    assert response.json()['user_id'] == json_data['user_id']
    assert response.json()['emergency_contact_id'] == json_data['emergency_contact_id']
    print(response.json())
    if "diabetes" in response.json()["patient_history"]:
        assert response.json()["patient_history"]["diabetes"] == json_data["patient_history"]["diabetes"]

    print(response.json())

    # test delete request
    response = requests.delete(BASE + 'patients/'+patient_id)
    assert response.json() == patient_id
    print(response.json())

    # test get request
    response = requests.get(BASE + 'patients')
    assert response.status_code == 200
    print(response)
