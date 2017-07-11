import re
import socket
import time
import traceback
from threading import Thread

from cloudshell.layer_one.core.request.request_commands_parser import RequestCommandsParser
from cloudshell.layer_one.core.response.command_responses_builder import CommandResponsesBuilder


class RequestHandler(Thread):
    REQUEST_END = r'</Commands>'
    END_COMMAND = '\r\n'

    def __init__(self, connection_socket, command_executor, xml_logger, logger, buffer_size=2048):
        """
        
        :param connection_socket:
        :type connection_socket: socket.socket
        :param command_executor:
        :type command_executor: cloudshell.layer_one.core.command_executor.CommandExecutor
        :param xml_logger: 
        :param logger: 
        :param buffer_size: 
        """
        super(RequestHandler, self).__init__()
        self._connection_socket = connection_socket
        self._xml_logger = xml_logger
        self._logger = logger
        self._command_executor = command_executor
        self._buffer_size = buffer_size

    def run(self):
        commands = self._read_request_commands()
        responses = self._execute_commands(commands)
        self._send_responses(responses)

    def _read_socket(self):
        data = ''
        while True:
            try:
                input_buffer = self._connection_socket.recv(self._buffer_size)
                if not input_buffer:
                    time.sleep(0.2)
                else:
                    data += input_buffer.strip()
                    if re.search(self.REQUEST_END, data):
                        break
                        # command_logger.debug('GOT: {}'.format(current_output))
            except socket.timeout:
                continue
            except:
                tb = traceback.format_exc()
                self._logger.critical(tb)
                raise
        return data

    def _read_request_commands(self):
        xml_request = self._read_socket()
        self._xml_logger.info(xml_request.replace('\r', '') + "\n\n")
        commands = RequestCommandsParser.parse_request_commands(xml_request)
        self._logger.debug(commands)
        return commands

    def _execute_commands(self, commands):
        self._command_executor.execute_commands(commands)

    def _send_responses(self, commands):
        responses = CommandResponsesBuilder.build_responses(commands)
        self._connection_socket.send(responses)
        self._xml_logger.info(responses)
