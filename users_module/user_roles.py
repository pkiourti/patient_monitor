import logging
import os
import json
from itertools import compress

user_roles_db_file = os.path.join('db', 'user_roles.json')

class UserRole:
    """
    Class that creates a new user role
    """

    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('User roles Logger')
        self.logger.setLevel(logging.DEBUG)

    def _check_role_id(self, role_id):
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        if not user_role_id.isdecimal():
            self.logger.error("Role id %s " + \
                        "is not an decimal number", user_role_id)
            raise ValueError(3, "Role id %s " + \
                        "is not an decimal number", user_role_id)
        if user_role_id not in user_roles:
            self.logger.error('Role id ' \
                        + user_role_id + ' does not exist')
            raise ValueError(4, 'Role id ' \
                        + user_role_id + ' does not exist')

    def _check_user_role(self, user_role):
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        user_roles = user_roles.values()
        user_roles = [role.lower() for role in user_roles]
        if user_role.lower() in user_roles.values():
            self.logger.error('User role ' + user_role + \
                              ' already exists')
            raise ValueError(12, 'User role ' + user_role + \
                              ' already exists')

    def _check_json(self, data):
        self.logger.info('Parsing sent data')
        try:
            json.loads(data)
        except:
            self.logger.error('Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))
            raise ValueError(10, 'Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))

    def _create_user_role_id(self):
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        ids = user_roles.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        user_role_id = max(ids) + 1
        return user_role_id

    def create_user_role(self, json_data):
        self.logger.info('Creating a new user role')
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['user_role']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_role = json_data['user_role']
        self._check_user_role(user_role)
        new_user_role_id = self._create_user_role_id()
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        user_roles[str(new_user_role_id)] = user_role
        with open(user_roles_db_file, 'w') as f:
            data = json.dumps(user_roles)
            f.write(data)
        self.logger.info('Created user role with user role id ' + \
                         str(new_user_role_id))
        return str(new_user_role_id)

    def get_user_role(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['user_role_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_role_id = json_data['user_role_id']
        self._check_user_role_id(user_role_id)
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        user_role = user_roles[str(user_role_id)]

        return {"user_role": user_role}

    def update_user_role(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['user_role_id', 'user_role']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_role_id = json_data['user_role_id']
        user_role = json_data['user_role']

        self._check_user_role_id(user_role_id)
        self._check_user_role(user_role)

        self.logger.info('Updating user role %s', user_role_id)
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        user_roles[str(user_role_id)] = user_role
        with open(user_roles_db_file, 'w') as f:
            data = json.dumps(user_roles)
            f.write(data)
        self.logger.info('Updated user role with user role id ' + \
                         str(user_role_id))
        return user_role_id

    def delete_user_role(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)

        required_data = ['user_role_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_role_id = json_data['user_role_id']

        self._check_user_role_id(user_role_id)

        self.logger.info('Deleting user role %s', user_role_id)
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        del user_roles[user_role_id]
        with open(user_roles_db_file, 'w') as f:
            data = json.dumps(user_roles)
            f.write(data)
        self.logger.info('Deleted user role with user role id ' + \
                         str(user_role_id))
        return user_role_id

    def get_user_roles(self):
        with open(user_roles_db_file, 'r') as f:
            user_roles = json.load(f)
        return user_roles
