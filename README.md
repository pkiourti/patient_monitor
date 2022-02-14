# Project 2 - Patient Monitor Platform
## Setup
In order to run the tests or use any part of this code from its home directory you need to set the PYTHONPATH environment variable as follows:
```
$ pwd
/home/penny/ec530/project2/patient_monitor # make sure you are inside the project
$ export PYTHONPATH="${PYTHONPATH}:$(pwd)/device_module"
```

## Documentation
The code currently supports:
1) adding a new device
2) assigning a device to a user 
3) recording a new device measurement
4) getting the available devices, device types, device assignments and device measurements

Since there is no database at the moment, the recorded data are saved and updated to JSON files under the folder db/. The Device Module code can be found under device_module/.

#### 1. Add a new device
```
from device import Device
import random
import string
import time

device = Device()
device_type_id = '0'
chars = string.ascii_letters + string.digits
serial_number = ''.join([random.choice(chars) for _ in range(15)])
sw_version = '1.0'
mac_address = '00:00:5e:00:53:af'
purchased_on = time.time()

new_device_id = device.create_device(device_type_id, serial_number, sw_version,
                            mac_address, purchased_on)

```
#### 2. Assign a new device
```
from device_assignment import DeviceAssignment
import random
import string

da = DeviceAssignment()
device_id = '0'
assigned_by = ''.join([random.choice(string.digits) for _ in range(3)])
assignee = ''.join([random.choice(string.digits) for _ in range(3)])

new_assignment_id = da.assign_device(device_id, assigned_by, assignee)

```
#### 3. Record a new device measurement
```
from device_measurement import DeviceMeasurement
import time
import json

dm = DeviceMeasurement()

data = {}
data['device_type_id'] = '0'
data['device_id'] = '0'
data['assignment_id'] = '0'
data['measurement'] = '102'
data['timestamp'] = time.time()
json_data = json.dumps(data)

new_measurement_id = dm.record_measurement(json_data)

```
#### 4. Get the available devices, device types, device assignments and device measurements
```
from device import Device
from device_type import DeviceType
from device_assignmemnt import DeviceAssignment
from device_measurement import DeviceMeasurement

d = Device()
devices = d.get_devices()
print('Available Devices')
print(json.dumps(devices, indent=4, sort_keys=True))

dt = DeviceType()
device_types = d.get_device_types()
print('Available Device Types')
print(json.dumps(device_types, indent=4, sort_keys=True))

da = DeviceAssignment()
assignments = da.get_assignments()
print('Available Assignments')
print(json.dumps(assignments, indent=4, sort_keys=True))

dm = DeviceMeasurement()
measurements = dm.get_measurements()
print('Available Measurements')
print(json.dumps(measurements, indent=4, sort_keys=True))
```

## Command Line Interface
(Inspired by https://tinyurl.com/ycvsceju)

Run:
```
$ python3 interface.py
```

Output:
```
Welcome to the Patient Monitoring Platform
Your options are:

1) Check the available device types
2) Check the available devices
3) Check the available devices assignments
4) Check the available measurements of a device
5) Add a new device
6) Assign a device to a user
7) Record data using a device and a device assignment
8) Exit
Choose your option: 
```

## Database Schema

#### Users Table
- FristName
- LastName
- DateOfBirth
- Address
- State
- ZipCode
- PhoneNumber
- Email

#### Emergency Contact Table
- UserId
- EmergencyContactId

#### Roles Table
- Id
- Type (Patient, Family, Nurse, Doctor, Staff, Admin, Other)

#### RoleAssignment Table
- UserId
- RoleId
- CreatedAt

#### Measurements Type Table
- MeasurementId
- MeasurementName

#### Measurements Table
- UserId
- DeviceId
- AssignmentId
- MeasurementId
- Measurement
- CreatedAt
- UpdatedAt

#### Devices Type Table
- DeviceTypeId
- DeviceType

#### Devices
- Id
- DeviceTypeId
- Model
- PurchasedOn
- MACAddress
- SWVersion

#### DeviceAssignment Table
- Id 
- UserId
- DeviceId
- AssignedBy
- AssignedAt
- UpdatedAt (will be used when the device was removed for that patient)
