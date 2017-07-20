from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import Element

from cloudshell.layer_one.core.response.resource_info.resource_info_builder import ResourceInfoBuilder


class ResponseInfo(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def build_xml_node(self):
        pass

    @staticmethod
    def _build_response_info_node():
        return Element('ResponseInfo')


class ResourceDescriptionResponseInfo(ResponseInfo):
    def __init__(self, resource_info):
        if isinstance(resource_info, list):
            self.resource_info_list = resource_info
        else:
            self.resource_info_list = [resource_info]

    def build_xml_node(self):
        response_info_node = self._build_response_info_node()
        for resource_info in self.resource_info_list:
            response_info_node.append(ResourceInfoBuilder.build_resource_info_nodes(resource_info))
        return response_info_node


class SimpleResponseInfo(ResponseInfo):
    def __init__(self, attributes_dict):
        """
        :param attributes_dict:
        :type attributes_dict: dict
        """
        self.attributes_dict = attributes_dict

    def build_xml_node(self):
        response_info_node = self._build_response_info_node()
        for name, value in self.attributes_dict.iteritems():
            attribute_node = Element(name)
            attribute_node.text = value
            response_info_node.append(attribute_node)
        return response_info_node
