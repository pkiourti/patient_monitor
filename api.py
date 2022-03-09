import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

import sys
sys.path.append('./device_module')

application = Flask(__name__)
api = Api(application)

from device import Device
from device_type import DeviceType
from device_assignment import DeviceAssignment
from device_measurement import DeviceMeasurement

device_module = Device()
device_type_module = DeviceType()
device_assignment_module = DeviceAssignment()
device_measurement_module = DeviceMeasurement()

device_args = reqparse.RequestParser()

def error(e):
    if e.args[0] == 1:
        abort(400,
            message="Device id {} is not a string containing a decimal number".format(device_id))
    if e.args[0] == 2:
        abort(404, message="Device id {} does not exist".format(device_id))
    if e.args[0] == 3:
        abort(400,
           message="Device type id {} is not a string containing a decimal number".format(device_id))
    if e.args[0] == 4:
        abort(404, message="Device type id {} does not exist".format(device_id))
    if e.args[0] == 5:
        abort(400, message="MAC Address doesn't consist of 6 octets".format(mac_address))
    if e.args[0] == 6:
        abort(400, message="MAC Address doesn't consist of two-digit hex groups".format(mac_address))
    if e.args[0] == 7:
        abort(400, message="MAC Address doesn't consist of hex numbers".format(mac_address))
    if e.args[0] == 8:
        abort(400,
          message="Serial number doesn't contain only digits or ascii letters".format(serial_number))
    if e.args[0] == 9:
        abort(400, message="Software version doesn't contain only digits, "\
                    "ascii letters and/or a dot".format(serial_number))
    if e.args[0] == 10:
        abort(400, message="Data sent are not in json format")
    if e.args[0] == 11:
        abort(400, message=e.args[1])
    if e.args[0] == 12:
        abort(404, message="Device type {} already exists".format(device_type))
    if e.args[0] == 13:
        abort(400, message="Assignment id {} is not " +\
            "a string containing a decimal number".format(assignment_id))
    if e.args[0] == 14:
        abort(404, message="Assignment id {} does not exist".format(assignment_id))
    if e.args[0] == 15:
        abort(404, message="Wrong device id sent")
    if e.args[0] == 16:
        abort(404, message="Wrong device type id sent")
    if e.args[0] == 17:
        abort(400, message="Measurement id {} is not " +\
            "a string containing a decimal number".format(measurement_id))
    if e.args[0] == 18:
        abort(404, message="Measurement id {} does not exist".format(measurement_id))
    if e.args[0] == 19:
        abort(400, message="Temperature sent is not a number")
    if e.args[0] == 20:
        abort(404, message="Temperature is outside of possible range "\
                    + '[82 Fahrenheit, 105 Fahrenheit]')
    if e.args[0] == 21:
        abort(404, message="Oxygen level sent is not a number")
    if e.args[0] == 22:
        abort(404, message="Oxygen level in the blood " \
                    + " data sent are outside of possible range "\
                    + "[0, 100] (percentage of oxygen in the blood)")
    if e.args[0] == 23:
        abort(404, message="Systolic pressure data are not sent")
    if e.args[0] == 24:
        abort(404, message="Systolic pressure sent is not a number")
    if e.args[0] == 25:
        abort(404, message="Systolic blood pressure" \
                    + " data sent are outside of possible range "\
                    + "[80mmHg, 200mmHg]")
    if e.args[0] == 26:
        abort(404, message="Diastolic pressure data are not sent")
    if e.args[0] == 27:
        abort(404, message="Diastolic pressure sent is not a number")
    if e.args[0] == 28:
        abort(404, message="Diastolic blood pressure"\
                    + " data sent are outside of possible range "\
                    + "[30mmHg, 150mmHg]")
    if e.args[0] == 29:
        abort(404, message="Pulse sent is not a number")
    if e.args[0] == 30:
        abort(404, message="Pulse " \
                    + " data sent are outside of possible range "\
                    + "[27bpm, 480bpm]")
    if e.args[0] == 31:
        abort(404, message="Weight sent is not a number")
    if e.args[0] == 32:
        abort(404, message="Weight " \
                    + " data sent are outside of possible range "\
                    + "[2lbs, 1400lbs]")
    if e.args[0] == 33:
        abort(404, message="Blood glucose level sent is not a number")
    if e.args[0] == 34:
        abort(404, message="Blood glucose level " \
                    + " data sent are outside of possible range "\
                    + "[10mg/dL, 147mg/dL]")
    

class Device(Resource):
    def get(self, device_id):
        json_data = json.dumps({"device_id": device_id})
        try:
            response = device_module.get_device(json_data)
        except ValueError as e:
            error(e)
        response['device_id'] = device_id
        return response

    def delete(self, device_id):
        json_data = json.dumps({"device_id": str(device_id)})
        try:
            response = device_module.delete_device(json_data)
        except ValueError as e:
            error(e)
        return response

    def put(self, device_id):
        json_data = {"device_id": str(device_id)}
        device_type_id = request.form['device_type_id']
        serial_number = request.form['serial_number']
        sw_version = request.form['sw_version']
        mac_address = request.form['mac_address']
        purchased_on = request.form['purchased_on']
        json_data['device_type_id'] = device_type_id
        json_data['serial_number'] = serial_number
        json_data['sw_version'] = sw_version
        json_data['mac_address'] = mac_address
        json_data['purchased_on'] = purchased_on
        json_data = json.dumps(json_data)

        try:
            response = device_module.update_device(json_data)
        except ValueError as e:
            error(e)
        return response
           
