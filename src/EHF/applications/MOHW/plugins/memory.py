import ctypes
from EHF.core import win32types

from EHF.applications.MOHW import datastruct

from EHF.plugins.common import memory
from EHF.libs.ehfmemory import scanner

from EHF.libs import ehfmaths
from EHF.libs.ehfmaths import types as ehfmaths_types


def _round(val):
    if val < 0.0001:
        return "0.0"
    elif val > 9999.0:
        return "inf"
    return "%.4f"%val


class MOHWScannerPlugin(memory.MemoryScannerPlugin):
    def initialise(self):
        self.scn = scanner.MemoryScanner(self._appAttr["ProcessHelper"].hProcess,
                                         self._appAttr["AppInfo"].targetMemStart,
                                         self._appAttr["AppInfo"].targetMemSize,
                                         "EHF.applications.MOHW.config.PatternFinderRepo")
        
    def _run(self):
        self.scn.run()
        if self.scn.values:
            for k,v in self.scn.values.items():
                self._appAttr["AppInfo"].primaryVars[k] = v


class MOHWMemReaderPlugin(memory.MemoryReaderPlugin):
    
    """
    This plugin is able to trace the references from object to object.
    
    The similar concept can be found from various BF3 hacks from UC
    forum such as bonetracer (object->object->......)
    
    Register a series of "chains" (lists) of TracingEntities. 
    """
    
    def initialise(self):
        self.hasInitialised = False
        
    def delayedInit(self):
        if self.hasInitialised:
            return
        
        # TODO: [IMPORTANT] there are variable addresses that must be computed per-frame!! 
        _appInfo = self._appAttr["AppInfo"]
        self.gameTimeAddress = _appInfo.primaryVars["GameTime"]
        self.clientGameContext = _appInfo.primaryVars["ClientGameContext"]
        self.gameRenderer = _appInfo.primaryVars["GameRenderer"]
        
        self.clientPlayerManager = 0x0
        
        self.localPlayerAddress = 0x0
        self.localPlayerTeamId = 0x0
        
        # player entities
        self.ptrArrayClientPlayer = datastruct.PtrArrayClientSoldier()
        self.eastlVectorClientPlayers = 0x0
        self.ptrArrayClientPlayerAddress = 0x0
        self.ptrArrayClientPlayerLastAddress = 0x0
        self.playerCount = 0
        
        self.hasInitialised = True
    
    def _run(self):
        self.delayedInit()
        
        _vars = self._appAttr["AppInfo"].vars
        _prmVars = self._appAttr["AppInfo"].primaryVars
        
        mr = self._appAttr["MemoryReader"]
        
        # game time (tick count), working..
        _ptr = win32types.DWORD()
        mr._rpm(self.gameTimeAddress, _ptr, 4)
        _vars["GameTime"] = _ptr.value
        self._appAttr["AppInfo"].displayTextList.append( (0, "%s"%_ptr.value ) )
        
        # -------------- get the client player manager from context -----------------
        _ptr = win32types.DWORD()
        mr._rpm(self.clientGameContext+0x8, _ptr, 4)
        self.clientPlayerManager = _ptr.value
        # ===========================================================================
        
        # -------------- get the vector object that holds ptrs -----------------------
        # [IMPORTANT]: this vector object is stored directly into the player manager
        # rather than a pointer!!!
        self.eastlVectorClientPlayers = self.clientPlayerManager+0x98
        # ============================================================================
        
        # -------------- get the player count and array address -----------------------
        _ptr = win32types.DWORD()
        mr._rpm(self.eastlVectorClientPlayers, _ptr, 4)
        self.ptrArrayClientPlayerAddress = _ptr.value
        _ptr = win32types.DWORD()
        mr._rpm(self.eastlVectorClientPlayers+0x4, _ptr, 4)
        self.ptrArrayClientPlayerLastAddress = _ptr.value
        self.playerCount = (self.ptrArrayClientPlayerLastAddress - self.ptrArrayClientPlayerAddress) / 4 
        # ===========================================================================
        
        # -------------- get the array of client player ptrs -----------------
        mr._rpm(self.ptrArrayClientPlayerAddress, self.ptrArrayClientPlayer, datastruct.MAXPLAYER * 4)
        # ===========================================================================
        
        # -------------- get local player (to differentiate enemy from teammate) ----------------
        _ptr = win32types.DWORD()
        mr._rpm(self.clientPlayerManager+0xB8, _ptr, 4)
        self.localPlayerAddress = _ptr.value
        if self.localPlayerAddress:
            _ptr = win32types.DWORD()
            mr._rpm(self.localPlayerAddress+0x38C, _ptr, 4)
            self.localPlayerTeamId = _ptr.value
            _vars["localPlayerTeamId"] = self.localPlayerTeamId
            _vars["localPlayerAddress"] = self.localPlayerAddress
        # =======================================================================================
        
        # -------------- get view projection matrix ------------------
        linearTransform = ehfmaths.CameraTransform()
        mr._rpm(self.gameRenderer+0xE10, linearTransform, 64) # was 4E0
        # forward vector
        forward = linearTransform.getForwardVect3()
        # up vector
        up = linearTransform.getUpVec3()
        # right vector
        right = linearTransform.getRightVec3().scalar_mul(-1)
        # trans vector
        viewOrigin = linearTransform.getTransVect3()
        _vars["rightVec"] = right
        _vars["upVec"] = up
        _vars["forwardVec"] = forward
        _vars["viewAxisX"] = _vars["rightVec"]
        _vars["viewAxisY"] = _vars["upVec"]
        _vars["viewAxisZ"] = _vars["forwardVec"]
        _vars["viewOrigin"] = viewOrigin
        # ============================================================

        # -------------- get fovX/fovH, fovY/fovV (fovX >> fovY!) ---------------
        _memValue = win32types.c_float()
        mr._rpm(self.gameRenderer+0x48+0x50, _memValue, 4)
        fovY = _memValue.value
        _memValue = win32types.c_float()
        mr._rpm(self.gameRenderer+0x250, _memValue, 4)
        fovX = _memValue.value
                                                                                    
        _memValue = win32types.c_float()
        mr._rpm(self.gameRenderer+0x54+0x50, _memValue, 4)
        zf = _memValue.value
        _memValue = win32types.c_float()
        mr._rpm(self.gameRenderer+0x50+0x50, _memValue, 4)
        zn = _memValue.value
        
        _vars["fov_x"] = fovX
        _vars["fov_y"] = fovY
        _vars["zn"] = zn
        _vars["zf"] = zf
        # ============================================================


        # check if it's in the dry-run mode - in this mode all the soldier
        # data are pre-generated mock-ups
        if self._application._dryRun:
            for idx in range( len(datastruct.mockSimplePlayerArgs) ):
                datastruct.setPlayerMockAttr( _vars["players"][idx], datastruct.mockSimplePlayerArgs[idx] ) 
            self._appAttr["AppInfo"].displayTextList.append((0, "Dry-run mode"))
            return

        # TODO: [IMPORTANT] forget about the MAXPLAYER constant, compute the player count on the fly!!!
        count = 0
        for idx in range(self.playerCount):
            _vars["players"][idx].initialise()
            
            # get each client player object's address
            clientPlayer = self.ptrArrayClientPlayer.arr[idx]
            if not clientPlayer:
                continue
            
            playerName = ''
            playerTeamId = 0x0
            clientSoldierEntity = 0x0
            clientSoldierEntity_sub4 = 0x0
            clientSoldierPosition = ehfmaths.VECTOR()
            
            # ----------------- get name -------------------
            # check if the string object is invalid
            _ptr = win32types.DWORD()
            mr._rpm(clientPlayer+0x10, _ptr, 4)
            #if not _ptr.value:
            #    continue
            # read c char array from the string object
            _string = ctypes.create_string_buffer(16)
            mr._rpm(_ptr.value, _string, 16)
            #if not len(_string.value):
            #    continue
            playerName = _string.value
            _ptr = win32types.DWORD()
            mr._rpm(clientPlayer+0x38C, _ptr, 4)
            playerTeamId = _ptr.value
            # ==============================================
            
            # --------------- get client solder entity ---------------------
            _weakptr = win32types.DWORD()
            _weakptr_sub4 = win32types.DWORD()
            # this seems to be some "ghost" soldier entity, it will be a valid
            # ptr as soon as the player dies
            mr._rpm(clientPlayer+0x430, _weakptr, 4)
            # this seems to be the in-battle soldier entity!
            mr._rpm(clientPlayer+0x430-0x4, _weakptr_sub4, 4)
            clientSoldierEntity = _weakptr.value
            clientSoldierEntity_sub4 = _weakptr_sub4.value
            # ==============================================================
            
            # --------------- get client soldider position ! ------------------
            if clientSoldierEntity_sub4:
                _ptr = win32types.DWORD()
                mr._rpm(clientSoldierEntity_sub4, _ptr, 4)
                cse = _ptr.value
                mr._rpm(cse+0x4DC, clientSoldierPosition, 12)
            # ==================================================================
            
            _vars["players"][idx].setPosition(clientSoldierPosition)
            _vars["players"][idx].setTeamId(playerTeamId)
            _vars["players"][idx].setAddress(clientPlayer)

            if clientPlayer == self.localPlayerAddress:
                _vars["viewOrigin"] = clientSoldierPosition.toPyVector3() 

            count += 1
        self._appAttr["AppInfo"].displayTextList.append(  
                                                        (0, "player count: %d, total: %d" % (count, self.playerCount))  
                                                        )
        

