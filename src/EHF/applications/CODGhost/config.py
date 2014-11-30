from EHF.core import entity
from EHF.core import win32types

from EHF.libs.ehfmemory import patternfinder


class CODGhostAppInfo(entity.AppInfo):
    def override(self):
        self.appName = "COD GHOST ehf application"
        self.isDryRun = False
        self.isProfiling = False
        self.targetAppName = "Call of Duty Ghosts Multiplayer"
        self.targetAppWindowClass = "IW6"
        self.targetMemStart = 0x140001000
        self.targetMemSize =  0x001900000
        
        self.vars = {}
        

class CODGhostEnvInfo(entity.EnvInfo):
    def override(self):
        self.crossHairStyle = 0
        self.crossHairSize = 8
        self.crossHairLineWidth = 2
        
        
class PatternFinderRepo(object):
    def __init__(self):
        self.repo = \
            [
             
              patternfinder.PatternFinder(
                label          = "RefdefAddress",
                # the 4th reference from refdef, based on 20131109 dump
                patternExpected= "48 8D 15 54 09 4B 01 0F 28 D8 33 DB 8B CE 89 5C 24 20 E8 24 FB 20 00 E8 BF 6A 4A 00 8B CE",
                patternMask    = "FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF 00 00 00 00 FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x3, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x7
                ),
             
              # the size of the entity is also in that location (imul r13, 238h)
              patternfinder.PatternFinder(
                label          = "EntityAddress",
                # the 6th reference from Entity, based on 20131109 dump
                patternExpected= "40 53 57 41 54 41 55 41 56 48 83 EC 60 4C 63 E2 48 8D 05 39 02 55 01 44 8B F1 4D 8B EC 49 8B F8 4D 69 ED 38 02 00 00 4C 03 E8",
                patternMask    = "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x13, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x17
                ),
             
              # the size of the ClientInfo is also in that location (imul    rax, 5D8h)
              patternfinder.PatternFinder(
                label          = "ClientInfo",
                # the 9th reference from ClientInfo, based on 20131109 dump
                patternExpected= "4C 8B DC 49 89 73 18 49 89 7B 20 55 41 56 41 57 49 8D AB 48 FF FF FF 48 81 EC A0 01 00 00 48 63 05 33 96 33 01 48 63 F9 48 8D 0D 81 0F 43 01",
                patternMask    = "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF 00 00 00 00",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x2B, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x2F
                ),
             
              # the size of the player name can be found from the 1st xref (imul    rdx, 70h)
              patternfinder.PatternFinder(
                label          = "PlayerNames",
                # the 2nd reference from PlayerNames, based on 20131109 dump
                patternExpected= "48 8D 3D 58 EF 43 01 33 DB F3 44 0F 10 44 24 38 F3 44 0F 10 4C 24 34 F3 44 0F 10 54 24 30",
                patternMask    = "FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x3, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x7
                ),
             
              # be careful! the instruction (test    cs:IsInGame, 2000h) is longer than usual two operand instructions
              # the "offsetStarting" value in this case is offset + 0x8 !!
              patternfinder.PatternFinder(
                label          = "IsInGame",
                # the 1st reference from IsInGame, based on 20131109 dump
                patternExpected= "48 89 6C 24 10 48 89 74 24 18 57 48 83 EC 20 F7 05 27 4D 44 01 00 20 00 00 49 8B F8 8B F2 8B E9",
                patternMask    = "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x11, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x19
                ),

              patternfinder.PatternFinder(
                label          = "LocalClientNum",
                # the 8st reference from LocalClientNum, based on 20131109 dump
                patternExpected= "48 63 0D 7C AC 33 01 48 63 56 18 48 8B C1 48 69 C0 D8 05 00 00 44 8B 84 38 0C AC 0F 00 48 8B C2 48 69 C0 D8 05 00 00 45 85 C0",
                patternMask    = "FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x3, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x7
                ),

              patternfinder.PatternFinder(
                label          = "CurrentMapName",
                # the only reference from CurrentMapName, based on 20131109 dump
                patternExpected= "3B 1D 0D 4F 41 01 0F 28 44 24 40 4C 8B 85 A0 00 00 00 48 8D 45 90 48 8D 15 EA 37 FD 06 41 8B CD 66 0F 7F 45 90",
                patternMask    = "FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x2, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x6
                ),

              patternfinder.PatternFinder(
                label          = "ViewAngles",
                # the 1st reference from ViewAngles, based on 20131109 dump
                patternExpected= "F3 0F 10 0D 6C A0 3E 01 F3 41 0F 59 C0 F3 0F 58 C8 F3 0F 10 45 D7 F3 0F 59 C6 F3 41 0F 59 C3",
                patternMask    = "FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x4, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x8
                ),

              patternfinder.PatternFinder(
                label          = "Sensitivity",
                # the only reference from Sensitivity, based on 20131109 dump
                patternExpected= "F3 0F 5E C1 F3 0F 59 40 10 48 8B 05 DE 2D 96 01 F3 0F 58 40 10 F3 0F 59 83 90 34 00 00 48 8B 5C 24 50 0F 28 C8",
                patternMask    = "FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0xc, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x10
                ),

              patternfinder.PatternFinder(
                label          = "PlayerCount",
                # the 4th reference from PlayerCount, based on 20131109 dump
                patternExpected= "3B 15 BC 9B 3B 01 7F 2F 48 8D 0D EB 9B 3B 01 8D 42 FF 48 98 48 6B C0 58 48 03 C1 48 63 08 83 F9 2A",
                patternMask    = "FF FF 00 00 00 00 FF 00 FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x2, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x6
                ),

            ]
            
    def getRepo(self):
        return self.repo