from ctypes import c_int, c_float, sizeof

from EHF.core import entity
from EHF.libs.ehfmemory import patternfinder
from EHF.libs import ehfmaths

from EHF.applications.BO2 import profiles
from EHF.applications.BO2 import datastruct


class BO2AppInfo(entity.AppInfo):
    def override(self):
        self.appName = "Black Ops 2 ehf application"
        self.isDryRun = False
        self.isProfiling = False
        self.targetAppName = "t6mp.exe"
        self.targetAppWindowClass = "CoDBlackOps"
        self.targetMemStart = 0x00401000
        self.targetMemSize =  0x00F00000
        self.keyMouseInputState = \
        {
         # hold type
         "LMB":entity.KeyMouse("LMB", 0x01, 1, False),
         "RMB":entity.KeyMouse("RMB", 0x02, 1, False),
         
         # toggle type
         "INSERT":entity.KeyMouse("INSERT", 0x2D, 0, False),
        }
        
        # application-only attributes!
        self.vars = {
                     "refdef_width"   :  0,
                     "refdef_height"  :  0,
                     "fov_x"          :  0.0,
                     "fov_y"          :  0.0,
                     "viewOrigin"     :  ehfmaths.VECTOR(),
                     "viewAxis"       :  [ehfmaths.VECTOR]*3,
                     "viewAngle"      :  ehfmaths.VECTOR(),
                     "players"        :  [Player() for i in range(datastruct.PLAYERMAX)],
                     }
        

class BO2EnvInfo(entity.EnvInfo):
    def override(self):
        self.crossHairStyle = 0 # +
        self.crossHairSize = 8
        self.crossHairLineWidth = 2


class ClientInfo(object):
    def __init__(self):
        self.name = ""
        self.team = 0
        self.clientNum = 0


class Player(object):
   
    def __init__(self):
        self.pos = None
        self.pitch = 0.0
        self.yaw = 0.0

    def setValueFromEntity(self, entity):
        self.pos = entity.position
        self.pitch = entity.pitch
        self.yaw = entity.yaw


class PatternFinderRepo(object):
    def __init__(self):
        self.repo = [
                     
            patternfinder.PatternFinder(
                label          = "Entity",
                patternExpected="8B 8E 34 2A 00 00 69 C9 1C 03 00 00 6A 01 50 81 C1 C0 7C 10 02 51 E8 C0 33 1E 00 83 C4 14",
                patternMask    ="FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF 00 00 00 00 00 FF FF FF",
                #                1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x11, c_int, sizeof(c_int) ) ]
            ),

        ]   
    
    def getRepo(self):
        return self.repo    
