import json
import logging
import time
import os
from itertools import compress

role_assignments_db_file = os.path.join('db', 'role_assignments.json')
roles_db_file = os.path.join('db', 'user_roles.json')
users_db_file = os.path.join('db', 'users.json')

class DeviceAssignment(Device):

    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('Role Assignment Logger')
        self.logger.setLevel(logging.DEBUG)

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

    def _check_user_role_id(self, user_role_id):
        with open(roles_db_file, 'r') as f:
            roles = json.load(f)
        ids = roles.keys()
        if not user_role_id.isdecimal():
            self.logger.error("User role id %s is not an decimal number",
                              user_role_id)
            raise ValueError(1, "User role id %s is not an decimal number",
                              user_role_id)
        if user_role_id not in ids:
            self.logger.error('User role id ' \
                        + str(user_role_id) + ' does not exist')
            raise ValueError(2, 'User role id ' \
                        + str(user_role_id) + ' does not exist')

    def _check_role_assignment_id(self, role_assignment_id):
        with open(role_assignments_db_file, 'r') as f:
            role_assignments = json.load(f)
        if not role_assignment_id.isdecimal():
            self.logger.error("Role assignment id %s " + \
                        "is not an decimal number", role_assignment_id)
            raise ValueError(13, "Role assignment id %s " + \
                        "is not an decimal number", role_assignment_id)
        if role_assignment_id not in role_assignments:
            self.logger.error("Role assignment id %s " + \
                        "does not exist", role_assignment_id)
            raise ValueError(14, "Role assignment id %s " + \
                        "does not exist", role_assignment_id)

    def _create_role_assignment_id(self):
        with open(role_assignments_db_file, 'r') as f:
            role_assignments = json.load(f)
        ids = role_assignments.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        role_assignment_id = max(ids) + 1
        return role_assignment_id

    def assign_role(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['user_role_id', 'user_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        user_role_id = json_data['user_role_id']
        user_id = json_data['user_id']

        self._check_user_role_id(user_role_id)
        self._check_user_id(user_id)

        created_at = time.time()

        self.logger.info('Assigning user role id '+str(user_role_id)+' to user '+user_id)

        new_role_assignment_id = self._create_role_assignment_id()

        with open(role_assignments_db_file, 'r') as f:
            role_assignments = json.load(f)
        role_assignments[str(new_role_assignment_id)] = {
            "user_id": str(user_id),
            "user_role_id": str(user_role_id),
            "created_at": str(created_at),
        }
        with open(role_assignments_db_file, 'w') as f:
            data = json.dumps(role_assignments)
            f.write(data)
        self.logger.info('Successfully assigned user role id ' \
                         + str(user_role_id) + ' to user ' + str(user_id) \
                         + ' with role assignment id ' \
                         + str(new_role_assignment_id))
        return str(new_role_assignment_id)

    def get_role_assignment(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['role_assignment_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        role_assignment_id = json_data['role_assignment_id']
        self._check_role_assignment_id(role_assignment_id)
        with open(role_assignments_db_file, 'r') as f:
            role_assignments = json.load(f)
        return role_assignments[role_assignment_id]

    def delete_role_assignment(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['role_assignment_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        role_assignment_id = json_data['role_assignment_id']
        self._check_role_assignment_id(role_assignment_id)
        self.logger.info('Deleting role assignment id %s', role_assignment_id)
        with open(role_assignments_db_file, 'r') as f:
            role_assignments = json.load(f)

        del role_assignments[role_assignment_id]

        with open(role_assignments_db_file, 'w') as f:
            data = json.dumps(role_assignments)
            f.write(data)
        self.logger.info('Deleted role assignment with role assignment id ' + \
                         str(role_assignment_id))
        return role_assignment_id

    def update_role_assignment(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['role_assignment_id', 'user_role_id', 'user_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        role_assignment_id = json_data['role_assignment_id']
        user_role_id = json_data['user_role_id']
        user_id = json_data['user_id']
        updated_at = json_data['updated_at']

        self._check_role_assignment_id(role_assignment_id)
        self._check_user_role_id(user_role_id)
        updated_at = time.time()

        self.logger.info('Updating role assignment id '+str(role_assignment_id))
        with open(role_assignments_db_file, 'r') as f:
            role_assignments = json.load(f)
        role_assignments[str(role_assignment_id)] = {
            "user_id": str(assignee),
            "user_role_id": str(user_role_id),
            "created_at": role_assignments[str(role_assignment_id)]['assigned_at'],
            "updated_at": updated_at,
        }
        with open(role_assignments_db_file, 'w') as f:
            data = json.dumps(role_assignments)
            f.write(data)
        self.logger.info('Updated role assignment id' + str(role_assignment_id))
        return role_assignment_id

    def get_role_assignments(self):
        with open(role_assignments_db_file, 'r') as f:
            role_assignments = json.load(f)
        return role_assignments
