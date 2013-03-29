from EHF.plugins.common import memory
from EHF.libs.ehfmemory import scanner

from EHF.applications.COD4 import datastruct

import random

class COD4ScannerPlugin(memory.MemoryScannerPlugin):
    def initialise(self):
        self.scn = scanner.MemoryScanner(self._appAttr["ProcessHelper"].hProcess,
                                         self._appAttr["AppInfo"].targetMemStart,
                                         self._appAttr["AppInfo"].targetMemSize,
                                         "EHF.applications.COD4.config.PatternFinderRepo")
        
    def _run(self):
        self.scn.run()
        if self.scn.values:
            for k,v in self.scn.values.items():
                self._appAttr["AppInfo"].primaryVars[k] = v
                #self._appAttr["AppInfo"].titleTextList.append((0, "%s: 0x%X" % (k,v)))


class COD4MemReaderPlugin(memory.MemoryReaderPlugin):
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
        self.refDefAddress = _appInfo.primaryVars["RefDef"]
        self.cgAddress = _appInfo.primaryVars["CG"]
        self.cgsAddress = _appInfo.primaryVars["CGS"]
        self.entityArrayAddress = _appInfo.primaryVars["Entity"]
        self.clientInfoArrayAddress = _appInfo.primaryVars["ClientInfo"]
        self.isInGameAddress = _appInfo.primaryVars["IsInGame"]
        
        self.refDef = datastruct.RefDef()
        self.cg = datastruct.CG()
        self.cgs = datastruct.CGS()
        self.entityArray = datastruct.EntityArray()
        self.clientInfoArray = datastruct.ClientInfoArray()
        self.isInGame = datastruct.c_int(0)
        
        self.hasInitialised = True
    
    def _run(self):
        """
        delayed init and then -
        do the reading!!

        example:
        refDefInstance = datastruct.RefDef()
        ms._rpm(ms.values["CG"]+0x492c8, refDefInstance, datastruct.sizeof(refDefInstance))
        print "0x%X"%(ms.values["CG"]+0x492c8), refDefInstance.width, refDefInstance.height
    
         "refdef_width"   :  0,
         "refdef_height"  :  0,
         "fov_x"          :  0.0,
         "fov_y"          :  0.0,
         "viewOrigin"     :  (0.0, 0.0, 0.0),
         "viewAxis"       :  (0.0, 0.0, 0.0),
         "viewAngle"      :  (0.0, 0.0, 0.0),
         "players"        : [Player() for i in range(datastruct.PLAYERMAX)],
         "clientInfos"    : [ClientInfo() for i in range(datastruct.PLAYERMAX)]
         
        """
        self.delayedInit()
        
        _vars = self._appAttr["AppInfo"].vars
        mr = self._appAttr["MemoryReader"]
        mr._rpm(self.refDefAddress,      self.refDef, datastruct.sizeof(self.refDef))
        mr._rpm(self.cgAddress,          self.cg,     datastruct.sizeof(self.cg))
        mr._rpm(self.cgsAddress,         self.cgs,    datastruct.sizeof(self.cgs))
        mr._rpm(self.entityArrayAddress,     self.entityArray,     datastruct.sizeof(self.entityArray))
        mr._rpm(self.clientInfoArrayAddress, self.clientInfoArray, datastruct.sizeof(self.clientInfoArray))
        mr._rpm(self.isInGameAddress,    self.isInGame, datastruct.sizeof(self.isInGame))
        
        _vars["refdef_width"] = self.refDef.width
        _vars["refdef_height"] = self.refDef.height
        _vars["fov_x"] = self.refDef.fov_x
        _vars["fov_y"] = self.refDef.fov_y
        _vars["viewOrigin"] = self.refDef.viewOrigin
        _vars["viewAxis"] = self.refDef.viewAxis
        _vars["viewAngle"] = self.refDef.refDefViewAngles
        
        for i in range(datastruct.PLAYERMAX):
            _vars["players"][i].setValueFromEnCl(self.entityArray.arr[i], self.clientInfoArray.arr[i])
        
        _vars["myPlayer"] = _vars["players"][0]
        _vars["myTeam"] = _vars["myPlayer"].team
        