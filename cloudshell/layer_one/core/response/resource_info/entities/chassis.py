#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.layer_one.core.response.resource_info.entities.base import ResourceInfo, Attribute


class Chassis(ResourceInfo):
    NAME_TEMPLATE = 'Chassis{}'
    FAMILY_NAME = 'L1 Switch'

    def __init__(self, resource_id, address, model_name, serial_number):
        self._address = address
        name = self.NAME_TEMPLATE.format(resource_id)
        family_name = self.FAMILY_NAME
        super(Chassis, self).__init__(resource_id, name, family_name, model_name, serial_number)

    @property
    def address(self):
        return self._address

    def attr_volt_monitor_1(self, value):
        self.attributes.append(Attribute('Volt Monitor 1', Attribute.NUMERIC, value))
