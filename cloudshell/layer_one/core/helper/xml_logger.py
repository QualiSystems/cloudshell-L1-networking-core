class XMLLogger(object):
    def __init__(self, path):
        self._descriptor = open(path, 'w+')

    def __del__(self):
        self._descriptor.close()

    def _write_data(self, data):
        self._descriptor.write(data + '\r\n')
        self._descriptor.flush()

    def info(self, data):
        self._write_data(data)
