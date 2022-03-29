import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

import sys
sys.path.extend(['./device_module', './chat_module', './users_module', './auth_module'])

application = Flask(__name__)
api = Api(application)

from device import Device
from device_type import DeviceType
from device_assignment import DeviceAssignment
from device_measurement import DeviceMeasurement
from message import Message
from session import Session
from users import User
from user_roles import UserRole
from role_assignments import RoleAssignment
from patients import Patient
from auth import Authentication

device_module = Device()
device_type_module = DeviceType()
device_assignment_module = DeviceAssignment()
device_measurement_module = DeviceMeasurement()
session_module = Session()
message_module = Message()
users_module = User()
user_roles_module = UserRole()
role_assignment_module = RoleAssignment()
patient_module = Patient()
auth_module = Authentication()

device_args = reqparse.RequestParser()

def error(e, **kwargs):
    if e.args[0] == 1:
        abort(400,
            message="Device id {} is not a string containing a decimal number".format(kwargs['device_id']))
    if e.args[0] == 2:
        abort(404, message="Device id {} does not exist".format(kwargs['device_id']))
    if e.args[0] == 3:
        abort(400,
          message="Device type id {} is not a string containing a decimal number".format(
                                                                            kwargs['device_type_id']))
    if e.args[0] == 4:
        abort(404, message="Device type id {} does not exist".format(kwargs['device_type_id']))
    if e.args[0] == 5:
        abort(400, message="MAC Address doesn't consist of 6 octets".format(kwargs['mac_address']))
    if e.args[0] == 6:
        abort(400,
            message="MAC Address doesn't consist of two-digit hex groups".format(kwargs['mac_address']))
    if e.args[0] == 7:
        abort(400, message="MAC Address doesn't consist of hex numbers".format(kwargs['mac_address']))
    if e.args[0] == 8:
        abort(400,
         message="Serial number doesn't contain only digits or ascii letters".format(kwargs['serial_number']))
    if e.args[0] == 9:
        abort(400, message="Software version doesn't contain only digits, "\
                    "ascii letters and/or a dot".format(kwargs['serial_number']))
    if e.args[0] == 10:
        abort(400, message="Data sent are not in json format")
    if e.args[0] == 11:
        abort(400, message=e.args[1])
    if e.args[0] == 12:
        abort(404, message="Device type {} already exists".format(kwargs['device_type']))
    if e.args[0] == 13:
        abort(400, message="Assignment id {} is not " +\
            "a string containing a decimal number".format(kwargs['assignment_id']))
    if e.args[0] == 14:
        abort(404, message="Assignment id {} does not exist".format(kwargs['assignment_id']))
    if e.args[0] == 15:
        abort(404, message="Wrong device id sent")
    if e.args[0] == 16:
        abort(404, message="Wrong device type id sent")
    if e.args[0] == 17:
        abort(400, message="Measurement id {} is not " +\
            "a string containing a decimal number".format(kwargs['measurement_id']))
    if e.args[0] == 18:
        abort(404, message="Measurement id {} does not exist".format(kwargs['measurement_id']))
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
    if e.args[0] == 35:
        abort(400,
            message="Session id {} is not a string containing a decimal number".format(kwargs['session_id']))
    if e.args[0] == 36:
        abort(404, message="Session id {} does not exist".format(kwargs['session_id']))
    if e.args[0] == 37:
        abort(400,
            message="Message id {} is not a string containing a decimal number".format(kwargs['message_id']))
    if e.args[0] == 38:
        abort(404, message="Message id {} does not exist".format(kwargs['message_id']))
    if e.args[0] == 39:
        abort(400,
            message="User id {} is not a string containing a decimal number".format(kwargs['user_id']))
    if e.args[0] == 40:
        abort(404, message="User id {} does not exist".format(kwargs['user_id']))
    if e.args[0] == 41:
        abort(400,
            message="User role id {} is not a string containing " \
                    "a decimal number".format(kwargs['user_role_id']))
    if e.args[0] == 42:
        abort(404, message="User role id {} does not exist".format(kwargs['user_role_id']))
    if e.args[0] == 43:
        abort(400,
            message="Role assignment id {} is not a string containing " \
                    "a decimal number".format(kwargs['role_assignment_id']))
    if e.args[0] == 44:
        abort(404, message="Role assignment id {} does not exist".format(kwargs['role_assignment_id']))
    if e.args[0] == 45:
        abort(400,
            message="Patient id {} is not a string containing a decimal number".format(kwargs['patient_id']))
    if e.args[0] == 46:
        abort(404, message="Patient id {} does not exist".format(kwargs['patient_id']))
    if e.args[0] == 47:
        abort(400,
            message="Emergency contact id {} is not a string containing " \
                    "a decimal number".format(kwargs['emergency_contact_id']))
    if e.args[0] == 48:
        abort(404, message="Emergency contact id {} does not exist".format(kwargs['emergency_contact_id']))
    if e.args[0] == 49:
        abort(404, message="User role {} already exists".format(kwargs['user_role']))

