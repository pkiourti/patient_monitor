import sys
sys.path.append('./device_module')

from device_measurement import DeviceMeasurement
import time
import os
import json

device_measurements_db_file = os.path.join('db', 'device_measurements.json')
device_assignments_db_file = os.path.join('db', 'device_assignments.json')
devices_db_file = os.path.join('db', 'devices.json')

def test_create_measurement_fail():
    da = DeviceMeasurement()
    data = {"device_type_id": "0",
            "device_id": "3",
            "assignment_id": "0",
            "measurement": "102",
            "timestamp": time.time()}
    json_data = json.dumps(data)
    with open(device_assignments_db_file, 'r') as f:
        assignments = json.load(f)
    assignment = assignments[data['assignment_id']]
    device_id = assignment['device_id']
    try:
        da.record_measurement(json_data)
    except ValueError as e:
        assert e.args[0] == 15
        assert e.args[1] == 'Wrong device id sent. '+\
                            'Expected device '+str(device_id) + \
                            ' but got '+ data['device_id']
    
def test_create_device_success():
    da = DeviceMeasurement()
    data = {}
    data['device_type_id'] = '0'
    data['device_id'] = '0'
    data['assignment_id'] = '0'
    data['measurement'] = '102'
    data['timestamp'] = time.time()
    json_data = json.dumps(data)
    measurement_id = da.record_measurement(json_data)
    with open(device_measurements_db_file, 'r') as f:
        measurements = json.load(f)
    assert measurement_id in measurements
