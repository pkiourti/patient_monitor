# Use code from https://stackoverflow.com/questions/11592261/check-if-a-string-is-hexadecimal
# to check if a string is hexadecimal

import time
import logging
import json
import os

device_db_file = os.path.join('db', 'devices.json')
device_types_db_file = os.path.join('db', 'device_types.json')

class Device:
    """
    Class that creates a new device
    """
    def __init__(self):
        self.logger = logging.getLogger('Device Logger')
        self.logger.setLevel(logging.DEBUG)
        
    def check_device_type_id(self, device_type_id):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        ids = device_types.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not device_type_id.isdecimal():
            self.logger.error("Device type id %s " + \
                        "is not an decimal number", device_type_id)
            raise ValueError("Device type id %s " + \
                        "is not an decimal number", device_type_id)
        if int(device_type_id) not in ids:
            self.logger.error('Device type id ' \
                        + str(device_type_id) + ' does not exist')
            raise ValueError('Device id ' \
                        + str(device_type_id) + ' does not exist')

    def check_mac_address(self, mac_address):
        four_hex_parts = mac_address.split(':')
        if len(four_hex_parts) != 4:
            self.logger.error('MAC Address %s does not consist of ' + \
                    '4 hexadecimal parts separated by \":\"', mac_address)
            raise ValueError('MAC Address does not consist of ' + \
                    '4 hexadecimal parts separated by :', mac_address)
        for hex_part in four_hex_parts:
            if len(hex_part) != 4:
                self.logger.error('MAC Address has more than four hex '+\
                    'digits in one of each parts. Should be in the format' +\
                    'xxxx:xxxx:xxxx:xxxx', mac_address)
                raise ValueError('MAC Address has more than four hex '+\
                    'digits in one of each parts. Should be in the format' +\
                    'xxxx:xxxx:xxxx:xxxx', mac_address)
            try:
                int(hex_part, 16)
            except ValueError:
                self.logger.error('MAC Address %s does not consist of ' + \
                    '4 hexadecimal parts', mac_address)
                raise ValueError('MAC Address does not consist of ' + \
                    '4 hexadecimal parts', mac_address)

    def check_serial_number(self, serial_number):
        digits = string.digits
        ascii_letters = string.ascii_letters
        for c in serial_number:
            if c not in digits and c not in ascii_letters:
                self.logger.error('Serial Number %s should contain digits ' + \
                    'or ascii letters', serial_number)
                raise ValueError('Serial Number %s should contain digits ' + \
                    'or ascii letters', serial_number)

    def check_sw_version(self, sw_version):
        digits = string.digits
        ascii_letters = string.ascii_letters
        for c in sw_version:
            if c not in digits and c not in ascii_letters and c != '.':
                self.logger.error('Software Version %s should contain digits ' + \
                    'ascii letters and/or a dot', serial_number)
                raise ValueError('Software Version %s should contain digits ' + \
                    'ascii letters and/or a dot', serial_number)
    
    def create_device_id(self): 
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        device_id = max(ids) + 1
        return device_id

    def create_device(self, device_type_id, serial_number, sw_version, 
                    mac_address, purchased_on):
        self.logger.info('Creating a new device')
        self.check_device_type_id(device_type_id)
        self.check_mac_address(mac_address)
        self.check_serial_number(serial_number)
        self.check_sw_version(sw_version)
        created_at = time.time()
        new_device_id = self.create_device_id()
        devices[str(device_id)] = {
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
        self.logger.info('Created device with device id', device_id)

    def get_device(self, device_id):
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not device_id.isdecimal():
            self.logger.error("Device id %s " + \
                        "is not an decimal number", device_type_id)
            raise ValueError("Device id %s " + \
                        "is not an decimal number", device_type_id)
        if int(device_id) not in ids:
            self.logger.error('Device id ' \
                        + device_id + ' does not exist')
            raise ValueError('Device id ' \
                        + device_id + ' does not exist')
        return devices[device_id]

    def get_devices(self):
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        return devices
