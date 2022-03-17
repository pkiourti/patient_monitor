import requests

BASE = "http://127.0.0.1:5000/"

def test_message_api():
    # test post request
    session_id = "0"
    message = {"text": "Hello"}
    sender = '12'
    json_data = {}
    json_data["session_id"] = session_id
    json_data["message"] = message
    json_data["sender"] = sender
    response = requests.post(BASE + 'messages', json=json_data)
    print(response.json())
    message_id = response.json()["message_id"]
    assert response.status_code == 200
    assert message_id.isdecimal()

    # test put request
    json_data["message"] = {"text": "Hello!"}
    response = requests.put(BASE + 'messages/'+message_id, json=json_data)
    assert response.status_code == 200
    assert message_id == response.json()
    print(response.json())

    # test get request
    response = requests.get(BASE + 'messages/'+message_id)
    assert response.status_code == 200
    assert response.json()["message_id"] == message_id
    assert response.json()["session_id"] == session_id
    assert response.json()["sender"] == json_data["sender"]
    if "text" in response.json()["message"]:
        assert response.json()["message"]["text"] == json_data["message"]["text"]
    print(response.json())

    # test delete request
    #response = requests.delete(BASE + 'messages/'+message_id)
    #assert response.json() == message_id
    #print(response.json())

    # test get request
    response = requests.get(BASE + 'messages')
    assert response.status_code == 200
    print(response)
