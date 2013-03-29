from ctypes import c_int, c_float, sizeof

from EHF.applications.MOHW import datastruct
from EHF.core import entity
from EHF.libs.ehfmemory import patternfinder


class MOHWAppInfo(entity.AppInfo):
    def override(self):
        self.appName = "MOHW ehf application"
        self.isDryRun = False
        self.isProfiling = False
        self.targetAppName = "Medal of Honor Warfighter"
        self.targetAppWindowClass = "Medal of Honor Warfighter"
        self.targetMemStart = 0x00401000
        self.targetMemSize =  0x02400000
        self.keyMouseInputState = \
        {
         # hold type
         "LMB":entity.KeyMouse("LMB", 0x01, 1, False),
         "RMB":entity.KeyMouse("RMB", 0x02, 1, False),
         
         # toggle type
         "INSERT":entity.KeyMouse("INSERT", 0x2D, 0, False),
        }
        # application-only attributes
        self.vars = {
                     "players"        : [datastruct.SimplePlayer() for i in range(datastruct.MAXPLAYER)],
                    }
        self.windowMode = "overlay"
        
class MOHWEnvInfo(entity.EnvInfo):
    def override(self):
        self.crossHairStyle = 0 # +
        self.crossHairSize = 8
        self.crossHairLineWidth = 2
        

class PatternFinderRepo(object):
    def __init__(self):
        self.repo = [
            
            # [IMPORTANT]:
            # the pattern finder for ptrClientGameContext will produce the address of client game context POINTER,
            # to get the actual client game context I need to evaluate this pointer first! (thus why there's a follower)
            
            patternfinder.PatternFinder(
                label          = "ptrClientGameContext",
                patternExpected="8B 06 8B 50 20 8B CE FF D2 8B 0D 24 3C AA 02 8B 86 9C 03 00 00 89 41 28",
                patternMask    ="FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF",
                               # 1  2  3  4  5  6  7  8  9  A  B  *, that why the offset is 0xB!
                patternMatch   ="FF",
                valueOffsets   =[ ( 0xB, c_int, sizeof(c_int) ) ],
                addressExpected=0x0 ),

            patternfinder.PatternFinder(
                label          = "ptrGameRenderer",
                patternExpected="D9 5C 24 04 8B 0D 10 6C AA 02 8B 11 F3 0F 10 44 24 04 8B 42 68 51 F3 0F 11 04 24 FF D0",
                patternMask    ="FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               # 1  2  3  4  5  6  * offset = 0x6
                patternMatch   ="FF",
                valueOffsets   =[ ( 0x6, c_int, sizeof(c_int) ) ],
                addressExpected=0x0 ),

            patternfinder.PatternFinderFollower(
                label = "ClientGameContext",
                baseVariableName = "ptrClientGameContext",
                isPointer=True,
                valueOffsets=[0x0, None, None],
                ),

            patternfinder.PatternFinderFollower(
                label = "GameRenderer",
                baseVariableName = "ptrGameRenderer",
                isPointer=True,
                valueOffsets=[0x0, None, None],
                ),

            # [IMPORTANT]:
            # this static finder (and its followers) should not be used, but LEAVE IT HERE for reference,
            # it appears to be another valid way to get the client game context, and later on i should make 
            # it a pattern finder, and check the result (client game context) with the first pattern finder
            
#            patternfinder.StaticFinder(
#                label = "Main",
#                address = 0x02A2B100  
#                ),
#            patternfinder.PatternFinderFollower(
#                label = "pMain",
#                baseVariableName = "Main",
#                isPointer=True,
#                valueOffsets=[0x0, None, None],
#                ),
#            patternfinder.PatternFinderFollower(
#                label = "Client",
#                baseVariableName = "pMain",
#                isPointer=True,
#                valueOffsets=[0x3A4, None, None],
#                ),
#            patternfinder.PatternFinderFollower(
#                label = "ClientGameContext",
#                baseVariableName = "Client",
#                isPointer=True,
#                valueOffsets=[0xC, None, None],
#                ),

            patternfinder.PatternFinderFollower(
                label = "GameTime",
                baseVariableName = "ClientGameContext",
                isPointer=True,
                valueOffsets=[0xC, None, None],
                ),

            patternfinder.PatternFinderFollower(
                label = "ClientLevel",
                baseVariableName = "ClientGameContext",
                isPointer=True,
                valueOffsets=[0x10, None, None],
                ),

            # [IMPORT] a test pattern to validate the ClientPlayerManager address's correctness
#            patternfinder.PatternFinderFollower(
#                label = "ptrLocalPlayerName",
#                baseVariableName = "LocalPlayer",
#                isPointer=True,
#                valueOffsets=[0x10, None, None],
#                ),
        
        ]
        
    def getRepo(self):
        return self.repo    
