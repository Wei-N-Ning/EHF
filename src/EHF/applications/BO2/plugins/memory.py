from EHF.plugins.common import memory
from EHF.libs.ehfmemory import scanner

from EHF.applications.BO2 import datastruct

import random

class BO2ScannerPlugin(memory.MemoryScannerPlugin):
    def initialise(self):
        self.scn = scanner.MemoryScanner(self._appAttr["ProcessHelper"].hProcess,
                                         self._appAttr["AppInfo"].targetMemStart,
                                         self._appAttr["AppInfo"].targetMemSize,
                                         "EHF.applications.BO2.config.PatternFinderRepo")
        
    def _run(self):
        self.scn.run()
        if self.scn.values:
            for k,v in self.scn.values.items():
                self._appAttr["AppInfo"].primaryVars[k] = v


class BO2MemReaderPlugin(memory.MemoryReaderPlugin):
    def initialise(self):
        """
        instantiate the data structures to be read
        
        note that this plugin uses a "delayed" initialization method
        because at the time of registering plugin, scanner has not 
        yet populated all the addresses!!
        """
        self.hasInitialised = False
        
    def delayedInit(self):
        if self.hasInitialised:
            return
        
        _appInfo = self._appAttr["AppInfo"]
        
        self.entityArrayAddress = _appInfo.primaryVars["Entity"]
        
        self.entityArray = datastruct.EntityArray()
        
        self.hasInitialised = True
    
    def _run(self):
        self.delayedInit()
        
        _vars = self._appAttr["AppInfo"].vars
        mr = self._appAttr["MemoryReader"]
        
        mr._rpm(self.entityArrayAddress,     self.entityArray,     datastruct.sizeof(self.entityArray))
        
        #
        self._appAttr["AppInfo"].displayTextList.append((0, "MemReaderRunning!"))
        self._appAttr["AppInfo"].displayTextList.append((0, "%d" % datastruct.PLAYERMAX))
        #
        
        for i in range(datastruct.PLAYERMAX):
            _vars["players"][i].setValueFromEntity(self.entityArray.arr[i])
            if i == 0:
                _vars["viewOrigin"] = _vars["players"][0].pos