from itertools import compress
import json
import logging
import time
import os

from device import Device

device_assignments_db_file = os.path.join('db', 'device_assignments.json')

class DeviceAssignment(Device):

    def __init__(self):
        self.logger = logging.getLogger('Device Assignment Logger')
        self.logger.setLevel(logging.DEBUG)

    def create_assignment_id(self):
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        ids = assignments.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        assignment_id = max(ids) + 1
        return assignment_id

    def assign_device(self, device_id, assigned_by, assignee):
        self.logger.info('Assigning device id ' + str(device_id) \
                            + ' to user ' + str(assignee) + ' by ' \
                            + str(assigned_by))
        assigned_at = time.time()
        new_assignment_id = self.create_assignment_id()
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
                         + ' by ' + str(assigned_by) + ' on ' \
                         + str(assigned_at) + ' with assignment id ' \
                         + str(new_assignment_id))
        return new_assignment_id

    def get_assignment(self, assignment_id):
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        if not assignment_id.isdecimal():
            self.logger.error("Assignment id %s " + \
                        "is not an decimal number", assignment_id)
            raise ValueError("Assignment id %s " + \
                        "is not an decimal number", assignment_id)
        if assignment_id not in assignments:
            self.logger.error("Assignment id %s " + \
                        "does not exist", assignment_id)
            raise ValueError("Assignment id %s " + \
                        "does not exist", assignment_id)
        return assignments[str(assignment_id)]

    def get_assignments(self):
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        return assignments

