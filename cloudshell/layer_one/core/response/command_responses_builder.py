import os

from cloudshell.layer_one.core.helper.xml_helper import XMLHelper


def full_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


class ResponsesBuilder(object):
    RESPONSES_TEMPLATE = full_path('templates/responses_template.xml')
    COMMAND_RESPONSE_TEMPLATE = full_path('templates/command_response_template.xml')

    def __init__(self):
        self._responses_template = XMLHelper.read_template(self.RESPONSES_TEMPLATE)
        self._command_response_template = XMLHelper.read_template(self.COMMAND_RESPONSE_TEMPLATE)

    def _build_command_response_node(self, command):
        """
        Build command response node
        :param command: 
        :type command: cloudshell.layer_one.core.entities.command.Command
        :return: 
        :rtype: xml.etree.ElementTree.Element
        """
        command_response_node = XMLHelper.build_node_from_string(self._command_response_template)
        command_response_node.set('CommandName', command.command_name)
        command_response_node.set('CommandId', command.command_id)
        command_response_node.set('Success', str(command.success).lower())

        timestamp_node = command_response_node.find('Timestamp')
        timestamp_node.text = command.timestamp

        if command.error is not None:
            command_response_node.find('Error').text = command.error

        if command.log is not None:
            command_response_node.find('Log').text = command.log

        if command.response_info is not None:
            command_response_node.find('ResponseInfo').append(command.response_info)
        return command_response_node

    def build_responses(self, command_list):
        """
        Builde responses for command list
        :param command_list: 
        :type command_list: list
        :return:
        :rtype: xml.etree.ElementTree.Element
        """
        responses_node = XMLHelper.build_node_from_string(self._responses_template)
        for command in command_list:
            responses_node.append(self._build_command_response_node(command))
        return responses_node
