# use code to prettyprint a json from https://tinyurl.com/3mmbzvdd
# use example interface from https://tinyurl.com/ycvsceju

import sys
sys.path.append('./device_module')

from device_type import DeviceType
from device import Device
from device_assignment import DeviceAssignment
from device_measurement import DeviceMeasurement
import json
import os
import time

device_assignments_db_file = os.path.join('db', 'device_assignments.json')
device_measurements_db_file = os.path.join('db', 'device_measurements.json')
devices_db_file = os.path.join('db', 'devices.json')
device_types_db_file = os.path.join('db', 'device_types.json')


if __name__ == '__main__':
    print('Welcome to the Patient Monitoring Platform')
    while True:
        print('Your options are:')
        print()
        print('1) Check the available device types')
        print('2) Check the available devices')
        print('3) Check the available devices assignments')
        print('4) Check the available measurements of a device')
        print('5) Add a new device')
        print('6) Assign a device to a user')
        print('7) Record data using a device and a device assignment')
        print('8) Exit')
        
        choice = input("Choose your option: ")
        choice = int(choice)
        if choice == 1:
            dt = DeviceType()
            device_types = dt.get_device_types()
            print('Available Device Types:')
            print(json.dumps(device_types, indent=4, sort_keys=True))
        elif choice == 2:
            device = Device()
            devices = device.get_devices()
            print('Available Devices:')
            print(json.dumps(devices, indent=4, sort_keys=True))
        elif choice == 3:
            d = DeviceAssignment()
            assignments = d.get_assignments()
            print('Available Assignments:')
            print(json.dumps(assignments, indent=4, sort_keys=True))
        elif choice == 4:
            d = DeviceMeasurement()
            measurements = d.get_measurements()
            print('Available Measurements:')
            print(json.dumps(measurements, indent=4, sort_keys=True))
        elif choice == 5:
            device_type_id = input("Write the device type id of the device you want to add: ")
            serial_number = input("Write the serial number of the device you want to add: ")
            sw_version = input("Write the software version of the device you want to add: ")
            mac_address = input("Write the MAC address of the device you want to add: ")
            purchased_on = input("Write the date of the purchase of the device you want to add: ")
            json_data = {}
            json_data['device_type_id'] = device_type_id
            json_data['serial_number'] = serial_number
            json_data['sw_version'] = sw_version
            json_data['mac_address'] = mac_address
            json_data['purchased_on'] = purchased_on
            json_data = json.dumps(json_data)
            dev = Device()
            try:
                dev.create_device(json_data)
            except ValueError:
                pass
        elif choice == 6:
            device = Device()
            devices = device.get_devices()
            print('Available Devices:')
            print(json.dumps(devices, indent=4, sort_keys=True))
            print()
            device_id = input('Write the device id you want to assign: ')
            assigner = input('Write the user id of the assigner: ')
            assignee = input('Write the user id of the assignee: ')
            d = DeviceAssignment()
            json_data = {}
            json_data['device_id'] = device_id
            json_data['assigned_by'] = assigner
            json_data['assignee'] = assignee
            json_data = json.dumps(json_data)
            try:
                dev_assignment = d.assign_device(json_data)
            except ValueError:
                pass
        elif choice == 7:
            d = DeviceAssignment()
            assignments = d.get_assignments()
            print('Available Assignments:')
            print(json.dumps(assignments, indent=4, sort_keys=True))
            print()
            assignment_id = input('Write the assignment id you want to use: ')
            json_data = {}
            json_data['assignment_id'] = assignment_id
            json_data = json.dumps(json_data)
            try:
                assignment = d.get_assignment(json_data)
                device_id = assignment['device_id']
            except ValueError:
                continue
            try:
                json_data = {}
                json_data['device_id'] = device_id
                json_data = json.dumps(json_data)
                device = Device().get_device(json_data)
                device_type_id = device['device_type_id']
            except ValueError:
                continue
            try:
                json_data = {}
                json_data['device_type_id'] = device_type_id
                json_data = json.dumps(json_data)
                device_type = DeviceType().get_device_type(json_data)
            except ValueError:
                continue
            if device_type == 'temperature':
                data = input('Write the temperature you want to record in Fahrenheit: ')
                json_data = {"measurement": str(data)}
            if device_type == 'blood_pressure':
                systolic_data = input('Write the systolic blood pressure you want to record in mmHg: ')
                diastolic_data = input('Write the diastolic blood pressure you want to record in mmHg: ')
                json_data = {
                              "measurement": {
                                "systolic": str(systolic_data),
                                "diastolic": str(diastolic_data)
                              }
                            }
            if device_type == 'oximeter':
                data = input('Write the blood oxygen you want to record in percentage: ')
                json_data = {"measurement": str(data)}
            if device_type == 'pulse':
                data = input('Write the pulse you want to record in beats per minute: ')
                json_data = {"measurement": str(data)}
            if device_type == 'weight':
                data = input('Write the weight you want to record in pounds: ')
                json_data = {"measurement": str(data)}
            if device_type == 'glucometer':
                data = input('Write the blood glucose level you want to record in mg/dL: ')
                json_data = {"measurement": str(data)}
            json_data['timestamp'] = time.time()
            json_data['device_id'] = device_id
            json_data['device_type_id'] = device_type_id
            json_data['assignment_id'] = assignment_id
            json_data = json.dumps(json_data)
            try:
                DeviceMeasurement().record_measurement(json_data)
            except ValueError:
                pass
        elif choice == 8:
            exit(0)