class Device(Resource):
    def get(self, device_id):
        json_data = json.dumps({"device_id": device_id})
        try:
            response = device_module.get_device(json_data)
        except ValueError as e:
            error(e, device_id=device_id)
        response['device_id'] = device_id
        return response

    def delete(self, device_id):
        json_data = json.dumps({"device_id": str(device_id)})
        try:
            response = device_module.delete_device(json_data)
        except ValueError as e:
            error(e, device_id=device_id)
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
            error(e, device_id=device_id, device_type_id=device_type_id,
                    serial_number=serial_number, mac_address=mac_address)
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
            error(e, device_id=device_id, device_type_id=device_type_id,
                    serial_number=serial_number, mac_address=mac_address)
        return {"device_id": device_id}

class DeviceType(Resource):
    def get(self, device_type_id):
        json_data = json.dumps({"device_type_id": str(device_type_id)})
        try:
            response = device_type_module.get_device_type(json_data)
        except ValueError as e:
            error(e, device_type_id=device_type_id)
        response['device_type_id'] = device_type_id
        return response

    def delete(self, device_type_id):
        json_data = json.dumps({"device_type_id": str(device_type_id)})
        try:
            response = device_type_module.delete_device_type(json_data)
        except ValueError as e:
            error(e, device_type_id=device_type_id)
        return response

    def put(self, device_type_id):
        json_data = {"device_type_id": str(device_type_id)}
        device_type = request.form['device_type']
        json_data['device_type'] = device_type
        json_data = json.dumps(json_data)
        try:
            response = device_type_module.update_device_type(json_data)
        except ValueError as e:
            error(e, device_type_id=device_type_id, device_type=device_type)
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
            error(e, device_type=device_type)
        return {"device_type_id": device_type_id}

class DeviceAssignment(Resource):
    def get(self, assignment_id):
        json_data = json.dumps({"assignment_id": str(assignment_id)})
        try:
            response = device_assignment_module.get_assignment(json_data)
        except ValueError as e:
            error(e, assignment_id=assignment_id)
        response['assignment_id'] = assignment_id
        return response

    def delete(self, assignment_id):
        json_data = json.dumps({"assignment_id": str(assignment_id)})
        try:
            response = device_assignment_module.delete_assignment(json_data)
        except ValueError as e:
            error(e, assignment_id=assignment_id)
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
            error(e, assignment_id=assignment_id, device_id=device_id)
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
            error(e, assignment_id=assignment_id, device_id=device_id)
        return {"assignment_id": assignment_id}

