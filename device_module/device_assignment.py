import json
import logging
import time
import os
from itertools import compress

from device import Device

device_assignments_db_file = os.path.join('db', 'device_assignments.json')
devices_db_file = os.path.join('db', 'devices.json')

class DeviceAssignment(Device):

    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('Device Assignment Logger')
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

    def _check_device_id(self, device_id):
        with open(devices_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        if not device_id.isdecimal():
            self.logger.error("Device id %s is not an decimal number",
                              device_id)
            raise ValueError(1, "Device id %s is not an decimal number",
                              device_id)
        if device_id not in ids:
            self.logger.error('Device id ' \
                        + str(device_id) + ' does not exist')
            raise ValueError(2, 'Device id ' \
                        + str(device_id) + ' does not exist')

    def _check_assignment_id(self, assignment_id):
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        if not assignment_id.isdecimal():
            self.logger.error("Assignment id %s " + \
                        "is not an decimal number", assignment_id)
            raise ValueError(13, "Assignment id %s " + \
                        "is not an decimal number", assignment_id)
        if assignment_id not in assignments:
            self.logger.error("Assignment id %s " + \
                        "does not exist", assignment_id)
            raise ValueError(14, "Assignment id %s " + \
                        "does not exist", assignment_id)

    def _create_assignment_id(self):
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        ids = assignments.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        assignment_id = max(ids) + 1
        return assignment_id

    def assign_device(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['device_id', 'assigned_by', 'assignee']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        device_id = json_data['device_id']
        assigned_by = json_data['assigned_by']
        assignee = json_data['assignee']

        self._check_device_id(device_id)

        assigned_at = time.time()

        self.logger.info('Assigning device id '+str(device_id)+' to user '+assignee+' by '+assigned_by)

        new_assignment_id = self._create_assignment_id()

        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        assignments[str(new_assignment_id)] = {
            "user_id": str(assignee),
            "device_id": str(device_id),
            "assigned_by": str(assigned_by),
            "assigned_at": str(assigned_at),
        }
        with open(device_assignments_db_file, 'w') as f:
            data = json.dumps(assignments)
            f.write(data)
        self.logger.info('User ' + str(assigned_by) \
                         + ' successfully assigned device id ' \
                         + str(device_id) + ' to user ' + str(assignee) \
                         + ' on ' \
                         + str(assigned_at) + ' with assignment id ' \
                         + str(new_assignment_id))
        return str(new_assignment_id)

    def get_assignment(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['assignment_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        assignment_id = json_data['assignment_id']
        self._check_assignment_id(assignment_id)
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        return assignments[assignment_id]

    def delete_assignment(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['assignment_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        assignment_id = json_data['assignment_id']
        self._check_assignment_id(assignment_id)
        self.logger.info('Deleting assignment id %s', assignment_id)
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)

        del assignments[assignment_id]

        with open(device_assignments_db_file, 'w') as f:
            data = json.dumps(assignments)
            f.write(data)
        self.logger.info('Deleted assignment with assignment id ' + \
                         str(assignment_id))
        return assignment_id

    def update_assignment(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['assignment_id', 'device_id', 'assigned_by', 'assignee']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        assignment_id = json_data['assignment_id']
        device_id = json_data['device_id']
        assigned_by = json_data['assigned_by']
        assignee = json_data['assignee']

        self._check_assignment_id(assignment_id)
        self._check_device_id(device_id)
        updated_at = time.time()

        self.logger.info('Updating assignment id '+str(assignment_id))
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        assignments[str(assignment_id)] = {
            "user_id": str(assignee),
            "device_id": str(device_id),
            "assigned_by": str(assigned_by),
            "created_at": assignments[str(assignment_id)]['assigned_at'],
            "updated_at": updated_at,
        }
        with open(device_assignments_db_file, 'w') as f:
            data = json.dumps(assignments)
            f.write(data)
        self.logger.info('Updated assignment id' + str(assignment_id))
        return assignment_id

    def get_assignments(self):
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        return assignments
