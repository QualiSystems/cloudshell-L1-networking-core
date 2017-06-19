import re
import socket
import traceback
from threading import Thread

import time

from cloudshell.layer_one.core.request.request_commands_parser import RequestCommandsParser


class RequestHandler(Thread):
    REQUEST_END = r'</Commands>'
    END_COMMAND = '\r\n'

    def __init__(self, connection_socket, command_executor, xml_logger, command_logger, buffer_size=2048):
        """
        :param client_socket:
        :param command_executor:
        :type command_executor: cloudshell.layer_one.core.command_executor.CommandExecutor 
        :param xml_logger: logging.Logger
        :param command_logger: logging.Logger
        :param buffer_size: 
        """
        super(RequestHandler, self).__init__()
        self._connection_socket = connection_socket
        self._xml_logger = xml_logger
        self._command_logger = command_logger
        self._command_executor = command_executor
        self._buffer_size = buffer_size
        self._commands = []

    def run(self):
        self._read_request_commands()
        self._execute_commands()
        self._send_responses()

    def _read_request_commands(self):
        xml_request = ''
        while True:
            try:
                input_buffer = self._connection_socket.recv(self._buffer_size)
                if not input_buffer:
                    time.sleep(0.2)
                else:
                    xml_request += input_buffer.strip()
                    if re.search(self.REQUEST_END, xml_request):
                        break
                        # command_logger.debug('GOT: {}'.format(current_output))
            except socket.timeout:
                continue
            except:
                tb = traceback.format_exc()
                self._command_logger.critical(tb)
                raise
        self._xml_logger.info(xml_request.replace('\r', '') + "\n\n")
        self._commands = RequestCommandsParser.parse_request_commands(xml_request)
        self._command_logger.debug(self._commands)

    def _execute_commands(self):
        for command in self._commands:
            try:
                self._command_executor.execute_command(command)
                command.success = True
            except Exception as ex:
                command.success = False
                command.error = ex.message

    def _send_responses(self):
        responses = CommandResponsesBuilder.build_responses(commands)
