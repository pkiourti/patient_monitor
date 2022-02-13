from device_instance import DeviceInstance
from device_type import DeviceType
from device import Device
import json
import os

device_assignments_db_file = os.path.join('db', 'device_assignments.json')
device_measurements_db_file = os.path.join('db', 'device_measurements.json')
devices_db_file = os.path.join('db', 'devices.json')
device_types_db_file = os.path.join('db', 'device_types.json')


if __name__ == '__main__':
    print('Welcome to the Patient Monitoring Platform')
    while True:
        print('Your options are:')
        print()
        print('1) Add a device type')
        print('2) Add a device')
        print('3) Check the available device types')
        print('4) Check the available devices')
        print('5) Assign a device to a user')
        print('6) Record data using a device and a device assignment')
        print('7) Exit')
        
        choice = input("Choose your option: ")
        choice = int(choice)
        if choice == 1:
            dtype = input("Write the type of the device you want to add: ")
            try:
                device_type = DeviceType(dtype)
            except ValueError as e:
                pass
        elif choice == 2:
            device_type_id = input("Write the device type id of the device you want to add: ")
            serial_number = input("Write the serial number of the device you want to add: ")
            sw_version = input("Write the software version of the device you want to add: ")
            mac_address = input("Write the MAC address of the device you want to add: ")
            purchased_on = input("Write the date of the purchase of the device you want to add: ")
            dev = Device(device_type_id, serial_number, sw_version, mac_address, purchased_on)
        elif choice == 3:
            with open(device_types_db_file, 'r') as f:
                device_types = json.load(f)
            print('Available Device Types:')
            print(json.dumps(device_types, indent=4, sort_keys=True))
        elif choice == 4:
            with open(devices_db_file, 'r') as f:
                devices = json.load(f)
            print('Available Devices:')
            print(json.dumps(devices, indent=4, sort_keys=True))
        elif choice == 5:
            with open(devices_db_file, 'r') as f:
                devices = json.load(f)
            print('Available Devices:')
            print(json.dumps(devices, indent=4, sort_keys=True))
            print()
            device_id = input('Write the device id you want to assign: ') 
            assigner = input('Write the user id of the assigner: ') 
            assignee = input('Write the user id of the assignee: ') 
            try:
                dev_assignment = DeviceInstance(device_id, assigner, assignee)
            except ValueError as e:
                pass
        elif choice == 6:
            print('You need to first assign a device to a user: ')
            with open(devices_db_file, 'r') as f:
                devices = json.load(f)
            print('Available Devices:')
            print(json.dumps(devices, indent=4, sort_keys=True))
            print()
            device_id = input('Write the device id you want to assign: ') 
            assigner = input('Write the user id of the assigner: ') 
            assignee = input('Write the user id of the assignee: ') 
            try:
                dev_assignment = DeviceInstance(device_id, assigner, assignee)
            except ValueError as e:
                continue
            device_type = dev_assignment.device_type
            if device_type == 'temperature':
                data = input('Write the temperature you want to record in Fahrenheit: ')
                json_data = {"temperature": str(data)}
            if device_type == 'blood_pressure':
                systolic_data = input('Write the systolic blood pressure you want to record in mmHg: ')
                diastolic_data = input('Write the diastolic blood pressure you want to record in mmHg: ')
                json_data = {"blood_pressure": {"systolic": str(systolic_data), "diastolic": str(diastolic_data)}}
            if device_type == 'oximeter':
                data = input('Write the blood oxygen you want to record in percentage: ')
                json_data = {"oximeter": str(data)}
            if device_type == 'pulse':
                data = input('Write the pulse you want to record in beats per minute: ')
                json_data = {"pulse": str(data)}
            if device_type == 'weight':
                data = input('Write the weight you want to record in pounds: ')
                json_data = {"weight": str(data)}
            if device_type == 'glucometer':
                data = input('Write the blood glucose level you want to record in mg/dL: ')
                json_data = {"glucometer": str(data)}
            json_data = json.dumps(json_data)
            try:
                dev_assignment.record_data(json_data)
            except ValueError as e:
                pass
        elif choice == 7:
            exit(0)
