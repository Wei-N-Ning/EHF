from EHF.applications import d3dapplication
from EHF.applications import consoleapplication
from EHF.applications.BF3 import config

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class BF3Application(d3dapplication.D3DApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.BF3.plugins.memory", "BF3ScannerPlugin"),
                         ("EHF.applications.BF3.plugins.memory", "BF3MemReaderPlugin"),
                         #("EHF.applications.plugins.keymouseinput", "KeyMouseInputPlugin"),
                         ("EHF.plugins.common.drawing", "SimpleCrosshairPlugin"),
                         ("EHF.applications.BF3.plugins.esp", "EspPlugin"),
                         ("EHF.plugins.common.drawing", "SimpleTextPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.BF3AppInfo()
        self._attributes["AppInfo"] = appInfo
        
    def _initEnvInfo(self):
        envInfo = config.BF3EnvInfo()
        self._attributes["EnvInfo"] = envInfo
        
        
class BF3ConsoleApplication(consoleapplication.ConsoleApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.BF3.plugins.memory", "BF3ScannerPlugin"),
                         ("EHF.applications.BF3.plugins.memory", "BF3MemReaderPlugin"),
                         ("EHF.applications.plugins.interacter", "SimpleInteracterPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.BF3AppInfo()
        self._attributes["AppInfo"] = appInfo
        
    def _initEnvInfo(self):
        envInfo = config.BF3EnvInfo()
        self._attributes["EnvInfo"] = envInfo
