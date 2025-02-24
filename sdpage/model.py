#------------------------------------------------------------------------
# Basic data model of SdPage
# sdpage.model
#------------------------------------------------------------------------
import copy
import json
import logging

logger = logging.getLogger(__name__)

class Metadata:
    def __init__(self, **kwargs):
        self.data = {
            'name': '', 
            'version': '', 
            'authors': [],
            }
        self.update(kwargs)
        
    def update(self, kvmap):
        self.data.update(kvmap)
        
    def firstAuthor(self):
        x = ''
        if len(self.authors)>0:
            x = self.authors[0]
        return x

    def toJson(self):
        jdata = copy.deepcopy(self.data)
        return jdata
    pass

class NamedNode:
    def __init__(self, name, baseType, children=[], **kwargs):
        self.name = name
        self.baseType = baseType
        self.parent = None
        self.children = []
        self.properties = {}
        self.setProperties(**kwargs)

    def fullName(self):
        fullname = self.name
        if self.parent:
            fullname = f'{self.parent.fullName()}.{self.name}'
        return fullname
    
    def addChild(self, c):
        self.children.append(c)
        
    def setChildren(self, v):
        self.children = v

    def nChildren(self):
        return len(self.children)

    def setProperties(self, **kwargs):
        self.properties = copy.deepcopy(kwargs)
        
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
            'baseType': self.baseType, 
            'children': [],  
        }
        for c in self.children:
            jdata['children'].append(c.toJson())
        return jdata

class Element(NamedNode):
    def __init__(self, name, baseType=None, children=[], **kwargs):
        self.baseComponent = None
        if issubclass(baseType.__class__, NamedNode):
            self.baseComponent = baseType
            baseType = baseType.name

        super().__init__(name, baseType, children, **kwargs)
        
        self.baseType = baseType
        for c in children:
            self.addChild(c)
        
class Model:
    def __init__(self):
        self.elements = []

    def addElement(self, e):
        self.elements.append(e)
        e.parent = self

    def findElement(self, ename):
        v = list(filter(lambda x: x.name == ename, self.elements) )
        e = None
        if len(v) == 1:
            e = v[0]
        return e
    
    def elementNames(self):
        names = [ e.name for e in self.elements ]
        return names
    
class Component(NamedNode):
    def __init__(self, name, baseType=None, children=[], **kargs):
        self.baseComponent = None
        if issubclass(baseType.__class__, NamedNode):
            self.baseComponent = baseType
            baseType = baseType.name
        super().__init__(name, baseType, children, **kargs)

    def componentType(self):
        return self.baseType

class Page:
    def __init__(self):
        self.filePath = None
        self.metadata = Metadata()
        self.model = None
        self.components = []
        self.properties = {}

    def load(self, fileName):
        self.filePath = fileName
        
    def saveJson(self, fn):
        jdata = {}
        jdata['metadata'] = self.metadata.toJson()
        jdata['model'] = self.model.toJson()
        
        components = []
        for c in self.components:
            components.append(c.toJson())
        jdata['components'] = components
        #
        properties = {}
        for pkey, pvalue in self.properties.items():
            properties[pkey] = pvalue
        jdata['properties'] = properties

        print(jdata)
        with open(fn, 'w') as fout:
            logger.info(f'Save model to JSON {fn}')
            json.dump(jdata, fout, indent=2)

    def saveXml(self, fn):
        logger.warning('saveXml is not available yet')
    pass

class PageBuilder(Page):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def findNodes(self, element):
        nodes = []
        cnames = []
        if element:
            if element.baseComponent:
                for child in element.baseComponent.children:
                    v = self.findNodes(child)
                    for c in v:
                        cfname = c.fullName()
                        if c and cfname not in cnames:
                            cnames.append(cfname)
                            nodes.append(c)
            else:
                for c in element.children:
                    v = self.findNodes(c)
                    for c in v:
                        cfname = c.fullName()
                        if c and cfname not in cnames:
                            cnames.append(cfname)
                            nodes.append(c)
            if element.baseComponent:
                nodes.append(element.baseComponent)
            if element.name not in cnames:
                nodes.append(element)
        return nodes
    
    def rearrange(self):
        logger.info('Rearrange page model={self.model}')
        if self.model:
            logger.info('Rearrange page')
            nodes = self.findNodes(self.model)
            print(nodes)
            for node in nodes:
                logger.info(f'  node {node.name}')
                if issubclass(node.__class__, Component):
                    self.components.append(node)
                fullname = node.fullName()
                for key, value in node.properties.items():
                    self.properties[f'{fullname}.{key}'] = value
        else:
            logger.warning('Builder model is None')
    
