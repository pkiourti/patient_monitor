from device import Device
import random
import string
import json
import logging

class DeviceInstance(Device):

    def __init__(self, device_type, serial_number, owner):
        super(DeviceInstance, self).__init__(device_type, serial_number)
        self.key = self.__create_key(owner, serial_number)
        self.owner = owner
        self.logger = logging.getLogger('Logger ' + self.device_type + \
                                        ' ' + self.serial_number + \
                                        ' ' + self.owner)

    def __create_key(self, name, number):
        return ''.join([random.choice(string.ascii_letters + string.digits) \
                            for _ in range(15)])

    
    def send_data(self, data):
        self.logger.info(self.key + ': parsing sent data')
        json_data = ''
        try:
            json.loads(data)
        except:
            self.logger.warning(self.key + ': Expected json data in a str ' + \
                             'format but got data in type: ' + str(type(data)))
