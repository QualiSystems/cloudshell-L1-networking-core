from abc import abstractmethod

from cloudshell.layer_one.core.layer_one_driver_exception import LayerOneDriverException
from cloudshell.layer_one.core.response.command_response import CommandResponse


class CommandResponseManager(object):
    """
    Generate and manage command response 
    """

    def __init__(self, command_request):
        self._command_response = CommandResponse(command_request)

    def __enter__(self):
        return self._command_response

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self._command_response.success = False
            self._command_response.error = exc_type.__name__
            self._command_response.log = exc_val.message
        else:
            self._command_response.success = True
        return True


class CommandExecutor(object):
    def __init__(self, logger):
        self._logger = logger
        self._registered_commands = {'Login': self.login_executor,
                                     'GetResourceDescription': self.get_resource_description_executor,
                                     'GetStateId': self.get_state_id_executor}

    @abstractmethod
    def _driver_instance(self):
        """
        Create instance of driver commands
        :return: 
        :rtype: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        """
        pass

    def execute_commands(self, command_requests):
        """
        :param command_requests: 
        :return:
        :rtype: list
        """
        driver = self._driver_instance()
        command_responses = []
        for command_request in command_requests:
            self._logger.info('Executing command {}'.format(command_request.command_name))
            if command_request.command_name in self._registered_commands:
                response = self._registered_commands[command_request.command_name](command_request, driver)
                command_responses.append(response)
            else:
                raise LayerOneDriverException(self.__class__.__name__,
                                              'Incorrect command name, or command not registered')

        return command_responses

    @staticmethod
    def login_executor(command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        :rtype: CommandResponse
        """
        address = command_request.command_params.get('Address')
        user = command_request.command_params.get('User')
        password = command_request.command_params.get('Password')

        with CommandResponseManager(command_request) as command_response:
            command_response.response_info = driver_instance.login(address, user, password)
        return command_response

    @staticmethod
    def get_resource_description_executor(command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return:
        :rtype: CommandResponse
        """
        address = command_request.command_params.get('Address')
        with CommandResponseManager(command_request) as command_response:
            command_response.response_info = driver_instance.get_resource_description(address)
        return command_response

    @staticmethod
    def map_bidi_executor(command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        """
        with CommandResponseManager(command_request) as command_response:
            pass
        return command_response

    @staticmethod
    def get_state_id_executor(command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return:
        :rtype: CommandResponse
        """
        with CommandResponseManager(command_request) as command_response:
            pass
        return command_response
