import re
import socket
import traceback
from threading import Thread

from cloudshell.layer_one.core.request.requests_parser import RequestsParser
from cloudshell.layer_one.core.response.command_responses_builder import CommandResponsesBuilder


class ConnectionClosedException(Exception):
    pass


class ConnectionHandler(Thread):
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
        super(ConnectionHandler, self).__init__()
        self._connection_socket = connection_socket
        self._xml_logger = xml_logger
        self._logger = logger
        self._command_executor = command_executor
        self._buffer_size = buffer_size

    def run(self):
        while True:
            try:
                commands = self._read_request_commands()
                responses = self._execute_commands(commands)
                self._send_responses(responses)
            except ConnectionClosedException:
                self._logger.debug('Connection closed')
                break
            except:
                tb = traceback.format_exc()
                self._logger.critical(tb)
                self._connection_socket.close()
                raise

    def _read_socket(self):
        data = ''
        while True:
            try:
                input_buffer = self._connection_socket.recv(self._buffer_size)
                if not input_buffer:
                    raise ConnectionClosedException()
                else:
                    data += input_buffer.strip()
                    if re.search(self.REQUEST_END, data):
                        break
            except socket.timeout:
                continue
        return data

    def _read_request_commands(self):
        xml_request = self._read_socket()
        self._xml_logger.info(xml_request.replace('\r', '') + "\n\n")
        requests = RequestsParser.parse_request_commands(xml_request)
        self._logger.debug(requests)
        return requests

    def _execute_commands(self, command_requests):
        return self._command_executor.execute_commands(command_requests)

    def _send_responses(self, responses):
        responses_string = CommandResponsesBuilder.to_string(responses)
        self._connection_socket.send(responses_string + self.END_COMMAND)
        self._xml_logger.info(responses_string)
