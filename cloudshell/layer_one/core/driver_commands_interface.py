from abc import ABCMeta, abstractmethod


class DriverCommandsInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def login(self, address, username, password):
        pass

    @abstractmethod
    def get_resource_description(self, address):
        pass

    @abstractmethod
    def map_bidi(self, src_port, dst_port):
        pass

    @abstractmethod
    def map_clear_to(self, src_port, dst_port):
        pass

    @abstractmethod
    def map_clear(self, src_port, dst_port):
        pass

    # @abstractmethod
    # def set_speed_manual(self, src_port, dst_port, speed, duplex):
    #     pass
    #
    # @abstractmethod
    # def get_attribute_value(self, address, attribute_name):
    #     pass