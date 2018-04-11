#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket

from collections import OrderedDict

from common.cli.expect_session import ExpectSession


class TCPSession(ExpectSession):
    _DEFAULT_BUFFER = 512

    def _init_handler(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, *args, **kwargs):
        ExpectSession.__init__(self, self._init_handler(), *args, **kwargs)

        self._buffer_size = TCPSession._DEFAULT_BUFFER
        if 'buffer_size' in kwargs:
            self._buffer_size = kwargs['buffer_size']

        if self._port is not None:
            self._port = int(self._port)

        self._command = None
        self._error_map = None

    def connect(self, host, username, password, command=None, error_map=None, action_map=None, port=None, re_string=''):
        """
            Connect to device

            :param expected_str: regular expression string
            :return:
        """

        if self._command is None:
            self._command = command

        if not self._error_map:
            self._error_map = error_map or OrderedDict()

        if action_map in None:
            action_map = OrderedDict()

        ExpectSession.init(self, host, username, password, port)

        server_address = (self._host, self._port)

        self._handler = self._init_handler()
        self._handler.connect(server_address)

        self._handler.settimeout(self._timeout)
        self.hardware_expect(re_string=re_string)
        output = self.hardware_expect(self._command,
                                      error_map=self._error_map,
                                      expect_map=action_map,
                                      re_string=re_string)

        return output

    def reconnect(self, re_string=''):
        self.disconnect()
        self._handler = self._init_handler()

        return self.connect(self._host, self._username, self._password, port=self._port, re_string=re_string)

    def disconnect(self):
        """
            Disconnect from device

            :return:
        """

        self._handler.close()

    def _send(self, data_str):
        """
            Send data to device

            :param data_str: ommand string
            :return:
        """
        self._handler.sendall(data_str)

    def _receive(self, timeout=None):
        """
            Read data from device

            :param timeout: time for waiting buffer
            :return: str
        """
        timeout = timeout if timeout else self._timeout
        self._handler.settimeout(timeout)

        data = self._handler.recv(self._buffer_size)
        return data
