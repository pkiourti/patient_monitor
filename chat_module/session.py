import logging
import os
import json
from itertools import compress

sessions_db_file = os.path.join('db', 'sessions.json')

class Session:
    """
    Class that creates a new Device Type
    """

    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def _check_session_id(self, session_id):
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        if not session_id.isdecimal():
            self.logger.error("Session id %s " + \
                        "is not an decimal number", session_id)
            raise ValueError(35, "Session id %s " + \
                        "is not an decimal number", session_id)
        if session_id not in sessions:
            self.logger.error('Session id ' \
                        + session_id + ' does not exist')
            raise ValueError(36, 'Session id ' \
                        + session_id + ' does not exist')

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

    def _create_session_id(self):
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        ids = sessions.keys() if sessions else None
        ids = [int(id) for id in ids] if ids else [-1]
        session_id = max(ids) + 1
        return session_id

    def create_session(self, json_data):
        self.logger.info('Creating a new session')
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['device_id', 'participants']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        device_id = json_data['device_id']
        participants = json_data['participants']
        created_at = time.time()

        self._check_device_id(device_id)

        new_session_id = self._create_session_id()
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        sessions[str(new_session_id)] = {
            "device_id": device_id,
            "participants": participants,
            "created_at": created_at,
        }
        with open(sessions_db_file, 'w') as f:
            data = json.dumps(sessions)
            f.write(data)
        self.logger.info('Created session with session id ' + \
                         str(new_session_id))
        return str(new_session_id)

    def get_session(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['session_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        session_id = json_data['session_id']
        self._check_session_id(session_id)
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        session = sessions[str(session_id)]

        return {"session": session}

    def update_session(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['session_id', 'session']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        session_id = json_data['session_id']
        device_id = json_data['device_id']

        self._check_session_id(session_id)
        self._check_device_id(device_id)

        self.logger.info('Updating session %s', session_id)
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        sessions[str(session_id)] = session
        with open(sessions_db_file, 'w') as f:
            data = json.dumps(sessions)
            f.write(data)
        self.logger.info('Updated session with session id ' + \
                         str(session_id))
        return session_id

    def delete_session(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)

        required_data = ['session_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        session_id = json_data['session_id']

        self._check_session_id(session_id)

        self.logger.info('Deleting session %s', session_id)
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        del sessions[session_id]
        with open(sessions_db_file, 'w') as f:
            data = json.dumps(sessions)
            f.write(data)
        self.logger.info('Deleted session with session id ' + \
                         str(session_id))
        return session_id

    def get_sessions(self):
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        return sessions
