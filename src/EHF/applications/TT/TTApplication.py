from EHF.applications import d3dapplication
from EHF.applications import consoleapplication
from EHF.applications.TT import config


class TTApplication(d3dapplication.D3DApplication):
    
    pluginDefinitions = [
                         ("EHF.applications.TT.plugins.esp", "PrototypeEspPlugin")
                        ]
    
    isPrototypeApplication = True
    
    def _initAppInfo(self):
        appInfo = config.TTAppInfo()
        self._attributes["AppInfo"] = appInfo
        
    def _initEnvInfo(self):
        envInfo = config.TTEnvInfo()
        self._attributes["EnvInfo"] = envInfo
        


class TTConsoleApplication(consoleapplication.ConsoleApplication):
    
    pluginDefinitions = [
                        ]
    
    def _initAppInfo(self):
        appInfo = config.TTAppInfo()
        self._attributes["AppInfo"] = appInfo
        
        
    def _initEnvInfo(self):
        envInfo = config.TTEnvInfo()
        self._attributes["EnvInfo"] = envInfo