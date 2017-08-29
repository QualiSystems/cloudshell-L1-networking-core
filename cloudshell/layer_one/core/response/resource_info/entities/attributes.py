from cloudshell.layer_one.core.response.resource_info.entities.base import Attribute


class StringAttribute(Attribute):
    def __init__(self, name, value):
        super(StringAttribute, self).__init__(name, Attribute.STRING, value)


class NumericAttribute(Attribute):
    def __init__(self, name, value):
        super(NumericAttribute, self).__init__(name, Attribute.NUMERIC, value)


class BooleanAttribute(Attribute):
    TRUE = 'True'
    FALSE = 'False'
    DEFAULT_VALUE = TRUE

    def __init__(self, name, value):
        super(BooleanAttribute, self).__init__(name, Attribute.BOOLEAN, value)