class DeviceMeasurement(Resource):
    def get(self, measurement_id):
        json_data = json.dumps({"measurement_id": str(measurement_id)})
        try:
            response = device_measurement_module.get_measurement(json_data)
        except ValueError as e:
            error(e, measurement_id=measurement_id)
        response['measurement_id'] = measurement_id
        return response

    def delete(self, measurement_id):
        json_data = json.dumps({"measurement_id": str(measurement_id)})
        try:
            response = device_measurement_module.delete_measurement(json_data)
        except ValueError as e:
            error(e, measurement_id=measurement_id)
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
            error(e, measurement_id=measurement_id, assignment_id=assignment_id,
                     device_type_id=device_type_id, device_id=device_id)
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
            error(e, measurement_id=measurement_id, assignment_id=assignment_id,
                     device_type_id=device_type_id, device_id=device_id)
        return {"measurement_id": measurement_id}

class Session(Resource):
    def get(self, session_id):
        json_data = json.dumps({"session_id": session_id})
        try:
            response = session_module.get_session(json_data)
        except ValueError as e:
            error(e, session_id=session_id)
        response['session_id'] = session_id
        return response

    def delete(self, session_id):
        json_data = json.dumps({"session_id": str(session_id)})
        try:
            response = session_module.delete_session(json_data)
        except ValueError as e:
            error(e, session_id=session_id)
        return response

    def put(self, session_id):
        json_data = {"session_id": str(session_id)}
        device_id = request.json['device_id']
        participants = request.json['participants']
        json_data['device_id'] = device_id
        json_data['participants'] = participants
        json_data = json.dumps(json_data)

        try:
            response = session_module.update_session(json_data)
        except ValueError as e:
            error(e, session_id=session_id, device_id=device_id)
        return response
           
class SessionList(Resource):
    def get(self):
        return session_module.get_sessions()

    def post(self):
        device_id = request.json['device_id']
        participants = request.json['participants']
        json_data = {}
        json_data['device_id'] = device_id
        json_data['participants'] = participants
        json_data = json.dumps(json_data)
        try:
            session_id = session_module.create_session(json_data)
        except ValueError as e:
            error(e, device_id=device_id)
        return {"session_id": session_id}

class Message(Resource):
    def get(self, message_id):
        json_data = json.dumps({"message_id": message_id})
        try:
            response = message_module.get_message(json_data)
        except ValueError as e:
            error(e, message_id=message_id)
        response["message_id"] = message_id
        return response

    def delete(self, message_id):
        json_data = json.dumps({"message_id": str(message_id)})
        try:
            response = message_module.delete_message(json_data)
        except ValueError as e:
            error(e, message_id=message_id)
        return response

    def put(self, message_id):
        json_data = {"message_id": str(message_id)}
        session_id = request.json['session_id']
        message = request.json['message']
        sender = request.json['sender']
        json_data['session_id'] = session_id
        json_data['message'] = message
        json_data['sender'] = sender
        json_data = json.dumps(json_data)

        try:
            response = message_module.update_message(json_data)
        except ValueError as e:
            error(e, session_id=session_id, message_id=message_id, message=message)
        return response
           
class MessageList(Resource):
    def get(self):
        return message_module.get_messages()

    def post(self):
        session_id = request.json['session_id']
        message = request.json['message']
        sender = request.json['sender']
        json_data = {}
        json_data['session_id'] = session_id
        json_data['message'] = message
        json_data['sender'] = sender
        json_data = json.dumps(json_data)
        try:
            print('inside try')
            message_id = message_module.create_message(json_data)
        except ValueError as e:
            error(e, session_id=session_id, message=message)
        return {"message_id": message_id}

