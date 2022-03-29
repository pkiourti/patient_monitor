import logging
import json

class Authentication:
    """
        Class that authenticates a user
    """

    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('Authentication Logger')
        self.logger.setLevel(logging.DEBUG)

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

    def authenticate(self, json_data):
        self.logger.info('Authenticating user')

        self._check_json(json_data)
        json_data = json.loads(json_data)

        email = json_data['email']
        password = json_data['password']

        if email == 'admin' and password == 'admin':
            return True
        else:
            return False
