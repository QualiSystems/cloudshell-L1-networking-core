#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.layer_one.core.response.resource_info.entities.base import ResourceInfo


class Port(ResourceInfo):
    """
    Port resource entity
    """
    NAME_TEMPLATE = 'Port{}'
    FAMILY_NAME = 'L1 Switch Port'

    def __init__(self, resource_id, model_name, serial_number, mapping=None):
        name = self.NAME_TEMPLATE.format(resource_id)
        family_name = self.FAMILY_NAME
        super(Port, self).__init__(resource_id, name, family_name, model_name, serial_number, mapping)
