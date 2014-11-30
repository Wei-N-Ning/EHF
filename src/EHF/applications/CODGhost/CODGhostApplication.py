from EHF.applications import consoleapplication
from EHF.applications.CODGhost import config

from EHF.libs.ehfmemory import reader


class CODGhostConsoleApplication(consoleapplication.ConsoleApplication):
    
    bitcount = 64
    
    pluginDefinitions = [
                         #("EHF.applications.plugins.interacter", "SimpleInteracterPlugin"),
                         ("EHF.applications.CODGhost.plugins.scanner", "CODGhostScannerPlugin"),
                         ("EHF.applications.CODGhost.plugins.serialization", "CODGhostAppInfoSerializationPlugin")
                        ]
    
    def _initAppInfo(self):
        self._attributes["AppInfo"] = config.CODGhostAppInfo()
        
    def _initEnvInfo(self):
        self._attributes["EnvInfo"] = config.CODGhostEnvInfo

    def _overrideAppInfo(self):
        self._attributes["MemoryReader"] = reader.MemoryReader(self._attributes["ProcessHelper"].hProcess, is64Bit=True)