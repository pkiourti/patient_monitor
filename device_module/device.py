# Use code from https://tinyurl.com/mvj637j6
# to check if a string is hexadecimal

import time
import logging
import string
import json
import os
from itertools import compress

device_db_file = os.path.join('db', 'devices.json')
device_types_db_file = os.path.join('db', 'device_types.json')

class Device:
    """
    Class that creates a new device
    """
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('Device Logger')
        self.logger.setLevel(logging.DEBUG)

    def _check_device_id(self, device_id):
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not device_id.isdecimal():
            self.logger.error("Device id %s " + \
                        "is not an decimal number", device_id)
            raise ValueError(1, "Device id %s " + \
                        "is not an decimal number", device_id)
        if int(device_id) not in ids:
            self.logger.error('Device id ' \
                        + device_id + ' does not exist')
            raise ValueError(2, 'Device id ' \
                        + device_id + ' does not exist')

    def _check_device_type_id(self, device_type_id):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        ids = device_types.keys()
        if not device_type_id.isdecimal():
            self.logger.error("Device type id %s " + \
                        "is not an decimal number", device_type_id)
            raise ValueError(3, "Device type id %s " + \
                        "is not an decimal number", device_type_id)
        if device_type_id not in ids:
            self.logger.error('Device type id ' \
                        + device_type_id + ' does not exist')
            raise ValueError(4, 'Device type id ' \
                        + device_type_id + ' does not exist')

    def _check_mac_address(self, mac_address):
        six_octets = mac_address.split(':')
        if len(six_octets) != 6:
            self.logger.error('MAC Address %s does not consist of ' + \
                    '6 2-digit hexadecimal groups separated by \":\"',
                    mac_address)
            raise ValueError(5, 'MAC Address does not consist of ' + \
                    '6 2-digit hexadecimal groups separated by \":\"',
                    mac_address)
        for hex_part in six_octets:
            if len(hex_part) != 2:
                self.logger.error('MAC Address does not consist of '+ \
                    '2 digit hexadecimal groups. Should be in the format' +\
                    'xx:xx:xx:xx:xx:xx', mac_address)
                raise ValueError(6, 'MAC Address does not consist of '+\
                    '2 digit hexadecimal groups. Should be in the format' +\
                    'xx:xx:xx:xx:xx:xx', mac_address)
            try:
                int(hex_part, 16)
            except ValueError:
                self.logger.error('MAC Address %s does not consist of ' + \
                    'hexadecimal numbers', mac_address)
                raise ValueError(7, 'MAC Address does not consist of ' + \
                    'hexadecimal numbers', mac_address)

    def _check_serial_number(self, serial_number):
        digits = string.digits
        ascii_letters = string.ascii_letters
        for c in serial_number:
            if c not in digits and c not in ascii_letters:
                self.logger.error('Serial Number %s should contain digits ' + \
                    'or ascii letters', serial_number)
                raise ValueError(8, 'Serial Number %s should contain digits ' + \
                    'or ascii letters', serial_number)

    def _check_sw_version(self, sw_version):
        digits = string.digits
        ascii_letters = string.ascii_letters
        for c in sw_version:
            if c not in digits and c not in ascii_letters and c != '.':
                self.logger.error('Software Version %s should contain digits'+\
                    ' ascii letters and/or a dot', sw_version)
                raise ValueError(9, 'Software Version %s should contain digits'+\
                    ' ascii letters and/or a dot', sw_version)
    
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

    def _create_device_id(self):
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        device_id = max(ids) + 1
        return device_id

    def create_device(self, json_data):
        self.logger.info('Creating a new device')

        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['device_type_id', 'serial_number', 'sw_version',
                         'mac_address', 'purchased_on']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        device_type_id = json_data['device_type_id']
        mac_address = json_data['mac_address']
        serial_number = json_data['serial_number']
        sw_version = json_data['sw_version']
        purchased_on = json_data['purchased_on']

        self._check_device_type_id(device_type_id)
        self._check_mac_address(mac_address)
        self._check_serial_number(serial_number)
        self._check_sw_version(sw_version)
        created_at = time.time()
        new_device_id = self._create_device_id()
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        devices[str(new_device_id)] = {
            "device_type_id": str(device_type_id),
            "serial_number": str(serial_number),
            "sw_version": str(sw_version),
            "mac_address": str(mac_address),
            "purchased_on": str(purchased_on),
            "created_at": str(created_at)
        }
        with open(device_db_file, 'w') as f:
            data = json.dumps(devices)
            f.write(data)
        self.logger.info('Created device with device id %s',str(new_device_id))
        return str(new_device_id)

    def get_device(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['device_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        device_id = json_data['device_id']
        self._check_device_id(device_id)
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        return devices[device_id]

    def delete_device(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['device_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        device_id = json_data['device_id']
        self._check_device_id(device_id)
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        self.logger.info('Deleting device with device id %s',str(device_id))
        del devices[device_id]
        with open(device_db_file, 'w') as f:
            data = json.dumps(devices)
            f.write(data)
        self.logger.info('Deleted device with device id %s',str(device_id))
        return device_id
        
    def update_device(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['device_id', 'device_type_id', 'serial_number', 'sw_version',
                         'mac_address', 'purchased_on']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        device_id = json_data['device_id']
        device_type_id = json_data['device_type_id']
        mac_address = json_data['mac_address']
        serial_number = json_data['serial_number']
        sw_version = json_data['sw_version']
        purchased_on = json_data['purchased_on']

        self._check_device_id(device_id)
        self._check_device_type_id(device_type_id)
        self._check_mac_address(mac_address)
        self._check_serial_number(serial_number)
        self._check_sw_version(sw_version)
        updated_at = time.time()

        self.logger.info('Updating device %s', device_id)
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        
        devices[str(device_id)] = {
            "device_type_id": str(device_type_id),
            "serial_number": str(serial_number),
            "sw_version": str(sw_version),
            "mac_address": str(mac_address),
            "purchased_on": str(purchased_on),
            "created_at": devices[str(device_id)]["created_at"],
            "updated_at": updated_at
        }
        with open(device_db_file, 'w') as f:
            data = json.dumps(devices)
            f.write(data)
        self.logger.info('Updated device with device id %s',str(device_id))
        return device_id
        
    def get_devices(self):
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        return devices
