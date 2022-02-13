import logging
import json
import os
import string
import time

device_assignments_db_file = os.path.join('db', 'device_assignments.json')
device_measurements_db_file = os.path.join('db', 'device_measurements.json')
devices_db_file = os.path.join('db', 'devices.json')
device_types_db_file = os.path.join('db', 'device_types.json')

class DeviceMeasurement:
    def __init__(self):
        self.logger = logging.getLogger('Device Measurement Logger')
        self.logger.setLevel(logging.DEBUG)
        
    def create_measurement_id(self):
        with open(device_measurements_db_file, 'r') as f:
            measurements = json.load(f)
        ids = measurements.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        measurement_id = max(ids) + 1
        return measurement_id

    def check_device_id(self, device_id):
        with open(devices_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if device_id not in ids:
            self.logger.error('Device id ' \
                        + str(device_id) + ' does not exist')
            raise ValueError('Device id ' \
                        + str(self.device_id) + ' does not exist')

    def check_device(self, device_id, device_type_id):
        with open(devices_db_file, 'r') as f:
            devices = json.load(f)
        ids = devices.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if device_id not in ids:
            self.logger.error('Device id '+str(device_id)+' does not exist')
            raise ValueError('Device id '+str(device_id)+' does not exist')
        device = devices[str(device_id)]
        if device_type_id != int(device['device_type_id']):
            self.logger.error('Wrong device type id sent')
            self.logger.error('Expected device type '+device['device_type_id'])
            self.logger.error(' but got ' + str(device_type_id))

            raise ValueError('Wrong device type id sent'+\
                            'Expected device type '+device['device_type_id']+\
                            ' but got '+ str(device_type_id))

    def check_assignment_id(self, device_id, assignment_id):
        with open(device_assignments_db_file, 'r') as f:
            assignments = json.load(f)
        ids = assignments.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if assignment_id not in ids:
            self.logger.error('Assignment id '+str(assignment_id)+' does not exist')
            raise ValueError('Assignment id '+str(assignment_id)+' does not exist')
        assignment = assignments[str(assignment_id)]
        if device_id != int(assignment['device_id']):
            self.logger.error('Wrong device id sent')
            self.logger.error('Expected device '+assignment['device_id'])
            self.logger.error(' but got ' + str(device_id))

            raise ValueError('Wrong device id sent'+\
                            'Expected device '+assignment['device_id']+\
                            ' but got '+ str(device_id))

    def record_measurement(self, data):
        self.logger.info('Parsing sent data')
        json_data = ''
        try:
            json_data = json.loads(data)
        except:
            self.logger.error('Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))
            raise ValueError('Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))

        required_data = ['device_type_id', 'device_id', 
                         'assignment_id', 'measurement', 'timestamp']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError("Missing required data %s", missing_data)
        
        device_type_id = json_data['device_type_id']
        device_id = json_data['device_id']
        assignment_id = json_data['assignment_id']
        timestamp = json_data['timestamp']
        device_data_sent = json_data['measurement']
        
        if not device_type_id.isdecimal():
            self.logger.error("Device type id %s is not an decimal number", device_type_id)
            raise ValueError("Device type id %s is not an decimal number", device_type_id)
        if not device_id.isdecimal():
            self.logger.error("Device id %s is not an decimal number", device_id)
            raise ValueError("Device id %s is not an decimal number", device_id)
        if not assignment_id.isdecimal():
            self.logger.error("Assignment id %s is not an decimal number", assignment_id)
            raise ValueError("Assignment id %s is not an decimal number", assignment_id)

        device_type_id = int(device_type_id)
        device_id = int(device_id)
        assignment_id = int(assignment_id)
        
        self.check_device_id(device_id)
        self.check_device(device_id, device_type_id)
        self.check_assignment_id(device_id, assignment_id)
        
        self.logger.info(str(assignment_id) + \
            ": Checking format of measurement data sent from device %s", \
            str(device_id))

        device_type = self.get_device_type(device_type_id)
        self.check_data(assignment_id, device_type, device_data_sent)
        self.logger.info('Creating a new measurement')
        created_at = time.time()
        new_measurement_id = self.create_measurement_id()
        with open(device_measurements_db_file, 'r') as f:
            measurements = json.load(f)
        measurements[str(new_measurement_id)] = {
            "device_id": str(device_id),
            "assignment_id": str(assignment_id),
            "measurement": {
                device_type: str(device_data_sent), 
                "timestamp": timestamp
            },
            "created_at": str(created_at)
        }
        with open(device_measurements_db_file, 'w') as f:
            data = json.dumps(measurements)
            f.write(data)
        self.logger.info(str(assignment_id) + \
            'Created a new measurement with measurement id ' + \
            str(new_measurement_id))

    def get_device_type(self, device_type_id):
        with open(device_types_db_file, 'r') as f:
            device_types = json.load(f)
        if str(device_type_id) not in device_types:
            self.logger.error('Device type id ' \
                        + str(device_type_id) + ' does not exist')
            raise ValueError('Device type id ' \
                        + str(device_type_id) + ' does not exist')
        device_type = device_types[str(device_type_id)]

        return device_type

    def check_temp_data(self, assignment_id, data):
        try:
            data = float(data)
        except ValueError:
            self.logger.error(str(assignment_id) + \
                ": Temperature sent %s is not a number", data)
            raise ValueError(str(assignment_id) + \
                ": Temperature sent %s is not a number", data)
            
        if data > 105 or data < 82:
            self.logger.error(str(assignment_id) + \
                ": Temperature data sent are outside of possible range "\
                    + '[82 Fahrenheit, 105 Fahrenheit]')
            raise ValueError(str(assignment_id) + \
                ": Temperature data sent are outside of possible range "\
                    + '[82 Fahrenheit, 105 Fahrenheit]')

    def check_oxygen_data(self, assignment_id, data):
        if not data.isdecimal():
            self.logger.error(str(assignment_id) + \
                ": Oxygen data sent %s is not an decimal number", data)
            raise ValueError(str(assignment_id) + \
                ": Oxygen data sent %s is not an decimal number", data)
        data = int(data)
        if data > 100 or data < 0:
            self.logger.error(str(assignment_id) + ': ' 
                    + 'Oxygen level in the blood ' \
                    + ' data sent are outside of possible range '\
                    + '[0, 100] (percentage of oxygen in the blood)')
            raise ValueError(str(assignment_id) + ': ' 
                    + 'Oxygen level in the blood ' \
                    + ' data sent are outside of possible range '\
                    + '[0, 100] (percentage of oxygen in the blood)')

    def check_systolic_pressure_data(self, assignment_id, data):
        if 'systolic' not in data:
            self.logger.error(str(self.assignment_id) + \
                ": Systolic pressure data not sent in %s", data)
            raise ValueError(str(self.assignment_id) + \
                ": Systolic pressure data not sent in %s", data)
        if not data['systolic'].isdecimal():
            self.logger.error(str(self.assignment_id) + \
                ": Systolic pressure data sent %s is not an decimal number", data)
            raise ValueError(str(self.assignment_id) + \
                ": Systolic pressure data sent %s is not an decimal number", data)
        systolic = int(data['systolic'])
        if systolic > 200 or systolic < 80:
            self.logger.error(str(assignment_id) + ': ' 
                    + 'Systolic blood pressure' \
                    + ' data sent are outside of possible range '\
                    + '[80mmHg, 200mmHg]')
            raise ValueError(str(assignment_id) + ': ' 
                    + 'Systolic blood pressure' \
                    + ' data sent are outside of possible range '\
                    + '[80mmHg, 200mmHg]')

    def check_diastolic_pressure_data(self, assignment_id, data):
        if 'diastolic' not in data:
            self.logger.error(str(self.assignment_id) + \
                ": Diastolic pressure data not sent in %s", data)
            raise ValueError(str(self.assignment_id) + \
                ": Diastolic pressure data not sent in %s", data)
        if not data['diastolic'].isdecimal():
            self.logger.error(str(self.assignment_id) + \
                ": Systolic pressure data sent %s is not an decimal number", data)
            raise ValueError(str(self.assignment_id) + \
                ": Systolic pressure data sent %s is not an decimal number", data)
        diastolic = int(data['diastolic'])
        if diastolic > 150 or diastolic < 30:
            self.logger.error(str(assignment_id) + ': ' 
                    + 'Diastolic blood pressure'\
                    + ' data sent are outside of possible range '\
                    + '[30mmHg, 150mmHg]')
            raise ValueError(str(assignment_id) + ': ' 
                    + 'Diastolic blood pressure'\
                    + ' data sent are outside of possible range '\
                    + '[30mmHg, 150mmHg]')

    def check_pulse_data(self, assignment_id, data):
        if not data.isdecimal():
            self.logger.error(str(self.assignment_id) + \
                ": Pulse data sent %s is not an decimal number", data)
            raise ValueError(str(self.assignment_id) + \
                ": Pulse data sent %s is not an decimal number", data)
        data = int(data)
        if data > 480 or data < 27:
            self.logger.error(str(assignment_id) + ': ' 
                    + 'Pulse ' \
                    + ' data sent are outside of possible range '\
                    + '[27bpm, 480bpm]')
            raise ValueError(str(assignment_id) + ': ' 
                    + 'Pulse ' \
                    + ' data sent are outside of possible range '\
                    + '[27bpm, 480bpm]')

    def check_weight_data(self, assignment_id, data):
        try:
            data = float(data)
        except ValueError:
            self.logger.error(str(assignment_id) + \
                ": Weight sent %s is not a number", data)
            raise ValueError(str(assignment_id) + \
                ": Weight sent %s is not a number", data)
        if data > 1400 or data < 2:
            self.logger.error(str(assignment_id) + ': ' 
                    + 'Weight ' \
                    + ' data sent are outside of possible range '\
                    + '[2lbs, 1400lbs]')
            raise ValueError(str(assignment_id) + ': ' 
                    + 'Weight ' \
                    + ' data sent are outside of possible range '\
                    + '[2lbs, 1400lbs]')

    def check_blood_glucose_data(self, assignment_id, data):
        if not data.isdecimal():
            self.logger.error(str(assignment_id) + \
                ": Blood glucose level sent %s is not an decimal number", data)
            raise ValueError(str(assignment_id) + \
                ": Blood glucose level sent %s is not an decimal number", data)
        data = int(data)
        if data > 147.6 or data < 10:
            self.logger.error(str(assignment_id) + ': ' 
                    + 'Blood glucose level ' \
                    + ' data sent are outside of possible range '\
                    + '[10mg/dL, 147mg/dL]')
            raise ValueError(str(assignment_id) + ': ' 
                    + 'Blood glucose level ' \
                    + ' data sent are outside of possible range '\
                    + '[10mg/dL, 147mg/dL]')
        
    def check_data(self, assignment_id, device_type, data):
        if device_type == 'temperature':
            self.check_temp_data(assignment_id, data)
        if device_type == 'oximeter':
            self.check_oxygen_data(assignment_id, data)
        if device_type == 'pulse':
            self.check_pulse_data(assignment_id, data)
        if device_type == 'glucometer':
            self.check_blood_glucose_data(assignment_id, data)
        if device_type == 'blood_pressure':
            self.check_systolic_pressure_data(assignment_id, data)
            self.check_diastolic_pressure_data(assignment_id, data)
        if device_type == 'weight':
            self.check_weight_data(assignment_id, data)

    def get_measurements(self):
        with open(device_measurements_db_file, 'r') as f:
            measurements = json.load(f)
        return measurements