class User(Resource):
    def get(self, user_id):
        json_data = json.dumps({"user_id": user_id})
        try:
            response = users_module.get_user(json_data)
        except ValueError as e:
            error(e, user_id=user_id)
        response['user_id'] = user_id
        return response

    def delete(self, user_id):
        json_data = json.dumps({"user_id": str(user_id)})
        try:
            response = users_module.delete_user(json_data)
        except ValueError as e:
            error(e, user_id=user_id)
        return response

    def put(self, user_id):
        json_data = {"user_id": str(user_id)}

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
        state = request.form['state']
        zipcode = request.form['zipcode']
        phone_number = request.form['phone_number']
        email = request.form['email']
        json_data['first_name'] = first_name
        json_data['last_name'] = last_name
        json_data['date_of_birth'] = date_of_birth
        json_data['address'] = address
        json_data['state'] = state
        json_data['zipcode'] = zipcode
        json_data['phone_number'] = phone_number
        json_data['email'] = email
        json_data = json.dumps(json_data)
        try:
            response = users_module.update_user(json_data)
        except ValueError as e:
            error(e, user_id=user_id)
        return response
           
class UserList(Resource):
    def get(self):
        return users_module.get_users()

    def post(self):
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        date_of_birth = request.json['date_of_birth']
        address = request.json['address']
        state = request.json['state']
        zipcode = request.json['zipcode']
        phone_number = request.json['phone_number']
        email = request.json['email']
        json_data = {}
        json_data['first_name'] = first_name
        json_data['last_name'] = last_name
        json_data['date_of_birth'] = date_of_birth
        json_data['address'] = address
        json_data['state'] = state
        json_data['zipcode'] = zipcode
        json_data['phone_number'] = phone_number
        json_data['email'] = email
        json_data = json.dumps(json_data)
        try:
            user_id = users_module.create_user(json_data)
        except ValueError as e:
            error(e)
            print(e)
        return {"user_id": user_id}

class UserRole(Resource):
    def get(self, user_role_id):
        json_data = json.dumps({"user_role_id": user_role_id})
        try:
            response = user_roles_module.get_user_role(json_data)
        except ValueError as e:
            error(e, user_role_id=user_role_id)
        response['user_role_id'] = user_role_id
        return response

    def delete(self, user_role_id):
        json_data = json.dumps({"user_role_id": str(user_role_id)})
        try:
            response = user_roles_module.delete_user_role(json_data)
        except ValueError as e:
            error(e, user_role_id=user_role_id)
        return response

    def put(self, user_role_id):
        json_data = {"user_role_id": str(user_role_id)}

        user_role = request.form['user_role']
        json_data['user_role'] = user_role
        json_data = json.dumps(json_data)
        try:
            response = user_roles_module.update_user_role(json_data)
        except ValueError as e:
            error(e, user_role_id=user_role_id, user_role=user_role)
        return response

class UserRoleList(Resource):
    def get(self):
        return user_roles_module.get_user_roles()

    def post(self):
        user_role = request.form['user_role']
        json_data = {}
        json_data['user_role'] = user_role
        json_data = json.dumps(json_data)
        try:
            user_role_id = user_roles_module.create_user_role(json_data)
        except ValueError as e:
            error(e, user_role=user_role)
        return {"user_role_id": user_role_id}

class UserRoleAssignment(Resource):
    def get(self, role_assignment_id):
        json_data = json.dumps({"role_assignment_id": role_assignment_id})
        try:
            response = role_assignment_module.get_role_assignment(json_data)
        except ValueError as e:
            error(e, role_assignment_id=role_assignment_id)
        response['role_assignment_id'] = role_assignment_id
        return response

    def delete(self, role_assignment_id):
        json_data = json.dumps({"role_assignment_id": str(role_assignment_id)})
        try:
            response = role_assignment_module.delete_role_assignment(json_data)
        except ValueError as e:
            error(e, role_assignment_id=role_assignment_id)
        return response

    def put(self, role_assignment_id):
        json_data = {"role_assignment_id": str(role_assignment_id)}

        user_role_id = request.form['user_role_id']
        user_id = request.form['user_id']
        json_data['user_role_id'] = user_role_id
        json_data['user_id'] = user_id
        json_data = json.dumps(json_data)
        try:
            response = role_assignment_module.update_role_assignment(json_data)
        except ValueError as e:
            error(e, role_assignment_id=role_assignment_id, user_id=user_id, user_role_id=user_role_id)
        return response

