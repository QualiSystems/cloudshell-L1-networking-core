#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from cloudshell.layer_one.core.layer_one_driver_exception import LayerOneDriverException
from cloudshell.layer_one.core.response.command_response import CommandResponse


class CommandResponseManager(object):
    """
    Generate and manage command response 
    """

    def __init__(self, command_request, logger):
        self._command_response = CommandResponse(command_request)
        self._logger = logger

    def __enter__(self):
        return self._command_response

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self._command_response.success = False
            self._command_response.error = exc_type.__name__
            self._command_response.log = exc_val.message
            # self._logger.critical(traceback.print_exception(exc_type, exc_val, exc_tb))
        else:
            self._command_response.success = True
            # return True


class CommandExecutor(object):
    def __init__(self, logger):
        self._logger = logger
        self._state_id = None
        self._registered_commands = {'Login': self.login_executor,
                                     'GetResourceDescription': self.get_resource_description_executor,
                                     'MapBidi': self.map_bidi_executor,
                                     'MapUni': self.map_uni_executor,
                                     'MapClearTo': self.map_clear_to_executor,
                                     'MapClear': self.map_clear_executor}

    @abstractmethod
    def _driver_instance(self):
        """
        Create instance of the driver
        :return: 
        :rtype: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        """
        pass

    def execute_commands(self, command_requests):
        """
        Execute bunch of commands
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

    def login_executor(self, command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        :rtype: CommandResponse
        """
        address = command_request.command_params.get('Address')[0]
        user = command_request.command_params.get('User')[0]
        password = command_request.command_params.get('Password')[0]

        with CommandResponseManager(command_request, self._logger) as command_response:
            command_response.response_info = driver_instance.login(address, user, password)
        return command_response

    def get_resource_description_executor(self, command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return:
        :rtype: CommandResponse
        """
        address = command_request.command_params.get('Address')[0]
        with CommandResponseManager(command_request, self._logger) as command_response:
            command_response.response_info = driver_instance.get_resource_description(address)
        return command_response

    def map_bidi_executor(self, command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        """
        port_a = command_request.command_params.get('MapPort_A')[0]
        port_b = command_request.command_params.get('MapPort_B')[0]
        # mapping_group = command_request.command_params('MappingGroupName')
        with CommandResponseManager(command_request, self._logger) as command_response:
            command_response.response_info = driver_instance.map_bidi(port_a, port_b)
        return command_response

    def map_uni_executor(self, command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        """
        src_port = command_request.command_params.get('SrcPort')[0]
        dst_port = command_request.command_params.get('DstPort')[0]
        # mapping_group = command_request.command_params('MappingGroupName')
        with CommandResponseManager(command_request, self._logger) as command_response:
            command_response.response_info = driver_instance.map_uni(src_port, dst_port)
        return command_response

    def map_clear_to_executor(self, command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        """
        src_port = command_request.command_params.get('SrcPort')[0]
        dst_ports = command_request.command_params.get('DstPort')
        with CommandResponseManager(command_request, self._logger) as command_response:
            for dst_port in dst_ports:
                driver_instance.map_clear_to(src_port, dst_port)
        return command_response

    def map_clear_executor(self, command_request, driver_instance):
        """
        :param command_request:
        :type command_request: cloudshell.layer_one.core.entities.command.Command
        :param driver_instance
        :type driver_instance: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        :return: 
        """
        ports = command_request.command_params.get('MapPort')
        with CommandResponseManager(command_request, self._logger) as command_response:
            command_response.response_info = driver_instance.map_clear(ports)
        return command_response
