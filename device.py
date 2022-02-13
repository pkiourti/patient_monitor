import time
import logging
import json

device_db_file = 'devices.json'

class Device:
    """
    Class that creates a new device
    """
    def __init__(self, device_type_id, serial_number, sw_version, mac_address,
                    purchased_on):
        self.device_type_id = device_type_id
        self.serial_number = serial_number
        self.sw_version = sw_version
        self.mac_address = mac_address
        self.purchased_on = purchased_on
        self.logger = logging.getLogger('Device Logger')
        self.device_id = self.create_device_id()
        
    def create_device_id(self):
        self.logger.info('Creating a new device')
        created_at = time.time()
        with open(device_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        device_id = max(ids) + 1
        self.logger.info('Created device with device id', device_id)
        devices[str(device_id)] = {
            "device_type_id": str(self.device_type_id),
            "serial_number": str(self.serial_number),
            "sw_version": str(self.sw_version),
            "mac_address": str(self.mac_address),
            "purchased_on": str(self.purchased_on),
            "created_at": str(created_at)
        }
        with open(device_db_file, 'w') as f:
            data = json.dumps(devices)
            f.write(data)
        return device_id

