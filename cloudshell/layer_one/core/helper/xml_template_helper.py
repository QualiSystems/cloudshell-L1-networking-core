from xml.etree import ElementTree


class XMLTemplateHelper(object):
    @staticmethod
    def build_node_for_template(template):
        """
        Node for template
        :param template: 
        :type template: basestring
        :return:
        :rtype: xml.etree.ElementTree.Element
        """
        parser = ElementTree.XMLParser(encoding='utf-8')
        node = ElementTree.fromstring(template, parser=parser)
        return node

    @staticmethod
    def read_template(template_path):
        """
        Read template from file
        :param template_path: 
        :return: 
        :rtype: basestring
        """
        with open(template_path) as f:
            return f.read()
