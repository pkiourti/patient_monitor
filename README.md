# Project 2 - Patient Monitor Platform
### NOTE: Project 4 exists in a different repository - please check here: https://github.com/pkiourti/queue-system
## Setup
In order to run the tests or use any part of this code from its home directory you need to set the FLASK environment variable as follows:
```
$ pwd
/home/penny/ec530/project2/patient_monitor # make sure you are inside the project
$ export FLASK_APP="application.py"
$ flask run
```
## Screenshots of React Native App
Screenshots of the login screen and the Users Table fetched by the backend:
- <img src="https://github.com/pkiourti/patient_monitor/blob/main/screenshots/login-screen.png" width="250" height="400">
- <img src="https://github.com/pkiourti/patient_monitor/blob/main/screenshots/users-table-start.png" width="250" height="400">

## Screenshots of API
Screenshots of GET requests can be found under the folder screenshots. Example:
![Screenshot of GET devices request](https://github.com/pkiourti/patient_monitor/blob/main/screenshots/get-device.png)

## Design of Chat Module

#### Message Table
- MessageID
- SessionID
- Sender
- Created_at
- Updated_at
- Message: { VoiceMessage: "", Media: "", Text: ""}
- Sender

#### Session Table
- SessionId
- Device_id
- Participants
- Created_at
- Updated_at

I will use a key-value document database because it provides better performance when there are multiple columns. Additionally a chat module will need to perform a lot of read/write operations so a document database seems a better option than SQL.

## Documentation
The code currently supports:
1) GET, PUT, DELETE a device: **{url}/devices/{device_id}**
2) GET all devices, POST a new device: **{url}/devices**
3) GET, PUT, DELETE a device type: **{url}/device_types/{device_type_id}**
4) GET all device types, POST a new device type: **{url}/device_types**
5) GET, PUT, DELETE a device assignment: **{url}/device_assignments/{device_assignment_id}**
6) GET all device assignments, POST a new device assignment: **{url}/device_assignments**
7) GET, PUT, DELETE a device measurement: **{url}/device_measurements/{device_measurement_id}**
8) GET all device measurements, POST a new device measurement: **{url}/device_measurements**
9) GET, PUT, DELETE a chat session: **{url}/sessions/{session_id}**
10) GET all chat sessions, POST a new chat session: **{url}/sessions**
11) GET, PUT, DELETE a chat message: **{url}/messages/{message_id}**
12) GET all chat messages, POST a new chat message: **{url}/messages**

Since there is no database at the moment, the recorded data are saved and updated to JSON files under the folder db/. The Device Module code can be found under device_module/. The chat_module can be found under chat_module/

### Examples
#### 1. Add a new device
```
from device import Device
import random
import string
import time
import json

device = Device()
chars = string.ascii_letters + string.digits
data = {"device_type_id": "0",
        "serial_number": ''.join([random.choice(chars) for _ in range(15)]),
        "sw_version": "T1.0",
        "mac_address": "00:00:5e:00:53:af",
        "purchased_on": time.time()}
json_data = json.dumps(data)

new_device_id = device.create_device(json_data)

```
#### 2. Assign a new device
```
from device_assignment import DeviceAssignment
import random
import string
import json

da = DeviceAssignment()
data = {
        "device_id": '0',
        "assigned_by": ''.join([random.choice(string.digits) for _ in range(3)]),
        "assignee": ''.join([random.choice(string.digits) for _ in range(3)])
       }
json_data = json.dumps(data)
new_assignment_id = da.assign_device(json_data)

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
from device_assignment import DeviceAssignment
from device_measurement import DeviceMeasurement
import json

d = Device()
devices = d.get_devices()
print('Available Devices')
print(json.dumps(devices, indent=4, sort_keys=True))

dt = DeviceType()
device_types = dt.get_device_types()
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

#### Patient Table
- UserId
- PatientHistory (Json)
- EmergencyContactId

#### Roles Table
- Id
- Type (Patient, Family, Nurse, Doctor, Staff, Admin, Other)

#### RoleAssignment Table
- UserId
- RoleId
- CreatedAt
- UpdatedAt

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
