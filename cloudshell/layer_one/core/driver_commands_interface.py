#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    def map_uni(self, src_port, dst_port):
        pass

    @abstractmethod
    def map_clear_to(self, src_port, dst_port):
        pass

    @abstractmethod
    def map_clear(self, ports):
        pass

    @abstractmethod
    def get_attribute_value(self, address, attribute_name):
        pass

    @abstractmethod
    def set_attribute_value(self, address, attribute_name, attribute_value):
        pass

    @abstractmethod
    def get_state_id(self):
        pass

    @abstractmethod
    def set_state_id(self, state_id):
        pass

    @abstractmethod
    def map_tap(self, src_port, dst_port):
        pass
