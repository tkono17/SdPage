#------------------------------------------------------------------------
# Page builder
# sdmodel.builder
#------------------------------------------------------------------------
from .model import *

class ComponentInstance(NamedNode):
    def __init__(self, name, baseType, **kwargs):
        super().__init__(name, baseType, **kwargs)

    def componentType(self):
        return self.baseType

def CT(name, baseType=None, **kwargs):
    return Component(name, baseType, **kwargs)

def CI(name, baseType, **kwargs):
    return Component(name, baseType, **kwargs)

