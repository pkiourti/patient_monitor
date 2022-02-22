import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

from device import Device
from device_type import DeviceType
from device_assignment import DeviceAssignment
from device_measurement import DeviceMeasurement

device_module = Device()
device_type_module = DeviceType()
device_assignment_module = DeviceAssignment()
device_measurement_module = DeviceMeasurement()

device_args = reqparse.RequestParser()

class Device(Resource):
    def get(self, device_id):
        json_data = json.dumps({"device_id": str(device_id)})
        response = device_module.get_device(json_data)
        response['device_id'] = device_id
        return response

    def delete(self, device_id):
        json_data = json.dumps({"device_id": str(device_id)})
        return device_module.delete_device(json_data)

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
        return device_module.update_device(json_data)

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
        device_id = device_module.create_device(json_data)
        return {"device_id": device_id}

class DeviceType(Resource):
    def get(self, device_type_id):
        json_data = json.dumps({"device_type_id": str(device_type_id)})
        response = device_type_module.get_device_type(json_data)
        response['device_type_id'] = device_type_id
        return response

    def delete(self, device_type_id):
        json_data = json.dumps({"device_type_id": str(device_type_id)})
        return device_type_module.delete_device_type(json_data)

    def put(self, device_type_id):
        json_data = {"device_type_id": str(device_type_id)}
        device_type = request.form['device_type']
        json_data['device_type'] = device_type
        json_data = json.dumps(json_data)
        return device_type_module.update_device_type(json_data)

class DeviceTypeList(Resource):
    def get(self):
        return device_type_module.get_device_types()

    def post(self):
        device_type = request.form['device_type']
        json_data = {}
        json_data['device_type'] = device_type
        json_data = json.dumps(json_data)
        device_type_id = device_type_module.create_device_type(json_data)
        return {"device_type_id": device_type_id}

class DeviceAssignment(Resource):
    def get(self, assignment_id):
        json_data = json.dumps({"assignment_id": str(assignment_id)})
        response = device_assignment_module.get_assignment(json_data)
        response['assignment_id'] = assignment_id
        return response

    def delete(self, assignment_id):
        json_data = json.dumps({"assignment_id": str(assignment_id)})
        return device_assignment_module.delete_assignment(json_data)

    def put(self, assignment_id):
        json_data = {"assignment_id": str(assignment_id)}
        device_id = request.form['device_id']
        assigned_by = request.form['assigned_by']
        assignee = request.form['assignee']
        json_data['device_id'] = device_id
        json_data['assigned_by'] = assigned_by
        json_data['assignee'] = assignee
        json_data = json.dumps(json_data)
        return device_assignment_module.update_assignment(json_data)

class DeviceAssignmentList(Resource):
    def get(self):
        return device_assignment_module.get_devices()

    def post(self):
        device_id = request.form['device_id']
        assigned_by = request.form['assigned_by']
        assignee = request.form['assignee']
        json_data = {}
        json_data['device_id'] = device_id
        json_data['assigned_by'] = assigned_by
        json_data['assignee'] = assignee
        json_data = json.dumps(json_data)
        assignment_id = device_assignment_module.assign_device(json_data)
        return {"assignment_id": assignment_id}

class DeviceMeasurement(Resource):
    def get(self, measurement_id):
        json_data = json.dumps({"measurement_id": str(measurement_id)})
        response = device_measurement_module.get_measurement(json_data)
        response['measurement_id'] = measurement_id
        return response

    def delete(self, measurement_id):
        json_data = json.dumps({"measurement_id": str(measurement_id)})
        return device_measurement_module.delete_measurement(json_data)

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
        return device_measurement_module.update_measurement(json_data)

class DeviceMeasurementList(Resource):
    def get(self):
        return device_measurement_module.get_measurements()

    def post(self):
        required_data = ['device_type_id', 'device_id',
                         'assignment_id', 'measurement', 'timestamp']
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
        measurement_id = device_measurement_module.record_measurement(json_data)
        return {"measurement_id": measurement_id}


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<string:device_id>')
api.add_resource(DeviceTypeList, '/device_types')
api.add_resource(DeviceType, '/device_types/<string:device_type_id>')
api.add_resource(DeviceAssignmentList, '/device_assignments')
api.add_resource(DeviceAssignment, '/device_assignments/<string:assignment_id>')
api.add_resource(DeviceMeasurementList, '/device_measurements')
api.add_resource(DeviceMeasurement, '/device_measurements/<string:measurement_id>')

if __name__ == '__main__':
    app.run(debug=True) # not for production
