from EHF.applications import consoleapplication
from EHF.applications import d3dapplication
from EHF.applications.BF4 import config

from EHF.libs.ehfmemory import reader

import logging
logger = logging.getLogger(__name__)


class BF4ConsoleApplication(consoleapplication.ConsoleApplication):
    
    bitcount = 64
    
    pluginDefinitions = [
                         #("EHF.applications.plugins.interacter", "SimpleInteracterPlugin"),
                         ("EHF.applications.BF4.plugins.scanner", "BF4ScannerPlugin"),
                         ("EHF.applications.BF4.plugins.serialization", "BF4AppInfoSerializationPlugin")
                        ]
    
    def _initAppInfo(self):
        self._attributes["AppInfo"] = config.BF4AppInfo()
        
    def _initEnvInfo(self):
        self._attributes["EnvInfo"] = config.BF4EnvInfo()

    def _overrideAppInfo(self):
        self._attributes["MemoryReader"] = reader.MemoryReader(self._attributes["ProcessHelper"].hProcess, is64Bit=True)
        
