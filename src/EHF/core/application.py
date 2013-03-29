"""
Application is the place holder of functionalities.

It's the mount point for various plugins and organize for their collaborations. 

The instance of application is also the repository of all the data attributes. Plugin reads and/or writes to
the attributes repo to achieve data sharing.  
"""
from pprint import pprint as pp

import time
import threading

from EHF.libs import ehfmodule as module
from EHF import EHFError

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

PostExecutionPluginType = 0x1
PreExecutionPluginType = 0x3
PerFrameDataPluginType = 0x2
PerFrameDrawingPluginType = 0x4
DebugPluginType = 0x1337



class BaseApplication(object):
    
    """
    The base class of the application
    """
    
    pluginDefinitions = []
    
    # NOTE:
    # only override this attribute in a pure test/prototype application,
    # it will affect lots of things
    # if just for debug purpose, it's recommended to use the --debug or --dryRun flag!!
    isPrototypeApplication = False
    
    def __init__(self, debug=False, dryRun=False):
        """
        Application share the data with its own plugins via the _attributes.
        
        For the sub-classes that are going to define their own attributes, implement the initAttributes() method
        that is called before the plugin registery (which allow the sub-classes to define the preliminary attributes
        required by the plugins)
        
        @param debug: is a flag to turn on debug features (extra logging message, widget etc etc)
                      rarely used though
        @type  debug: bool
        
        @param dryRun: is a flag to turn on the dry run mode - it is a mode that no live data is used, only the mock up data;
                       the mock data is define in the per-application config.py module
                       this flag is passed from the launch script 
        @type  dryRun: bool
        """
        self._debugFlag = debug
        self._dryRun = dryRun
        
        self._terminate = False # stop executing by brutal force
        
        self._attributes = {
                            "FPS"  : 60.0,
                            "Lock" : threading.Lock(),
                           }
        self.initAttributes()
        self._pluginRegistry = {
                                PostExecutionPluginType: [],
                                PreExecutionPluginType : [],
                                PerFrameDataPluginType : [],
                                PerFrameDrawingPluginType:[],
                                DebugPluginType        : [],
                               }
        self.registerPlugins()
    
    
    def initAttributes(self):
        pass 
    
    
    def getAttribute(self, key, defaultValue=None):
        return self._attributes.get(key, defaultValue)
    
    
    def getAttributeRepo(self):
        return self._attributes
    
    
    def getPlugins(self):
        result = []
        for k, v in self._pluginRegistry.items():
            result.extend( v )
        return result
    
    
    def setAttribute(self, key, value):
        self._attributes[key] = value


    def registerPlugins(self):
        if self.pluginDefinitions:
            for pluginModulePath, pluginClassName in self.pluginDefinitions:
                self._registerPlugin(pluginModulePath, pluginClassName)
    
    
    def _registerPlugin(self, pluginModulePath, pluginClassName):
        pluginClass = module.getClass(pluginModulePath, pluginClassName)
        if not pluginClass:
            raise EHFError, "ERROR! can not resolve plugin class from:\n%s\n%s" % (pluginModulePath, pluginClassName)
        for _attr in pluginClass.requirements:
            if _attr not in self._attributes:
                raise EHFError, "ERROR! plugin\n%s\nrequires [%s] but can not find it from the application"%(pluginClass, _attr)
        for _attr in pluginClass.contributions:
            if _attr in self._attributes:
                raise EHFError, "ERROR! plugin\n%s\nwill override attribute [%s]"%(pluginClass, _attr)
            self.setAttribute(_attr, None)
        pluginInstance = pluginClass(self)
        self._pluginRegistry[pluginClass.uid].append(pluginInstance)
        logger.info(" + Successfully registered plugin: %s" % pluginClass)
        
    
    def terminate(self):
        self._terminate = True

    
    def execute(self):
        raise NotImplementedError, "You must implement execute() method in the derived classes"