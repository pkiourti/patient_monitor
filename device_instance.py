from device import Device
import random
import string
import json
import logging
import time

device_assignments_db_file = 'device_assignments.json'
device_measurements_db_file = 'device_measurements.json'
devices_db_file = 'devices.json'
device_types_db_file = 'device_types.json'

class DeviceInstance(Device):

    def __init__(self, device_id, assigner, assignee):
        self.logger = logging.getLogger('Device Assignment Logger')
        self.device_id = device_id
        self.owner = assignee
        self.assigner = assigner
        self.assignment_id = self.__create_assignment_id(device_id, assigner, assignee)
        self.device_type = self.get_device_type()

    def __create_assignment_id(self, number, assigned_by, assignee):
        self.logger.info('Assigning device id ' + str(self.device_id) \
                            + ' to user ' + str(assignee) + ' by ' \
                            + str(assigned_by))
        assigned_at = time.time()
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        ids = assignments.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        assignment_id = max(ids) + 1
        assignments[str(assignment_id)] = {
            "user_id": str(self.owner),
            "device_id": str(self.device_id),
            "assigned_by": str(self.assigner),
            "assigned_at": str(assigned_at),
        }
        with open(device_assignments_db_file, 'w') as f:
            data = json.dumps(assignments)
            f.write(data)
        self.logger.info('User ' + str(assigned_by) + ' assigned device id ' \
                         + str(self.device_id) + ' to user ' + str(assignee) \
                         + ' by ' + str(assigned_by) + ' on ' \
                         + str(assigned_at) + ' with assignment id ' \
                         + str(assignment_id))
        return assignment_id

    def record_data(self, data):
        self.logger.info(str(self.assignment_id) + ': parsing sent data')
        json_data = ''
        try:
            json_data = json.loads(data)
        except:
            self.logger.error(str(self.assignment_id) \
                             + ': Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))
            raise ValueError(str(self.assignment_id) \
                             + ': Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))

        if self.device_type not in json_data:
            self.logger.error(str(self.assignment_id) + ': ' \
                             + self.device_type \
                             + ' data are not included in the data sent')
            raise ValueError(str(self.assignment_id) + ': ' \
                             + self.device_type \
                             + ' data are not included in the data sent')
        device_type_data = json_data[self.device_type]
        self.logger.info(str(self.assignment_id) \
                             + ': Checking measurement data sent from device '\
                             + str(self.device_id))
        self.check_data(device_type_data)
        self.logger.info(str(self.assignment_id) \
                             + ': Creating a new measurement')
        created_at = time.time()
        with open(device_measurements_db_file, 'r') as f:
            measurements = json.load(f)
        ids = measurements.keys()
        ids = [id for id in ids] if ids else [-1]
        measurement_id = max(ids) + 1
        measurements[str(measurement_id)] = {
            "user_id": str(),
            "device_id": str(self.device_id),
            "assignment_id": str(self.assignment_id),
            "measurement": str(data),
            "created_at": str(created_at)
        }
        with open(device_measurements_db_file, 'w') as f:
            data = json.dumps(measurements)
            f.write(data)
        self.logger.info(str(self.assignment_id) \
                        + ': Created a new measurement with measurement id ' \
                        + str(measurement_id))

    def get_device_type(self):
        with open(devices_db_file, 'r') as f:
            devices = json.load(f)
        if str(self.device_id) not in devices:
            self.logger.error(str(self.assignment_id) + ': Device id ' \
                        + str(self.device_id) + ' does not exist')
            raise ValueError(str(self.assignment_id) + ': Device id ' \
                        + str(self.device_id) + ' does not exist')
        device = devices[str(self.device_id)]
        device_type_id = int(device['device_type_id'])
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        if str(device_type_id) not in device_types:
            self.logger.error(str(self.assignment_id) + ': Device type id ' \
                        + str(device_type_id) + ' does not exist')
            raise ValueError(str(self.assignment_id) + ': Device type id ' \
                        + str(device_type_id) + ' does not exist')
        device_type = device_types[str(device_type_id)]
        return device_type

    def check_data(self, data):
        if self.device_type == 'temperature':
            data = float(data)
            if data > 105 or data < 82:
                self.logger.error(str(self.assignment_id) + ': ' 
                        + self.device_type \
                        + ' data sent are outside of possible range '\
                        + '[82 Fahrenheit, 105 Fahrenheit]')
                raise ValueError(str(self.assignment_id) + ': ' 
                        + self.device_type \
                        + ' data sent are outside of possible range '\
                        + '[82 Fahrenheit, 105 Fahrenheit]')