class UserRoleAssignmentList(Resource):
    def get(self):
        return role_assignment_module.get_role_assignments()

    def post(self):
        user_role_id = request.form['user_role_id']
        user_id = request.form['user_id']
        json_data = {}
        json_data['user_role_id'] = user_role_id
        json_data['user_id'] = user_id
        json_data = json.dumps(json_data)
        try:
            role_assignment_id = role_assignment_module.assign_role(json_data)
        except ValueError as e:
            error(e, user_id=user_id, user_role_id=user_role_id)
            print(e)
        return {"role_assignment_id": role_assignment_id}

class Patient(Resource):
    def get(self, patient_id):
        json_data = json.dumps({"patient_id": patient_id})
        try:
            response = patient_module.get_patient(json_data)
        except ValueError as e:
            error(e, patient_id=patient_id)
        response['patient_id'] = patient_id
        return response

    def delete(self, patient_id):
        json_data = json.dumps({"patient_id": str(patient_id)})
        try:
            response = patient_module.delete_patient(json_data)
        except ValueError as e:
            error(e, patient_id=patient_id)
        return response

    def put(self, patient_id):
        json_data = {"patient_id": str(patient_id)}

        emergency_contact_id = request.json['emergency_contact_id']
        user_id = request.json['user_id']
        patient_history = request.json['patient_history']
        json_data['emergency_contact_id'] = emergency_contact_id
        json_data['user_id'] = user_id
        json_data['patient_history'] = patient_history
        json_data = json.dumps(json_data)
        try:
            response = patient_module.update_patient(json_data)
        except ValueError as e:
            error(e, patient_id=patient_id, user_id=user_id, emergency_contact_id=emergency_contact_id)
        return response
           
class PatientList(Resource):
    def get(self):
        return patient_module.get_patients()

    def post(self):
        emergency_contact_id = request.json['emergency_contact_id']
        user_id = request.json['user_id']
        patient_history = request.json['patient_history']
        json_data = {}
        json_data['emergency_contact_id'] = emergency_contact_id
        json_data['user_id'] = user_id
        json_data['patient_history'] = patient_history
        json_data = json.dumps(json_data)
        try:
            patient_id = patient_module.create_patient(json_data)
        except ValueError as e:
            error(e, patient_id=patient_id, user_id=user_id, emergency_contact_id=emergency_contact_id)
        return {"patient_id": patient_id}

class Authentication(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']

        json_data = {}
        json_data['email'] = email
        json_data['password'] = password
        json_data = json.dumps(json_data)

        return auth_module.authenticate(json_data)

api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<string:device_id>')
api.add_resource(DeviceTypeList, '/device_types')
api.add_resource(DeviceType, '/device_types/<string:device_type_id>')
api.add_resource(DeviceAssignmentList, '/device_assignments')
api.add_resource(DeviceAssignment, '/device_assignments/<string:assignment_id>')
api.add_resource(DeviceMeasurementList, '/device_measurements')
api.add_resource(DeviceMeasurement, '/device_measurements/<string:measurement_id>')
api.add_resource(SessionList, '/sessions')
api.add_resource(Session, '/sessions/<string:session_id>')
api.add_resource(MessageList, '/messages')
api.add_resource(Message, '/messages/<string:message_id>')
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<string:user_id>')
api.add_resource(UserRoleList, '/user_roles')
api.add_resource(UserRole, '/user_roles/<string:user_role_id>')
api.add_resource(UserRoleAssignmentList, '/user_role_assignments')
api.add_resource(UserRoleAssignment, '/user_role_assignments/<string:role_assignment_id>')
api.add_resource(PatientList, '/patients')
api.add_resource(Patient, '/patients/<string:patient_id>')
api.add_resource(Authentication, '/auth')

@application.route('/')
def index():
    return "<h1>Patient Monitor App!</h1>"