class DeviceList(Resource):
    def get(self):
        return device_module.get_devices()

    def post(self):
        device_type_id = request.form['device_type_id']
        serial_number = request.form['serial_number']
        sw_version = request.form['sw_version']
        mac_address = request.form['mac_address']
        purchased_on = request.form['purchased_on']
        json_data = {}
        json_data['device_type_id'] = device_type_id
        json_data['serial_number'] = serial_number
        json_data['sw_version'] = sw_version
        json_data['mac_address'] = mac_address
        json_data['purchased_on'] = purchased_on
        json_data = json.dumps(json_data)
        try:
            device_id = device_module.create_device(json_data)
        except ValueError as e:
            error(e)
        return {"device_id": device_id}

class DeviceType(Resource):
    def get(self, device_type_id):
        json_data = json.dumps({"device_type_id": str(device_type_id)})
        try:
            response = device_type_module.get_device_type(json_data)
        except ValueError as e:
            error(e)
        response['device_type_id'] = device_type_id
        return response

    def delete(self, device_type_id):
        json_data = json.dumps({"device_type_id": str(device_type_id)})
        try:
            response = device_type_module.delete_device_type(json_data)
        except ValueError as e:
            error(e)
        return response

    def put(self, device_type_id):
        json_data = {"device_type_id": str(device_type_id)}
        device_type = request.form['device_type']
        json_data['device_type'] = device_type
        json_data = json.dumps(json_data)
        try:
            response = device_type_module.update_device_type(json_data)
        except ValueError as e:
            error(e)
        return response

class DeviceTypeList(Resource):
    def get(self):
        return device_type_module.get_device_types()

    def post(self):
        device_type = request.form['device_type']
        json_data = {}
        json_data['device_type'] = device_type
        json_data = json.dumps(json_data)
        try:
            device_type_id = device_type_module.create_device_type(json_data)
        except ValueError as e:
            error(e)
        return {"device_type_id": device_type_id}

class DeviceAssignment(Resource):
    def get(self, assignment_id):
        json_data = json.dumps({"assignment_id": str(assignment_id)})
        try:
            response = device_assignment_module.get_assignment(json_data)
        except ValueError as e:
            error(e)
        response['assignment_id'] = assignment_id
        return response

    def delete(self, assignment_id):
        json_data = json.dumps({"assignment_id": str(assignment_id)})
        try:
            response = device_assignment_module.delete_assignment(json_data)
        except ValueError as e:
            error(e)
        return response

    def put(self, assignment_id):
        json_data = {"assignment_id": str(assignment_id)}
        device_id = request.form['device_id']
        assigned_by = request.form['assigned_by']
        assignee = request.form['assignee']
        json_data['device_id'] = device_id
        json_data['assigned_by'] = assigned_by
        json_data['assignee'] = assignee
        json_data = json.dumps(json_data)
        try:
            response = device_assignment_module.update_assignment(json_data)
        except ValueError as e:
            error(e)
        return response

class DeviceAssignmentList(Resource):
    def get(self):
        return device_assignment_module.get_assignments()

    def post(self):
        device_id = request.form['device_id']
        assigned_by = request.form['assigned_by']
        assignee = request.form['assignee']
        json_data = {}
        json_data['device_id'] = device_id
        json_data['assigned_by'] = assigned_by
        json_data['assignee'] = assignee
        json_data = json.dumps(json_data)
        try:
            assignment_id = device_assignment_module.assign_device(json_data)
        except ValueError as e:
            error(e)
        return {"assignment_id": assignment_id}

class DeviceMeasurement(Resource):
    def get(self, measurement_id):
        json_data = json.dumps({"measurement_id": str(measurement_id)})
        try:
            response = device_measurement_module.get_measurement(json_data)
        except ValueError as e:
            error(e)
        response['measurement_id'] = measurement_id
        return response

    def delete(self, measurement_id):
        json_data = json.dumps({"measurement_id": str(measurement_id)})
        try:
            response = device_measurement_module.delete_measurement(json_data)
        except ValueError as e:
            error(e)
        return response

    def put(self, measurement_id):
        json_data = {"measurement_id": str(measurement_id)}
        device_type_id = request.form['device_type_id']
        device_id = request.form['device_id']
        assignment_id = request.form['assignment_id']
        measurement = request.form['measurement']
        timestamp = request.form['timestamp']
        json_data['device_type_id'] = device_type_id
        json_data['device_id'] = device_id
        json_data['assignment_id'] = assignment_id
        json_data['measurement'] = measurement
        json_data['timestamp'] = timestamp
        json_data = json.dumps(json_data)
        try:
            response = device_measurement_module.update_measurement(json_data)
        except ValueError as e:
            error(e)
        return response

class DeviceMeasurementList(Resource):
    def get(self):
        return device_measurement_module.get_measurements()

    def post(self):
        device_type_id = request.form['device_type_id']
        device_id = request.form['device_id']
        assignment_id = request.form['assignment_id']
        measurement = request.form['measurement']
        timestamp = request.form['timestamp']
        json_data = {}
        json_data['device_type_id'] = device_type_id
        json_data['device_id'] = device_id
        json_data['assignment_id'] = assignment_id
        json_data['measurement'] = measurement
        json_data['timestamp'] = timestamp
        json_data = json.dumps(json_data)
        try:
            measurement_id = device_measurement_module.record_measurement(json_data)
        except ValueError as e:
            error(e)
        return {"measurement_id": measurement_id}


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<string:device_id>')
api.add_resource(DeviceTypeList, '/device_types')
api.add_resource(DeviceType, '/device_types/<string:device_type_id>')
api.add_resource(DeviceAssignmentList, '/device_assignments')
api.add_resource(DeviceAssignment, '/device_assignments/<string:assignment_id>')
api.add_resource(DeviceMeasurementList, '/device_measurements')
api.add_resource(DeviceMeasurement, '/device_measurements/<string:measurement_id>')

@application.route('/')
def index():
    return "<h1>Patient Monitor App!</h1>"
