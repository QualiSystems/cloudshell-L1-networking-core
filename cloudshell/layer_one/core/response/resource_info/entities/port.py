from cloudshell.layer_one.core.response.resource_info.entities.base import ResourceInfo, Attribute


class Port(ResourceInfo):
    def __init__(self, resource_id, model_name, serial_number):
        name = 'Port{}'.format(resource_id)
        family_name = 'L1 Switch Port'
        super(Port, self).__init__(resource_id, name, family_name, model_name, serial_number)

    def attr_protocol_type(self, value):
        self.attributes.append(Attribute('Protocol Type', Attribute.NUMERIC, value))

    def attr_toggle_mode(self, value):
        self.attributes.append(Attribute('Toggle Mode', Attribute.NUMERIC, value))
