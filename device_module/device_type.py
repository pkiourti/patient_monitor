import logging
import os
import json
from itertools import compress

device_types_db_file = os.path.join('db', 'device_types.json')

class DeviceType:
    """
    Class that creates a new Device Type
    """

    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def _check_device_type(self, device_type):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        dev_types = device_types.values()
        dev_types = [dtype.lower() for dtype in dev_types]
        if device_type.lower() in device_types.values():
            self.logger.error('Device type ' + device_type + \
                              ' already exists')
            raise ValueError('Device type ' + device_type + \
                              ' already exists')

    def _check_json(self, data):
        self.logger.info('Parsing sent data')
        try:
            json.loads(data)
        except:
            self.logger.error('Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))
            raise ValueError('Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))

    def _create_device_type_id(self):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        ids = device_types.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        device_type_id = max(ids) + 1
        return device_type_id

    def create_device_type(self, json_data):
        self.logger.info('Creating a new device type')
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['device_type']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError("Missing required data %s", missing_data)

        device_type = json_data['device_type']
        self._check_device_type(device_type)
        new_device_type_id = self._create_device_type_id()
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        device_types[str(new_device_type_id)] = device_type
        with open(device_types_db_file, 'w') as f:
            data = json.dumps(device_types)
            f.write(data)
        self.logger.info('Created device type with device type id ' + \
                         str(new_device_type_id))
        return new_device_type_id

    def get_device_type(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['device_type_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError("Missing required data %s", missing_data)

        device_type_id = json_data['device_type_id']
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
