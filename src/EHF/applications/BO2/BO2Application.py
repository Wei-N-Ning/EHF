from EHF.applications import d3dapplication
from EHF.applications import consoleapplication
from EHF.applications.BO2 import config
from EHF.libs.ehfmemory import scanner

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class BO2Application(d3dapplication.D3DApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.BO2.plugins.memory", "BO2ScannerPlugin"),
                         ("EHF.applications.BO2.plugins.memory", "BO2MemReaderPlugin"),
                         #("EHF.applications.plugins.keymouseinput", "KeyMouseInputPlugin"),
                         #("EHF.applications.plugins.keymouseinput", "SimpleMouseMovePlugin"),
                         ("EHF.plugins.common.drawing", "SimpleCrosshairPlugin"),
                         ("EHF.plugins.common.drawing", "SimpleTextPlugin"),
                         ("EHF.applications.BO2.plugins.esp", "EspPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.BO2AppInfo()
        self._attributes["AppInfo"] = appInfo
        
        
    def _initEnvInfo(self):
        envInfo = config.BO2EnvInfo()
        self._attributes["EnvInfo"] = envInfo
        
    def _cleanUp(self):
        # clean up per-frame text list
        self._attributes["AppInfo"].displayTextList = []


class BO2ConsoleApplication(consoleapplication.ConsoleApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.BO2.plugins.memory", "BO2ScannerPlugin"),
                         ("EHF.applications.BO2.plugins.memory", "BO2MemReaderPlugin"),
                         ("EHF.applications.plugins.interacter", "SimpleInteracterPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.BO2AppInfo()
        self._attributes["AppInfo"] = appInfo
        
        
    def _initEnvInfo(self):
        envInfo = config.BO2EnvInfo()
        self._attributes["EnvInfo"] = envInfo
