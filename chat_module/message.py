# Use code from https://tinyurl.com/mvj637j6
# to check if a string is hexadecimal

import time
import logging
import string
import json
import os
from itertools import compress

sessions_db_file = os.path.join('db', 'sessions.json')
messages_db_file = os.path.join('db', 'messages.json')

class Message:
    """
    Class that creates a new message
    """
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('Message Logger')
        self.logger.setLevel(logging.DEBUG)

    def _check_session_id(self, session_id):
        with open(sessions_db_file, 'r') as f:
            sessions = json.load(f)
        ids = sessions.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not session_id.isdecimal():
            self.logger.error("Session id %s " + \
                        "is not an decimal number", session_id)
            raise ValueError(35, "Session id %s " + \
                        "is not an decimal number", session_id)
        if int(session_id) not in ids:
            self.logger.error('Session id ' \
                        + session_id + ' does not exist')
            raise ValueError(36, 'Session id ' \
                        + session_id + ' does not exist')

    def _check_message_id(self, message_id):
        with open(messages_db_file, 'r') as f:
            messages = json.load(f)
        ids = messages.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        if not message_id.isdecimal():
            self.logger.error("Message id %s " + \
                        "is not an decimal number", message_id)
            raise ValueError(37, "Message id %s " + \
                        "is not an decimal number", message_id)
        if int(message_id) not in ids:
            self.logger.error('Message id ' \
                        + message_id + ' does not exist')
            raise ValueError(38, 'Message id ' \
                        + message_id + ' does not exist')

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

    def _create_message_id(self):
        with open(messages_db_file, 'r') as f:
            messages = json.load(f)
        ids = messages.keys()
        ids = [int(id) for id in ids] if ids else [-1]
        message_id = max(ids) + 1
        return message_id

    def create_message(self, json_data):
        self.logger.info('Creating a new message')

        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['session_id', 'message']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        session_id = json_data['session_id']
        message = json_data['message']

        self._check_session_id(session_id)
        self._check_message(message)
        created_at = time.time()
        new_message_id = self._create_message_id()
        with open(messages_db_file, 'r') as f:
            messages = json.load(f)
        messages[str(new_message_id)] = {
            "session_id": str(session_id),
            "message": message,
            "created_at": created_at,
        }
        with open(messages_db_file, 'w') as f:
            data = json.dumps(messages)
            f.write(data)
        self.logger.info('Created message with message id %s',str(new_message_id))
        return str(new_message_id)

    def get_message(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['message_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        message_id = json_data['message_id']
        self._check_message_id(message_id)
        with open(messages_db_file, 'r') as f:
            messages = json.load(f)
        return messages[message_id]

    def delete_message(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        required_data = ['message_id']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        message_id = json_data['message_id']
        self._check_message_id(message_id)
        with open(messages_db_file, 'r') as f:
            messages = json.load(f)
        self.logger.info('Deleting message with message id %s',str(message_id))
        del messages[message_id]
        with open(messages_db_file, 'w') as f:
            data = json.dumps(messages)
            f.write(data)
        self.logger.info('Deleted message with message id %s',str(message_id))
        return message_id
        
    def update_message(self, json_data):
        self._check_json(json_data)
        json_data = json.loads(json_data)
        
        required_data = ['message_id', 'session_id', 'message']
        required_exist = [elem in json_data.keys() for elem in required_data]
        if not all(required_exist):
            missing_data = list(set(required_data) \
                    - set(compress(required_data, required_exist)))
            self.logger.error("Missing required data %s", missing_data)
            raise ValueError(11, "Missing required data %s", missing_data)

        message_id = json_data['message_id']
        session_id = json_data['session_id']
        message = json_data['message']

        self._check_message_id(message_id)
        self._check_session_id(session_id)
        self._check_message(message)
        updated_at = time.time()

        self.logger.info('Updating message %s', message_id)
        with open(messages_db_file, 'r') as f:
            messages = json.load(f)
        
        messages[str(message_id)] = {
            "session_id": str(session_id),
            "message": str(message),
            "created_at": messages[str(message_id)]["created_at"],
            "updated_at": updated_at
        }
        with open(messages_db_file, 'w') as f:
            data = json.dumps(messages)
            f.write(data)
        self.logger.info('Updated message with message id %s',str(message_id))
        return message_id
        
    def get_messages(self):
        with open(messages_db_file, 'r') as f:
            messages = json.load(f)
        return messages
