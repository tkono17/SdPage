#------------------------------------------------------------------------
# Basic data model of SdModel
#------------------------------------------------------------------------

class Entity:
    def __init__(self, name, eType, **kargs):
        self.name = name
        self.eType = eType
        self.children = []
        self.properties = {}
        self.setProperties(**kargs)
        
    def addChild(self, c):
        self.children.append(c)
        
    def setChildren(self, v):
        self.children = v

    def nChildren(self):
        return len(self.children)

    def setProperties(self, **kargs):
        self.properties = kargs
        
    def setProperty(self, pName, pValue):
        self.properties[pName] = pvalue

    def property(self, pName):
        if pName in self.properties.keys():
            return self.properties[pName]
        else:
            return None
        
class ComponentType(Entity):
    def __init__(self, name, baseType=None, **kargs):
        super().__init__(name, baseType, **kargs)
        self.cType = baseType
        
    def componentType(self):
        return self.cType

    def baseType(self):
        return self.eType

class ComponentInstance(Entity):
    def __init__(self, name, cType, **kargs):
        super().__init__(name, cType, **kargs)

    def componentType(self):
        return self.eType

def CT(name, baseType=None, **kargs):
    return ComponentType(name, baseType, **kargs)

def CI(name, cType, **kargs):
    return ComponentInstance(name, cType, **kargs)
