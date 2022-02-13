from device_assignment import DeviceAssignment
import string
import random
import os
import json

device_assignments_db_file = os.path.join('db', 'device_assignments.json')

def test_create_assignment_fail():
    da = DeviceAssignment()
    device_id = '500'
    assigned_by = ''.join([random.choice(string.digits) for _ in range(3)])
    assignee = ''.join([random.choice(string.digits) for _ in range(3)])
    try:
        da.assign_device(device_id, assigned_by, assignee)
    except ValueError as e:
        assert e.args[0] == 'Device id ' \
                        + device_id + ' does not exist'
    
def test_create_device_success():
    da = DeviceAssignment()
    device_id = '0'
    assigned_by = ''.join([random.choice(string.digits) for _ in range(3)])
    assignee = ''.join([random.choice(string.digits) for _ in range(3)])
    assignment_id = da.assign_device(device_id, assigned_by, assignee)
    assert type(assignment_id) == int
    with open(device_assignments_db_file, 'r') as f:
        assignments = json.load(f)
    assert str(assignment_id) in assignments
