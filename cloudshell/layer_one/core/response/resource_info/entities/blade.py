from cloudshell.layer_one.core.response.resource_info.entities.base import ResourceInfo, Attribute


class Blade(ResourceInfo):
    def __init__(self, resource_id, model_name, serial_number):
        name = 'Blade{}'.format(resource_id)
        family_name = 'L1 Switch Blade'
        super(Blade, self).__init__(resource_id, name, family_name, model_name, serial_number)

    def attr_toggle_rate(self, value):
        self.attributes.append(Attribute('Toggle Rate', Attribute.NUMERIC, value))

    def attr_volt_monitor_operational(self, value):
        self.attributes.append(Attribute('Volt Monitor Operational', Attribute.NUMERIC, value))
