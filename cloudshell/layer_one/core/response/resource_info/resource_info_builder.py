import os
from cloudshell.layer_one.core.helper.xml_template_helper import XMLTemplateHelper


def full_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


class ResourceInfoBuilder(object):
    """
    Build resource info node
    """
    RESOURCE_TEMPLATE = full_path('templates/resource_template.xml')
    ATTRIBUTE_TEMPLATE = full_path('templates/resource_attribute_template.xml')
    MAPPING_TEMPLATE = full_path('templates/resource_incoming_map_template.xml')

    def __init__(self):
        self._mapping_template = XMLTemplateHelper.read_template(self.MAPPING_TEMPLATE)
        self._attribute_template = XMLTemplateHelper.read_template(self.ATTRIBUTE_TEMPLATE)
        self._resource_template = XMLTemplateHelper.read_template(self.RESOURCE_TEMPLATE)

    def _build_resource_node(self, resource_info):
        """
        Builde resource xml node
        :param resource_info:
        :type resource_info: cloudshell.layer_one.core.response.entities.base.ResourceInfo
        :return: Resource node
        :rtype: xml.etree.ElementTree.Element
        """
        node = XMLTemplateHelper.build_node_for_template(self._resource_template)
        node.set("Name", resource_info.name)
        node.set("ResourceFamilyName", resource_info.family_name)
        node.set("ResourceModelName", resource_info.model_name)
        node.set("SerialNumber", resource_info.serial_number)
        node.set("Address", resource_info.address)
        attributes_node = node.find("ResourceAttributes")
        for attribute in resource_info.attributes:
            attribute_node = self._build_attribute_node(attribute)
            attributes_node.append(attribute_node)
        if resource_info.mapping:
            node.append(self._build_mapping_node(resource_info.mapping))
        return node

    def _build_attribute_node(self, attribute):
        """
        Build attribute node
        :param attribute: 
        :type attribute: cloudshell.layer_one.core.response.entities.base.Attribute
        :return: Attribute node
        :rtype: xml.etree.ElementTree.Element
        """
        node = XMLTemplateHelper.build_node_for_template(self._attribute_template)
        node.set("Name", attribute.name)
        node.set("Type", attribute.type)
        node.set("Value", attribute.value)
        return node

    def _build_mapping_node(self, resource):
        """
        Build mapping node
        :param resource: 
        :type resource: cloudshell.layer_one.core.response.entities.base.ResourceInfo
        :return: Mapping node
        :rtype: xml.etree.ElementTree.Element
        """
        node = XMLTemplateHelper.build_node_for_template(self._mapping_template)
        child_incoming_node = node.find("IncomingMapping")
        child_incoming_node.text = resource.address
        return node

    def _build_resource_child_nodes(self, node, resource):
        """
        Build resource nodes for children recursively
        :param resource:
        :type resource: cloudshell.layer_one.core.response.entities.base.ResourceInfo
        :param node: 
        :type node: xml.etree.ElementTree.Element
        """
        if len(resource.child_resources) > 0:
            child_resources_node = node.find('ChildResources')
            for child_resource in resource.child_resources.values():
                child_node = self._build_resource_node(child_resource)
                child_resources_node.append(child_node)
                self._build_resource_child_nodes(child_node, child_resource)

    def build_resource_info_node(self, base_resource):
        """
        Build tree of xml nodes for resource tree
        :param base_resource:
        :type base_resource: cloudshell.layer_one.core.response.entities.base.ResourceInfo
        :return:
        :type: xml.etree.ElementTree.Element
        """
        base_resource_node = self._build_resource_node(base_resource)
        self._build_resource_child_nodes(base_resource_node, base_resource)
        return base_resource_node
