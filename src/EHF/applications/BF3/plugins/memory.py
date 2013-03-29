import ctypes
from EHF.core import win32types

from EHF.applications.BF3 import datastruct

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


class BF3ScannerPlugin(memory.MemoryScannerPlugin):
    def initialise(self):
        self.scn = scanner.MemoryScanner(self._appAttr["ProcessHelper"].hProcess,
                                         self._appAttr["AppInfo"].targetMemStart,
                                         self._appAttr["AppInfo"].targetMemSize,
                                         "EHF.applications.BF3.config.PatternFinderRepo")
        
    def _run(self):
        self.scn.run()
        if self.scn.values:
            for k,v in self.scn.values.items():
                self._appAttr["AppInfo"].primaryVars[k] = v


class BF3MemReaderPlugin(memory.MemoryReaderPlugin):
    
    """
    This plugin is able to trace the references from object to object.
    
    The similar concept can be found from various BF3 hacks from UC
    forum such as bonetracer (object->object->......)
    
    Register a series of "chains" (lists) of TracingEntities. 
    
    NOTE: March 2013 patch changed the ClientSoldierEntity layout:
    ClientSoldierEntity:
    getActiveAnimatable() is at index 91.
    m_predictedController is at 0x248
    m_soldierWeaponsComponent is at 0x35C
    
    AimAssist:
    Add 8 bytes of padding between the modifiable x and y angles.
    """
    
    def initialise(self):
        self.hasInitialised = False
        
    def delayedInit(self):
        if self.hasInitialised:
            return
        
        _appInfo = self._appAttr["AppInfo"]
        
        # the fundamental addresses - these are supposed to be static
        self.gameTimeAddress = _appInfo.primaryVars["GameTime"]
        self.clientGameContext = _appInfo.primaryVars["ClientGameContext"]
        self.gameRenderer = _appInfo.primaryVars["GameRenderer"]
        
        # player iteration
        self.clientPlayerManager = 0x0
        
        # local player address (to avoid drawing twice) and team id (team color)
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
        
        # get primaryVars and vars repository
        _vars = self._appAttr["AppInfo"].vars
        _prmVars = self._appAttr["AppInfo"].primaryVars
        
        # get a reference to the memory reader
        mr = self._appAttr["MemoryReader"]
        
        # game time (tick count)
        _ptr = win32types.DWORD()
        mr._rpm(self.gameTimeAddress, _ptr, 4)
        _vars["GameTime"] = _ptr.value
        self._appAttr["AppInfo"].displayTextList.append( (0, "%s"%_ptr.value ) )
        
        # -------------- get the client player manager from context -----------------
        _ptr = win32types.DWORD()
        mr._rpm(self.clientGameContext+0x30, _ptr, 4)
        self.clientPlayerManager = _ptr.value
        # ===========================================================================
        
        # ----------- get the eastl vector object that holds ptrs --------------------
        # [IMPORTANT]: this vector object is stored directly into the player manager
        # rather than a pointer!!!
        # [IMPORTANT]: the class listing from UC is out-dated, it said 0x98
        self.eastlVectorClientPlayers = self.clientPlayerManager+0x9C
        # ============================================================================
        
        # -------------- get the player count and array address ----------------------------------------
        _ptr = win32types.DWORD()
        mr._rpm(self.eastlVectorClientPlayers, _ptr, 4)
        self.ptrArrayClientPlayerAddress = _ptr.value
        _ptr = win32types.DWORD()
        mr._rpm(self.eastlVectorClientPlayers+0x4, _ptr, 4)
        self.ptrArrayClientPlayerLastAddress = _ptr.value
        self.playerCount = (self.ptrArrayClientPlayerLastAddress - self.ptrArrayClientPlayerAddress) / 4 
        # ==============================================================================================
        
        # -------------- get the array of client player ptrs, NOTE THE DATA SIZE------------------------
        mr._rpm(self.ptrArrayClientPlayerAddress, self.ptrArrayClientPlayer, datastruct.MAXPLAYER * 4)
        # ==============================================================================================
        
        # -------------- get local player (to differentiate enemy from team mate) ----------------------
        _ptr = win32types.DWORD()
        mr._rpm(self.clientPlayerManager+0xBC, _ptr, 4)
        self.localPlayerAddress = _ptr.value
        if self.localPlayerAddress:
            _ptr = win32types.DWORD()
            mr._rpm(self.localPlayerAddress+0x31C, _ptr, 4)
            self.localPlayerTeamId = _ptr.value
            _vars["localPlayerTeamId"] = self.localPlayerTeamId
            _vars["localPlayerAddress"] = self.localPlayerAddress
            
        # ==============================================================================================
        
        # -------------- get view projection matrix ------------------
        linearTransform = ehfmaths.CameraTransform()
        mr._rpm(self.gameRenderer+0xDE0, linearTransform, 64)
        # forward vector
        forward = linearTransform.getForwardVect3()
        # up vector
        up = linearTransform.getUpVec3()
        # right vector (the original VECTOR is actual LEFT-pointing!!!)
        right = linearTransform.getRightVec3().scalar_mul(-1)
        # trans vector
        viewOrigin = linearTransform.getTransVect3()
        #    forward ==> right                 ; right = old_forward
        #    right ==> back ==> forward inverse; forward = inverse old_right
        #    up ==> up                         ; up = old_up
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
        mr._rpm(self.gameRenderer+0x1F0+0x50, _memValue, 4)
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
            for idx in range(1):
                _vars["players"][idx].setPosition(ehfmaths_types.VECTOR4(56.0, 34.0, 100.0, 1.0))
                _vars["players"][idx].setTeamId(1)
                _vars["players"][idx].setAddress(0x1337)
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
            replicatedController = 0x0
            clientSoldierPosition = ehfmaths.VECTOR()
            poseType = 0x0
            yaw = 0.0
            
            # ----------------- get name -------------------
            # check if the string object is invalid
            _ptr = win32types.DWORD()
            mr._rpm(clientPlayer+0x10, _ptr, 4)
            #if not _ptr.value:
            #    continue
            # read c char array from the string object
            _string = ctypes.create_string_buffer(16)
            mr._rpm(_ptr.value, _string, 16)
            #if not len(_string.value                                                                                                ):
            #    continue
            playerName = _string.value
            _ptr = win32types.DWORD()
            mr._rpm(clientPlayer+0x31C, _ptr, 4)
            playerTeamId = _ptr.value
            # ==============================================
            
            # --------------- get client solder entity ---------------------
            _weakptr = win32types.DWORD()
            _weakptr_sub4 = win32types.DWORD()
            # this seems to be some "ghost" soldier entity, it will be a valid
            # ptr as soon as the player dies
            # [IMPORTANT]: the class listing from UC is out-dated! it said 3BC
            mr._rpm(clientPlayer+0x3C4, _weakptr, 4)
            # this seems to be the in-battle soldier entity!
            mr._rpm(clientPlayer+0x3C4-0x4, _weakptr_sub4, 4)
            clientSoldierEntity = _weakptr.value
            clientSoldierEntity_sub4 = _weakptr_sub4.value
            # ==============================================================
            
            # --------------- get client soldider position ! ------------------
            if clientSoldierEntity_sub4:
                _ptr = win32types.DWORD()
                mr._rpm(clientSoldierEntity_sub4, _ptr, 4)
                cse = _ptr.value
                
                # get replicatedController
                _ptr = win32types.DWORD()
                mr._rpm(cse+0x24C, _ptr, 4) # Mar 2013 patch, 0x23C -> 0x24C
                replicatedController = _ptr.value
                
                # get position vec3 (vec4 in the memory) object+0x10
                mr._rpm(replicatedController+0x10, clientSoldierPosition, 12)
                # get the pose type object+0x5c
