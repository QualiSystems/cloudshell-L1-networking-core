from cloudshell.layer_one.core.entities.command import Command
from cloudshell.layer_one.core.helper.xml_helper import XMLHelper


class RequestCommandsParser(object):
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def _build_command_instance(command_node):
        """
        Build command instance for command node
        :param command_node: 
        :type command_node: xml.etree.ElementTree.Element
        :return:
        :rtype: cloudshell.layer_one.core.entities.command.Command
        """
        command_name = command_node.get('CommandName')
        command_id = command_node.get('CommandId')
        command_params = {}
        namespace = XMLHelper.get_node_namespace(command_node)
        parameters_node = command_node.find(namespace + 'Parameters')

        if parameters_node is not None:
            for param_node in parameters_node:
                command_params[param_node.tag.replace(namespace, '')] = param_node.text

        return Command(command_name, command_id, command_params)

    @staticmethod
    def parse_request_commands(xml_request):
        """
        Parse xml request and create command instances
        :param xml_request: 
        :return:
        :rtype: list
        """
        commands = []
        request_node = XMLHelper.build_node_from_string(xml_request)
        for command_node in request_node:
            commands.append(RequestCommandsParser._build_command_instance(command_node))
        return commands
