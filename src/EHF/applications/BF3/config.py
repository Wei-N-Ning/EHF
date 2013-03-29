from ctypes import c_int, c_float, sizeof, c_uint

from EHF.applications.BF3 import datastruct
from EHF.core import entity
from EHF.libs.ehfmemory import patternfinder


class BF3AppInfo(entity.AppInfo):
    def override(self):
        self.appName = "BF3 ehf application"
        self.isDryRun = False
        self.isProfiling = False
        self.targetAppName = "Battlefield 3"
        self.targetAppWindowClass = "Battlefield 3"
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
        self.vars = {
                     "players": [datastruct.SimplePlayer() for i in range(datastruct.MAXPLAYER)],
                    }
        
        
class BF3EnvInfo(entity.EnvInfo):
    def override(self):
        self.crossHairStyle = 0 # +
        self.crossHairSize = 8
        self.crossHairLineWidth = 2
        

class PatternFinderRepo(object):
    def __init__(self):
        self.repo = [
            
#            patternfinder.PatternFinder(
#                label          = "recoilVT",
#                patternExpected="8B 10 8B C8 8B 42 04 68 76 B3 C0 01 FF D0 89 86 28 01 00 00 8B 4D 04 8B 41 0C 50 8B CF",
#                patternMask    ="FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
#                               # 1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A
#                patternMatch   ="FF",
#                valueOffsets   =[ ( 0x9, c_uint, sizeof(c_uint) ) ],
#                addressExpected=0x0 ),
            
#            patternfinder.StaticFinder(
#                label = "recoilVT",
#                address = 0x02082D18  
#                ),
            
            patternfinder.PatternFinder(
                label          = "ptrClientGameContext",
                patternExpected="18 F3 0F 11 48 1C 89 78 24 89 48 0C 89 50 10 89 78 14 89 78 20 B9 28 00 00 00 89 48 28 89 48 2C 8B 44 24 0C 56 89 46 60 8B 0D 74 FC 33 02",
                patternMask    ="FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00",
                               # 1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x2A, c_int, sizeof(c_int) ) ],
                addressExpected=0x0 ),
                     
            patternfinder.PatternFinder(
                label          = "ptrGameRenderer",
                patternExpected="A1 44 3A 34 02 85 C0 74 35 8B 8E BC 00 00 00 8A 91 B8 00 00 00 8B 38 88 54 24 14 83 C7 3C",
                patternMask    ="FF 00 00 00 00 FF FF FF 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF",
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x1, c_int, sizeof(c_int) ) ],
                addressExpected=0x0 ),

            patternfinder.PatternFinderFollower(
                label = "ClientGameContext",
                baseVariableName = "ptrClientGameContext",
                isPointer = True,
                valueOffsets = [0x0, None, None]
                ),
                     
            patternfinder.PatternFinderFollower(
                label = "GameTime",
                baseVariableName = "ClientGameContext",
                isPointer = True,
                valueOffsets = [0x0C, None, None]
                ),

            patternfinder.PatternFinderFollower(
                label = "GameRenderer",
                baseVariableName = "ptrGameRenderer",
                isPointer = True,
                valueOffsets = [0x0, None, None]
                ),

        ]
        
    def getRepo(self):
        return self.repo    