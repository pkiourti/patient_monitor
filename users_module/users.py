# Use code from https://tinyurl.com/mvj637j6
# to check if a string is hexadecimal

import time
import logging
import json
import os
from itertools import compress

users_db_file = os.path.join('db', 'users.json')

class User:
    """
    Class that creates a new user
    """
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('User Logger')
        self.logger.setLevel(logging.DEBUG)

    def _check_user_id(self, user_id):
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        ids = users.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not user_id.isdecimal():
            self.logger.error("User id %s " + \
                        "is not an decimal number", user_id)
            raise ValueError(39, "User id %s " + \
                        "is not an decimal number", user_id)
        if int(user_id) not in ids:
            self.logger.error('User id ' \
                        + user_id + ' does not exist')
            raise ValueError(40, 'User id ' \
                        + user_id + ' does not exist')

    def _check_json(self, data):
        self.logger.info('Parsing sent data')
        print(data)
        print(type(data))
        try:
            json.loads(data)
        except:
            self.logger.error('Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))
            raise ValueError(10, 'Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))

    def _create_user_id(self):
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        ids = users.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        user_id = max(ids) + 1
        return user_id

    def create_user(self, json_data):
        self.logger.info('Creating a new user')

        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['first_name', 'last_name', 'date_of_birth', 'address', 'state',
                         'zipcode', 'phone_number', 'email']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        first_name = json_data['first_name']
        last_name = json_data['last_name']
        date_of_birth = json_data['date_of_birth']
        address = json_data['address']
        state = json_data['state']
        zipcode = json_data['zipcode']
        phone_number = json_data['phone_number']
        email = json_data['email']
        created_at = time.time()

        new_user_id = self._create_user_id()
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        users[str(new_user_id)] = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "address": address,
            "state": state,
            "zipcode": zipcode,
            "phone_number": phone_number,
            "email": email,
            "created_at": created_at
        }
        with open(users_db_file, 'w') as f:
            data = json.dumps(users)
            f.write(data)
        self.logger.info('Created user with user id %s',str(new_user_id))
        return str(new_user_id)

    def get_user(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['user_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_id = json_data['user_id']
        self._check_user_id(user_id)
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        return users[user_id]

    def delete_user(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['user_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_id = json_data['user_id']
        self._check_user_id(user_id)
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        self.logger.info('Deleting user with user id %s',str(user_id))
        del users[user_id]
        with open(users_db_file, 'w') as f:
            data = json.dumps(users)
            f.write(data)
        self.logger.info('Deleted user with user id %s',str(user_id))
        return user_id
        
    def update_user(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['user_id', 'first_name', 'last_name', 'date_of_birth', 
                         'address', 'state', 'zipcode', 'phone_number', 'email']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_id = json_data['user_id']
        first_name = json_data['first_name']
        last_name = json_data['last_name']
        date_of_birth = json_data['date_of_birth']
        address = json_data['address']
        state = json_data['state']
        zipcode = json_data['zipcode']
        phone_number = json_data['phone_number']
        email = json_data['email']
        updated_at = time.time()

        self._check_user_id(user_id)

        self.logger.info('Updating user %s', user_id)
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        
        users[str(user_id)] = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "address": address,
            "state": state,
            "zipcode": zipcode,
            "phone_number": phone_number,
            "email": email,
            "created_at": users[str(user_id)]["created_at"],
            "updated_at": updated_at
        }
        with open(users_db_file, 'w') as f:
            data = json.dumps(users)
            f.write(data)
        self.logger.info('Updated user with user id %s',str(user_id))
        return user_id
        
    def get_users(self):
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        return users
