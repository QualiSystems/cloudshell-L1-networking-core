from abc import abstractmethod

from cloudshell.layer_one.core.layer_one_driver_exception import LayerOneDriverException
from cloudshell.layer_one.core.response.command_response import CommandResponse


class CommandExecutor(object):
    def __init__(self, logger):
        self._logger = logger
        self._registered_commands = {'Login': self.login_executor,
                                     'GetResourceDescription': self.get_resource_description_executor}

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
            try:
                self._logger.info('Executing command {}'.format(command_request.command_name))
                if command_request.command_name in self._registered_commands:
                    response = self._registered_commands[command_request.command_name](command_request, driver)
                    command_responses.append(response)
                else:
                    raise LayerOneDriverException(self.__class__.__name__,
                                                  'Incorrect command name, or command not registered')
                command_response.success = True
            except Exception as ex:
                command_response.success = False
                command_response.error = ex.message
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
        address = command_request.command_params.get('address')
        user = command_request.command_params.get('user')
        password = command_request.command_params.get('password')

        command_response = CommandResponse(command_request)
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
        command_response = CommandResponse(command_request)
        command_response.response_info = driver_instance.get_resource_description(address)
        return command_response

    @staticmethod
    def map_bidi_executor(command_response, driver_instance):
        """
        :param command_response:
        :type command_response: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        """
        pass
