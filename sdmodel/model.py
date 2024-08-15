#------------------------------------------------------------------------
# Basic data model of SdModel
# sdmodel.model
#------------------------------------------------------------------------
import copy
import json
import logging

logger = logging.getLogger(__name__)

class NamedNode:
    def __init__(self, name, cType, **kargs):
        self.name = name
        self.cType = cType
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

    def toJson(self):
        jdata = {
            'name': self.name, 
            'cType': self.cType, 
            'children': [],  
            'properties': self.properties
        }
        for c in self.children:
            jdata['children'].append(c.toJson())
        return jdata
        
class ComponentType(NamedNode):
    def __init__(self, name, baseType=None, **kargs):
        super().__init__(name, baseType, **kargs)
        self.cType = baseType
        
    def componentType(self):
        return self.cType

    def baseType(self):
        return self.cType

class ComponentInstance(NamedNode):
    def __init__(self, name, cType, **kargs):
        super().__init__(name, cType, **kargs)

    def componentType(self):
        return self.cType

def CT(name, baseType=None, **kargs):
    return ComponentType(name, baseType, **kargs)

def CI(name, cType, **kargs):
    return ComponentInstance(name, cType, **kargs)

class Model:
    def __init__(self):
        self.data = {'header': {},
                     'model': None,
                     'components': [],
                     'properties': {}
                     }

    def setHeader(self, x):
        self.data['header'] = x
        
    def setModel(self, x):
        self.data['model'] = x
        
    def setComponents(self, x):
        self.data['components'] = x
        
    def setProperties(self, x):
        self.data['properties'] = x
        
    def header(self):
        return self.data['header']

    def model(self):
        return self.data['model']

    def components(self):
        return self.data['components']

    def properties(self):
        return self.data['properties']

    def saveJson(self, fn):
        jdata = copy.deepcopy(self.data)
        jdata['model'] = self.data['model'].toJson()
        jdata['components'] = []
        for c in self.data['components']:
            jdata['components'].append(c.toJson())
        with open(fn, 'w') as fout:
            logger.info(f'Save model to JSON {fn}')
            json.dump(jdata, fout, indent=2)
    pass
    
