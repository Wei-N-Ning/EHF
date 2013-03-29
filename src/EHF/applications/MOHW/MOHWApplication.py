from EHF.applications import d3dapplication
from EHF.applications import consoleapplication
from EHF.applications.MOHW import config

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class MOHWApplication(d3dapplication.D3DApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.MOHW.plugins.memory", "MOHWScannerPlugin"),
                         ("EHF.applications.MOHW.plugins.memory", "MOHWMemReaderPlugin"),
                         #("EHF.applications.plugins.keymouseinput", "KeyMouseInputPlugin"),
                         #("EHF.applications.plugins.keymouseinput", "SimpleMouseMovePlugin"),
                         ("EHF.plugins.common.drawing", "SimpleCrosshairPlugin"),
                         ("EHF.applications.MOHW.plugins.esp", "EspPlugin"),
                         ("EHF.plugins.common.drawing", "SimpleTextPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.MOHWAppInfo()
        
        # application-specified attributes
        # this flag will block or continue the execution of plugins
        # in practice,
        # it checks if the game level is valid as well as the tick count (if tick == 0 and prev_tick != 0)
        # the false status of this flag indicates all the readers/esps need to wait for another valid
        # game level is loaded
        self._attributes["requireScannerUpdate"] = False
        
        self._attributes["AppInfo"] = appInfo
        
    def _initEnvInfo(self):
        envInfo = config.MOHWEnvInfo()
        self._attributes["EnvInfo"] = envInfo
        

# ------------------------------------------------------------------


class MOHWConsoleApplication(consoleapplication.ConsoleApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.MOHW.plugins.memory", "MOHWScannerPlugin"),
                         ("EHF.applications.MOHW.plugins.memory", "MOHWMemReaderPlugin"),
                         ("EHF.applications.plugins.interacter", "SimpleInteracterPlugin")
                        ]
    
    def _initAppInfo(self):
        appInfo = config.MOHWAppInfo()
        self._attributes["AppInfo"] = appInfo
        
        
    def _initEnvInfo(self):
        envInfo = config.MOHWEnvInfo()
        self._attributes["EnvInfo"] = envInfo
