from device import Device
import pytest
import string
import random
import time
import os
import json

def test_create_device_fail():
    device = Device()
    device_type_id = '0'
    serial_number = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(15)])
    sw_version = 'T1.0'
    mac_address = '00005e0053af'
    purchased_on = time.time()
    try:
        device.create_device(device_type_id, serial_number, sw_version,
                            mac_address, purchased_on)
    except ValueError as e:
        assert e.args[0] == 'MAC Address does not consist of ' + \
                    '6 2-digit hexadecimal groups separated by \":\"'
    
def test_create_device_success():
    device = Device()
    device_type_id = '0'
    serial_number = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(15)])
    sw_version = 'T1.0'
    mac_address = '00:00:5e:00:53:af'
    purchased_on = time.time()
    
    device_id = device.create_device(device_type_id, serial_number, sw_version,
                            mac_address, purchased_on)
    assert type(device_id) == int
    with open(os.path.join('db', 'devices.json'), 'r') as f:
        devices = json.load(f)
    assert str(device_id) in devices
