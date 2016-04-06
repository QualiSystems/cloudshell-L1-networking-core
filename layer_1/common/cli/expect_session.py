__author__ = 'g8y3e'

import re
import socket
import time

from collections import OrderedDict

from cloudshell.cli.session import Session
from cloudshell.cli.helper.normalize_buffer import normalize_buffer

class ExpectSession(Session):

    def __init__(self, handler=None, username=None, password=None, host=None, port=None,
                 timeout=60, new_line='\r', logger=None, **kwargs):
        self._handler = handler
        self._logger = logger
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self._new_line = new_line
        self._timeout = timeout

    def _receive_with_retries(self, timeout, retries_count):
        current_retries = 0
        current_output = None

        while current_retries < retries_count:
            current_retries += 1

            try:
                current_output = self._receive(timeout)
            except socket.timeout:
                continue
            except Exception as err:
                raise err

            break

        return current_output

    def send_line(self, data_str):
        self._send(data_str + self._new_line)

    def hardware_expect(self, data_str=None, re_string='', expect_map=OrderedDict(),
                        error_map=OrderedDict(), timeout=None, retries_count=3):
        """

        :param data_str:
        :param re_string:
        :param expect_map:
        :param error_map:
        :param timeout:
        :param retries_count:
        :return:
        """

        if data_str is not None:
            self.send_line(data_str)

        if re_string is None or len(re_string) == 0:
            raise Exception('ExpectSession', 'Expect list is empty!')

        output_str = self._receive_with_retries(timeout, retries_count)
        if output_str is None:
            raise Exception('ExpectSession', 'Empty response from device!')

        # Loop until one of the expressions is matched or loop forever if
        # nothing is expected (usually used for exit)
        output_list = list()
        while True:
            if re.search(re_string, output_str, re.DOTALL):
                break
            else:
                time.sleep(0.2)

            for expect_string in expect_map:
                result_match = re.search(expect_string, output_str, re.DOTALL)
                if result_match:
                    expect_map[expect_string]()
                    output_list.append(output_str)
                    output_str = ''

            current_output = self._receive_with_retries(timeout, retries_count)
            if current_output is None:
                output_str = ''.join(output_list) + output_str
                self._logger.error("Can't find prompt in output: \n" + output_str)
                raise Exception('ExpectSession', 'Empty response from device!')
            output_str += current_output

        output_str = ''.join(output_list) + output_str
        for error_string in error_map:
            result_match = re.search(error_string, output_str, re.DOTALL)
            if result_match:
                raise Exception('ExpectSession', error_map[error_string])

        return normalize_buffer(output_str)
