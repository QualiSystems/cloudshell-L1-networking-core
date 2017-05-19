from datetime import datetime


class Command(object):
    def __init__(self, command_name, command_id, command_args):
        """
        Command entity
        :param command_name: 
        :param command_id: 
        :param command_args:
        :type command_args: dict
        """
        self.command_name = command_name
        self.command_id = command_id
        self.command_args = command_args

        # Response attributes
        self.success = False
        self.error = None
        self.log = None
        self.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.response_info = None

