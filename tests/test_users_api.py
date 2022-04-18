#import requests

#BASE = "http://127.0.0.1:5000/"

#def test_users_api():
#   # test post request
#   json_data = {}
#   json_data['first_name'] = "Penny"
#   json_data['last_name'] = "Kiourti"
#   json_data['date_of_birth'] = "01-01-2000"
#   json_data['address'] = "St. Mary's St"
#   json_data['state'] = "MA"
#   json_data['zipcode'] = "02215"
#   json_data['phone_number'] = "6173535050"
#   json_data['email'] = "pkiourti@bu.edu"
#   response = requests.post(BASE + 'users', data=json_data)
#   print(response.json())
#   user_id = response.json()['user_id']
#   assert response.status_code == 200
#   assert user_id.isdecimal()
#
#   # test put request
#   json_data = {}
#   json_data['first_name'] = "Panagiota"
#   json_data['last_name'] = "Kiourti"
#   json_data['date_of_birth'] = "01-01-2000"
#   json_data['address'] = "St. Mary's St"
#   json_data['state'] = "MA"
#   json_data['zipcode'] = "02215"
#   json_data['phone_number'] = "6173535050"
#   json_data['email'] = "pkiourti@bu.edu"
#   response = requests.put(BASE + 'users/'+user_id, data=json_data)
#   assert response.status_code == 200
#   assert user_id == response.json()
#   print(response.json())
#
#   # test get request
#   response = requests.get(BASE + 'users/'+user_id)
#   assert response.status_code == 200
#   assert response.json()['user_id'] == user_id
#   assert response.json()['first_name'] == json_data['first_name']
#   assert response.json()['last_name'] == json_data['last_name']
#   assert response.json()['date_of_birth'] == json_data['date_of_birth']
#   assert response.json()['address'] == json_data['address']
#   assert response.json()['state'] == json_data['state']
#   assert response.json()['zipcode'] == json_data['zipcode']
#   assert response.json()['phone_number'] == json_data['phone_number']
#   assert response.json()['email'] == json_data['email']
#   print(response.json())
#
#   # test delete request
#   response = requests.delete(BASE + 'users/'+user_id)
#   assert response.json() == user_id
#   print(response.json())
#
#   # test get request
#   response = requests.get(BASE + 'users')
#   assert response.status_code == 200
#   print(response)
