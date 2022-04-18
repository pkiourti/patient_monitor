# Use code from https://tinyurl.com/mvj637j6
# to check if a string is hexadecimal

import time
import logging
import json
import os
from itertools import compress
from bson.objectid import ObjectId
from pymongo import MongoClient

patients_db_file = os.path.join('db', 'patients.json')
users_db_file = os.path.join('db', 'users.json')

class Patient:
    """
    Class that creates a new patient record
    """
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('Patient Logger')
        self.logger.setLevel(logging.DEBUG)

    def _check_patient_id(self, patient_id):
        with open(patients_db_file, 'r') as f:
            patients = json.load(f)
        ids = patients.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not patient_id.isdecimal():
            self.logger.error("Patient id %s " + \
                        "is not an decimal number", patient_id)
            raise ValueError(45, "Patient id %s " + \
                        "is not an decimal number", patient_id)
        if int(patient_id) not in ids:
            self.logger.error('Patient id ' \
                        + patient_id + ' does not exist')
            raise ValueError(46, 'Patient id ' \
                        + patient_id + ' does not exist')

    def _check_user_id(self, user_id):
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        ids = users.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not user_id.isdecimal():
            self.logger.error("User id %s " + \
                        "is not an decimal number", user_id)
            raise ValueError(39, "User id %s " + \
                        "is not an decimal number", user_id)
        if int(user_id) not in ids:
            self.logger.error('User id ' \
                        + user_id + ' does not exist')
            raise ValueError(40, 'User id ' \
                        + user_id + ' does not exist')

    def _check_emergency_contact_id(self, emergency_contact_id):
        with open(users_db_file, 'r') as f:
            users = json.load(f)
        ids = users.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not emergency_contact_id.isdecimal():
            self.logger.error("User id %s " + \
                        "is not an decimal number", emergency_contact_id)
            raise ValueError(47, "User id %s " + \
                        "is not an decimal number", emergency_contact_id)
        if int(emergency_contact_id) not in ids:
            self.logger.error('User id ' \
                        + emergency_contact_id + ' does not exist')
            raise ValueError(48, 'User id ' \
                        + emergency_contact_id + ' does not exist')

    def _check_json(self, data):
        self.logger.info('Parsing sent data')
        try:
            json.loads(data)
        except:
            self.logger.error('Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))
            raise ValueError(10, 'Expected json data in a str ' \
                             + 'format but got data in type: ' \
                             + str(type(data)))

    def _create_patient_id(self):
        with open(patients_db_file, 'r') as f:
            patients = json.load(f)
        ids = patients.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        patient_id = max(ids) + 1
        return patient_id

    def create_patient(self, json_data):
        self.logger.info('Creating a new patient')

        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['emergency_contact_id', 'user_id', 'patient_history']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        emergency_contact_id = json_data['emergency_contact_id']
        user_id = json_data['user_id']
        patient_history = json_data['patient_history']
        created_at = time.time()

        #self._check_emergency_contact_id(emergency_contact_id)
        #self._check_user_id(user_id)

        new_patient_id = self._create_patient_id()
        with open(patients_db_file, 'r') as f:
            patients = json.load(f)
        patients[str(new_patient_id)] = {
            "emergency_contact_id": emergency_contact_id,
            "user_id": user_id,
            "patient_history": patient_history,
            "created_at": created_at,
        }
        with open(patients_db_file, 'w') as f:
            data = json.dumps(patients)
            f.write(data)
        self.logger.info('Created patient with patient id %s',str(new_patient_id))
        return str(new_patient_id)

    def get_patient(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['patient_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        patient_id = json_data['patient_id']
        self._check_patient_id(patient_id)
        with open(patients_db_file, 'r') as f:
            patients = json.load(f)
        return patients[patient_id]

    def delete_patient(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['patient_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        patient_id = json_data['patient_id']
        self._check_patient_id(patient_id)
        with open(patients_db_file, 'r') as f:
            patients = json.load(f)
        self.logger.info('Deleting patient with patient id %s',str(patient_id))
        del patients[patient_id]
        with open(patients_db_file, 'w') as f:
            data = json.dumps(patients)
            f.write(data)
        self.logger.info('Deleted patient with patient id %s',str(patient_id))
        return patient_id
        
    def update_patient(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['patient_id', 'emergency_contact_id', 'user_id', 'patient_history']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        patient_id = json_data['patient_id']
        emergency_contact_id = json_data['emergency_contact_id']
        user_id = json_data['user_id']
        patient_history = json_data['patient_history']

        #self._check_user_id(emergency_contact_id)
        #self._check_user_id(user_id)
        self._check_patient_id(patient_id)

        self.logger.info('Updating patient %s', patient_id)
        with open(patients_db_file, 'r') as f:
            patients = json.load(f)
        
        patients[str(patient_id)] = {
            "emergency_contact_id": emergency_contact_id,
            "user_id": user_id,
            "patient_history": patient_history,
            "created_at": patients[str(patient_id)]["created_at"],
            "updated_at": time.time()
        }
        with open(patients_db_file, 'w') as f:
            data = json.dumps(patients)
            f.write(data)
        self.logger.info('Updated patient with patient id %s',str(patient_id))
        return patient_id
        
    def get_patients(self):
        with open(patients_db_file, 'r') as f:
            patients = json.load(f)
        
        client = MongoClient('localhost', 27017)
        db = client.patientMonitorDB
        array = list(patients.values())
        patients = {"head": [], "data": []}
        for patient in array:
            user = db.users.find_one({"_id": ObjectId(patient["user_id"])})
            if "created_at" in user:
                del user['created_at']
            if "updated_at" in user:
                del user['updated_at']
            del user["_id"]
            user["date_of_birth"] = user["date_of_birth"].strftime('%d %b %Y')
            patient['created_at'] = time.ctime(patient['created_at'])
            if 'updated_at' in patient:
                patient['updated_at'] = time.ctime(patient['updated_at'])
            else:
                patient['updated_at'] = '-'
            patients["data"].append(list(user.values()) + list(patient.values())[1:])
        patients["head"] = ['First Name', 'Last Name', 'DOB', 'Address',
                        'State', 'Zip code', 'Phone Number', 'Email',
                        'Emergency Contact Id', 'Patient History', 'Created', 'Updated']
        return patients
