from device import Device
import random
import string
import time
import os
import json

def test_create_device_fail():
    device = Device()
    chars = string.ascii_letters + string.digits
    data = {"device_type_id": "0",
            "serial_number": ''.join([random.choice(chars) for _ in range(15)]),
            "sw_version": "T1.0",
            "mac_address": "00005e0053af",
            "purchased_on": time.time()}
    json_data = json.dumps(data)
    try:
        device.create_device(json_data)
    except ValueError as e:
        assert e.args[0] == 5
        assert e.args[1] == 'MAC Address does not consist of ' + \
                    '6 2-digit hexadecimal groups separated by \":\"'
    
def test_create_device_success():
    device = Device()
    chars = string.ascii_letters + string.digits
    data = {"device_type_id": "0",
            "serial_number": ''.join([random.choice(chars) for _ in range(15)]),
            "sw_version": "T1.0",
            "mac_address": "00:00:5e:00:53:af",
            "purchased_on": time.time()}
    json_data = json.dumps(data)
    
    try:
        device_id = device.create_device(json_data)
    except ValueError as e:
        raise ValueError("Expected to create new device with " + str(data) + \
                         " but got a Value Error " + e.args[0])

    with open(os.path.join('db', 'devices.json'), 'r') as f:
        devices = json.load(f)
    assert device_id in devices
