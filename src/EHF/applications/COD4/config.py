from ctypes import c_int, c_float, sizeof

from EHF.core import entity
from EHF.libs.ehfmemory import patternfinder
from EHF.libs import ehfmaths

from EHF.applications.COD4 import profiles
from EHF.applications.COD4 import datastruct


class Cod4AppInfo(entity.AppInfo):
    def override(self):
        self.appName = "cod4 ehf application"
        self.isDryRun = False
        self.isProfiling = False
        self.targetAppName = "iw3mp.exe"
        self.targetAppWindowClass = "CoD4"
        self.targetMemStart = 0x00401000
        self.targetMemSize =  0x00700000
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
                     "players"        : [Player() for i in range(datastruct.PLAYERMAX)],
                     }
        # the window-drawing mode, options are: overlay and standard
        self.windowMode = "standard"
        # these values must be set if the windowMode is "standard"
        self.stdOriginX = 200
        self.stdOriginY = 200
        self.stdResolutionX = 320
        self.stdResolutionY = 200
        

class Cod4EnvInfo(entity.EnvInfo):
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
        self.valid = 1
        self.pos = None
        self.newpos = None
        self.oldpos = None
        #self.prev_pos = None
        #self.pitch = 0
        #self.yaw = 0
        #self.roll = 0
        #self.client_num = 0
        self.type = 0
        #self.pose = 0
        #self.shooting = 0
        #self.zoomed = 0
        #self.weapon_num = 0
        self.alive = 0
        #self.enemy = False

        self.name = ""
        self.team = 0
        #self.perk = 0
        
        #self.color_esp = 0
        #self.color_map = 0
        #self.motion = ehfmaths.VECTOR(0, 0, 0)               # motion vector of the player, in game units per second
        
        #self.entity = None
        #self.client_info = None
        
        #self.aimbot = True                      # this entity is eligible for aimbot

    def setValueFromEnCl(self, entity, clientinfo):
        #self.entity = cod7_entity
        #self.client_info = cod7_clientinfo
        #self.valid = cod7_entity.valid
        #self.valid = True
        #self.prev_pos = self.pos
        #self.pos = entity.location
        #self.newpos = entity.newLocation
        #self.oldpos = entity.oldLocation
        #self.pitch = cod7_entity.anglex
        #self.yaw = cod7_entity.angley
        #self.roll = cod7_entity.fRoll
        #self.client_num = cod7_entity.clientNum

        #self.shooting = cod7_entity.Shooting
        #self.zoomed = cod7_entity.Zoomed
        #self.weapon_num = cod7_entity.weapon
        #self.pose = entity.pose
        #self.perk = 0
        
        self.alive = entity.isAlive
        self.valid = True
        self.type = entity.entityType
        self.pos = entity.location
        self.newpos = entity.newLocation
        self.oldpos = entity.oldLocation
        #p_str = datastruct.cast(datastruct.pointer(clientinfo.Name), datastruct.c_char_p)
        #self.name = 
        self.team = clientinfo.Team



class PatternFinderRepo(object):
    def __init__(self):
        self.repo = [
                     
            patternfinder.PatternFinder(
                label          = "CGS",
                niceName       = '',
                patternExpected="8B 5D 08 56 57 68 00 00 00 00 33 FF 57 68 00 00 00 00 ",
                patternMask    ="FF FF FF FF FF FF 00 00 00 00 FF FF FF FF 00 00 00 00 ",
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x0E, c_int, sizeof(c_int) ) ],
                addressExpected=0x0043FB2A ),
                     
            patternfinder.PatternFinder(
                label          = "CG",
                niceName       = '',
                patternExpected="8B 5D 08 56 57 68 00 00 00 00 33 FF 57 68 00 00 00 00 ",
                patternMask    ="FF FF FF FF FF FF 00 00 00 00 FF FF FF FF 00 00 00 00 ",
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x21, c_int, sizeof(c_int) ) ],
                addressExpected=0x0043FB2A),
            
            patternfinder.PatternFinderFollower(
                label = "RefDef",
                niceName = "RefDef",
                isPointer = False,
                baseVariableName = "CG",
                valueOffsets = [0x492c8, None, None]),
            
            patternfinder.PatternFinder(
                label          = "Entity",
                niceName       = '',
                patternExpected="8B 5D 08 56 57 68 00 00 00 00 33 FF 57 68 00 00 00 00 ",
                patternMask    ="FF FF FF FF FF FF 00 00 00 00 FF FF FF FF 00 00 00 00 ",
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x5D, c_int, sizeof(c_int) ) ],
                addressExpected=0x0043FB2A ),

            patternfinder.PatternFinder(
                label          = "ClientInfo",
                niceName       = '',
                patternExpected="83 EC 20 53 8B 5C 24 28 D9 43 0C 56 8B 35 00 00 00 00",
                patternMask    ="FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 ",
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x27, c_int, sizeof(c_int) ) ],
                addressExpected=0x00431F20 ),
            
            # IsInGame is 0 if not in a round; or some large value like 0x77035C if in a round
            patternfinder.PatternFinder(
                label          = "IsInGame",
                niceName       = '',
                patternExpected="8B 3D DC D2 74 00 83 C7 20 F6 07 18 89 7C 24 18 0F 84 DD 01 00 00 8B B4 24 64 01 00 00 8B D6 C1 E2 04",
                patternMask    ="FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF",
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x02, c_int, sizeof(c_int) ) ],
                addressExpected=0x00431F20 ),

        ]   
    
    def getRepo(self):
        return self.repo    
