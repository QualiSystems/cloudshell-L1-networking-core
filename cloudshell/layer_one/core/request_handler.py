from threading import Thread


class RequestHandler(Thread):
    def __init__(self, client_socket, xml_logger, command_logger):
        super(RequestHandler, self).__init__()
        self._client_socket = client_socket
        self._xml_logger = xml_logger
        self._command_logger = command_logger

    def run(self):
        super(RequestHandler, self).run()
        pass
