import logging
import os
import json

device_types_db_file = os.path.join('db', 'device_types.json')

class DeviceType:
    """
    Class that creates a new Device Type
    """

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def check_device_type(self, device_type):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        dev_types = device_types.values()
        dev_types = [dtype.lower() for dtype in dev_types]
        if self.device_type.lower() in device_types.values():
            self.logger.error('Device type ' + self.device_type + ' already exists')
            raise ValueError('Device type ' + self.device_type + ' already exists')

    def create_device_type_id(self):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        ids = device_types.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        device_type_id = max(ids) + 1
        return device_type_id

    def create_device_type(self, device_type):
        self.check_device_type(device_type)
        new_device_type_id = self.create_device_type_id()
        device_types[str(new_device_type_id)] = device_type
        with open(device_types_db_file, 'w') as f:
            data = json.dumps(device_types)
            f.write(data)
        self.logger.info('Created device type with device type id ' + str(device_type_id))
        return device_type_id

    def get_device_type(self, device_type_id):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        if not device_type_id.isdecimal():
            self.logger.error("Device type id %s " + \
                        "is not an decimal number", device_type_id)
            raise ValueError("Device type id %s " + \
                        "is not an decimal number", device_type_id)
        if device_type_id not in device_types:
            self.logger.error('Device type id ' \
                        + device_type_id + ' does not exist')
            raise ValueError('Device type id ' \
                        + device_type_id + ' does not exist')
        device_type = device_types[str(device_type_id)]

        return device_type

    def get_device_types(self):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        return device_types
