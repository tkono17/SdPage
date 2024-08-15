#------------------------------------------------------------------------
# Basic data model of SdModel
# sdmodel.io
#------------------------------------------------------------------------
import copy
import logging
import re
import json
import yaml

from .model import ComponentType, ComponentInstance, Model

logger = logging.getLogger(__name__)

class ModelReader:
    def __init__(self, fn=''):
        self.filePath = fn
        self.data = None
        self.model = None
        
    def read(self, fn):
        self.filePath = fn
        self.data = None
        with open(fn, 'r') as fin:
            self.data = yaml.load(fin, Loader=yaml.SafeLoader)
        if self.data is None:
            return self.data
        return self.data

    def getModel(self):
        self.model = None
        if self.data is None:
            return self.model
        return self.toModel()

    def convComponent(self, cdata, isInstance=False):
        logger.info(f'convComponent top {cdata}')
        comp = None
        if type(cdata) == type({}):
            if len(cdata) == 1:
                for k1, v1 in cdata.items():
                    logger.info(f'Convert component {k1}')
                    comp = self.convComponentM(k1, v1, isInstance)
                    break
            else:
                logger.error(f'component as a map with more than one entries')
        elif type(cdata) == type(''):
            k1 = cdata
            logger.info(f'Convert component scalar {k1}')
            comp = self.convComponentS(k1, isInstance)
        return comp
    
    def convComponentS(self, k, isInstance):
        re1 = re.compile('(.*)[(.*)]{(.*)}')
        re2 = re.compile('(.*){(.*)}')
        component = None
        name, ctype, params = '', '', {}
        #
        mg1 = re1.match(k)
        if mg1:
            name, ctype, params = mg1.groups()
        else:
            mg2 = re2.match(k)
            if mg2:
                name, ctype = mg2.groups()
        if name == '':
            logger.error(f'Cannot parse component information from "{k}"')
            return
        #
        if isInstance:
            component = ComponentInstance(name, ctype, **params)
        else:
            component = ComponentType(name, ctype, **params)
        return component
    
    def convComponentM(self, k, v, isInstance):
        component = self.convComponentS(k, isInstance)
        #
        if component != None:
            for sub in v:
                csub = self.convComponent(sub)
                if csub != None:
                    component.addChild(csub)
        return component
    
    def toModel(self):
        self.model = Model()
        if self.data is None:
            return self.model
        keys = self.data.keys()
        for key in keys:
            section = self.data[key]
            if key == 'model':
                self.model.setModel(self.convComponent(self.data[key], True) )
            elif key == 'components':
                components = []
                for cdata in section:
                    c = self.convComponent(cdata, False)
                    components.append(c)
                self.model.setComponents(components)
            elif key == 'header':
                self.model.setHeader(copy.copy(section) )
            elif key == 'properties':
                self.model.setProperties(copy.copy(section) )
            else:
                logger.warning(f'Unknown section {key}')
        return self.model
    
