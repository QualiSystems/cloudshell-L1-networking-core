from datetime import datetime


class Command(object):
    def __init__(self, command_name, command_id, command_params):
        """
        Command entity
        :param command_name: 
        :param command_id: 
        :param command_params:
        :type command_params: dict
        """
        self.command_name = command_name
        self.command_id = command_id
        self.command_params = command_params

        # Response attributes
        self.success = False
        self.error = None
        self.log = None
        self.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.response_info = None

    def __str__(self):
        return 'Command: {0}, {1}, {2}'.format(self.command_name, self.command_id, self.command_params)

    def __repr__(self):
        return self.__str__()
