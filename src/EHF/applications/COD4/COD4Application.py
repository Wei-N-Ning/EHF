from EHF.applications import d3dapplication
from EHF.applications import consoleapplication
from EHF.applications.COD4 import config
from EHF.libs.ehfmemory import scanner

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class Cod4Application(d3dapplication.D3DApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.COD4.plugins.memory", "COD4ScannerPlugin"),
                         ("EHF.applications.COD4.plugins.memory", "COD4MemReaderPlugin"),
                         #("EHF.applications.plugins.keymouseinput", "KeyMouseInputPlugin"),
                         #("EHF.applications.plugins.keymouseinput", "SimpleMouseMovePlugin"),
                         ("EHF.plugins.common.drawing", "SimpleCrosshairPlugin"),
                         ("EHF.plugins.common.drawing", "SimpleTextPlugin"),
                         ("EHF.applications.COD4.plugins.esp", "EspPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.Cod4AppInfo()
        self._attributes["AppInfo"] = appInfo
        
        
    def _initEnvInfo(self):
        envInfo = config.Cod4EnvInfo()
        self._attributes["EnvInfo"] = envInfo
        
    def _cleanUp(self):
        # clean up per-frame text list
        self._attributes["AppInfo"].displayTextList = []


class Cod4ConsoleApplication(consoleapplication.ConsoleApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.COD4.plugins.memory", "COD4ScannerPlugin"),
                         ("EHF.applications.COD4.plugins.memory", "COD4MemReaderPlugin"),
                         ("EHF.applications.plugins.interacter", "SimpleInteracterPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.Cod4AppInfo()
        self._attributes["AppInfo"] = appInfo
        
        
    def _initEnvInfo(self):
        envInfo = config.Cod4EnvInfo()
        self._attributes["EnvInfo"] = envInfo
