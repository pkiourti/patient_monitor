class DeviceType:
    """
    Class that creates a new Device Type
    """

    def __init__(self, dtype):
        self.device_type = dtype
        self.device_type_id = self.create_device()
        self.logger = logging.getLogger(dtype)

    def create_device(self):
        with open(device_type_db_file, 'r') as f:
            device_types = json.load(f)
        if self.device_type in device_types:
            self.logger.error('Device type', self.device_type, 'already exists')
            raise ValueError('Device type', self.device_type, 'already exists')
        device = devices[device_id]
        device_type_id = int(device[device_type_id])
        with open(device_type_db_file, 'r') as f:
            device_types = json.load(f)
        if device_type_id not in device_types:
            self.logger.error(self.assignment_id, ': Device type id', device_type_id, 'does not exist')
        device_type = device_types[device_type_id]
        return device_type
        for k, v in device_type_ids.items():
            if v == dtype:
                return k
