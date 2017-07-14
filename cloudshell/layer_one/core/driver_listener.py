import socket
from abc import ABCMeta

from cloudshell.layer_one.core.connection_handler import ConnectionHandler


class DriverListener(object):
    """
    Listen for new connection
    """
    __metaclass__ = ABCMeta
    BACKLOG = 100
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 1024

    def __init__(self, command_executor, xml_logger, command_logger):
        self._command_executor = command_executor
        self._command_logger = command_logger
        self._xml_logger = xml_logger
        self._is_running = False

    def _initialize_socket(self, host=SERVER_HOST, port=SERVER_PORT):
        """
        Initialize socket, and start listening
        :return: 
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._command_logger.debug('New socket created')
        try:
            server_socket.bind((host, int(port)))
            server_socket.listen(self.BACKLOG)
        except Exception as ex:
            # log will be  here
            self._command_logger.error(str(ex))
            raise
        self._command_logger.debug("Listen address {0}:{1}".format(host, port))
        self._is_running = True
        return server_socket

    def set_running(self, is_running):
        self._is_running = is_running

    def start_listening(self, host=SERVER_HOST, port=SERVER_PORT):
        """Initialize socket and start listening"""
        server_socket = self._initialize_socket(host, port)
        while self._is_running:
            connection, connection_data = server_socket.accept()
            self._command_logger.debug("New connection from {0}:{1}".format(connection_data[0], connection_data[1]))
            if connection is not None:
                request_handler = ConnectionHandler(connection, self._command_executor, self._xml_logger,
                                                    self._command_logger)
                request_handler.start()