#                _varible = win32types.DWORD()
#                mr._rpm(replicatedController+0x5C, _varible, 4)
#                poseType = _varible.value
                # get the yaw value, read from CharacterPhysicsEntity: soldierEntity+0x74
#                _ptr = win32types.DWORD()
#                mr._rpm(cse+0x74, _ptr, 4)
#                characterPhysicsEntity = _ptr.value
#                _variable = win32types.c_float()
#                if characterPhysicsEntity > 10000:
#                    mr._rpm(characterPhysicsEntity+0x38, _varible, 4)
#                    yaw = _varible.value
            # ==================================================================
            
            _vars["players"][idx].setPosition(clientSoldierPosition)
            _vars["players"][idx].setTeamId(playerTeamId)
            _vars["players"][idx].setAddress(clientPlayer)
            _vars["players"][idx].setPoseType(poseType)
            _vars["players"][idx].setYaw(yaw)
            
            if clientPlayer == self.localPlayerAddress:
                _vars["viewOrigin"] = clientSoldierPosition.toPyVector3() 
                _vars["viewOrigingPoseType"] = poseType
                _vars["viewOriginYaw"] = yaw
                
                # for debug purpose:
#                _prmVars["pc"] = self.localPlayerAddress
#                _prmVars["pcRc"] = replicatedController
#                _prmVars["pcCse"] = cse
                
            count += 1
        self._appAttr["AppInfo"].displayTextList.append(  
                                                        (0, "player count: %d, total: %d" % (count, self.playerCount))  
                                                        )