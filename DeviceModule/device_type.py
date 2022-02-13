import logging
import os
import json

device_types_db_file = os.path.join('db', 'device_types.json')

class DeviceType:
    """
    Class that creates a new Device Type
    """

    def __init__(self, dtype):
        self.device_type = dtype
        self.logger = logging.getLogger(dtype)
        self.logger.setLevel(logging.DEBUG)
        self.device_type_id = self.create_device_type()

    def create_device_type(self):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        dev_types = device_types.values()
        dev_types = [dtype.lower() for dtype in dev_types]
        if self.device_type.lower() in device_types.values():
            self.logger.error('Device type ' + self.device_type + ' already exists')
            raise ValueError('Device type ' + self.device_type + ' already exists')
        ids = device_types.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        device_type_id = max(ids) + 1
        self.logger.info('Created device type with device type id ' + str(device_type_id))
        device_types[str(device_type_id)] = self.device_type
        with open(device_types_db_file, 'w') as f:
            data = json.dumps(device_types)
            f.write(data)
        return device_type_id
