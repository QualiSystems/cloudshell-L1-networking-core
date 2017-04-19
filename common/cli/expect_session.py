import re
import socket
import time
from collections import OrderedDict

from common.configuration_parser import ConfigurationParser
from common.cli.helper.normalize_buffer import normalize_buffer
from common.cli.session import Session


class ExpectSession(Session):
    def __init__(self, handler=None, timeout=60, new_line='\r', reconnect_count=3,
                 logger=None, **kwargs):
        self._handler = handler
        self._logger = logger

        self._new_line = new_line
        self._timeout = timeout

        self._host = None
        self._username = None
        self._password = None
        self._port = None

        self._reconnect_count = reconnect_count

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def init(self, host, username, password, port=None):
        self._host = host

        self._username = username
        self._password = password

        if port is not None:
            self._port = port
        else:
            self._port = ConfigurationParser.get("common_variable", "connection_port")

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

    def send_command(self, data_str=None, re_string='', expect_map=OrderedDict(),
                     error_map=OrderedDict(), timeout=None, retries_count=3, logger=None):
        reconnect_count = 0
        while reconnect_count < self._reconnect_count:
            try:
                output_str = self.hardware_expect(data_str, re_string, expect_map, error_map, timeout,
                                                  retries_count, logger)

                return output_str
            except Exception as error_object:
                self.reconnect(re_string)

            reconnect_count += 1

        raise Exception('ExpectSession', 'Can\'t connect to device!')

    def hardware_expect(self, data_str=None, re_string='', expect_map=OrderedDict(),
                        error_map=OrderedDict(), timeout=None, retries_count=3, logger=None):
        """

        :param data_str:
        :param re_string:
        :param expect_map:
        :param error_map:
        :param timeout:
        :param retries_count:
        :return:
        """

        if not logger:
            logger = self._logger

        if data_str is not None:
            self.send_line(data_str)

        if re_string is None or len(re_string) == 0:
            # log
            return ""

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
                if logger:
                    logger.error("Can't find prompt in output: \n" + output_str)
                raise Exception('ExpectSession', 'Empty response from device!')
            output_str += current_output

        output_str = ''.join(output_list) + output_str
        for error_string in error_map:
            result_match = re.search(error_string, output_str, re.DOTALL)
            if result_match:
                raise Exception('ExpectSession', error_map[error_string])

        return normalize_buffer(output_str)
