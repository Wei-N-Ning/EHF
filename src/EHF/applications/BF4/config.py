from EHF.core import entity
from EHF.core import win32types

from EHF.libs.ehfmemory import patternfinder


class BF4AppInfo(entity.AppInfo):
    def override(self):
        self.appName = "BF4 ehf application"
        self.isDryRun = False
        self.isProfiling = False
        self.targetAppName = "Battlefield 4"
        self.targetAppWindowClass = "Battlefield 4"
        self.targetMemStart = 0x140001000
        self.targetMemSize =  0x001900000
        
        self.vars = {}

class TestAppInfo(entity.AppInfo):
    def override(self):
        self.appName = "BF4 test"
        self.isDryRun = False
        self.isProfiling = False
        self.targetAppName = "notepad"
        self.targetAppWindowClass = "Notepad"
        self.targetMemStart = 0x140001000
        self.targetMemSize =  0x001900000


class BF4EnvInfo(entity.EnvInfo):
    def override(self):
        self.crossHairStyle = 0
        self.crossHairSize = 8
        self.crossHairLineWidth = 2


class PatternFinderRepo(object):
    def __init__(self):
        """
        NEED TO UPDATE THE finger class to support the cs:xxxx like address-offset!! record
        the starting address of the pattern!
        
        """
        self.repo = \
           [
            patternfinder.PatternFinder(
                label          = "GameContextPtrAddress",
                # the 4th reference from gamecontext, based on 20131001 dump
                patternExpected= "48 8B 06 48 8B 15 E6 E1 41 02 48 8B CE FF 90 F0 00 00 00 49 8B 3E 48 8B B6 50 01 00 00 48 3B FE",
                patternMask    = "FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x6, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0xA
                ),
            patternfinder.PatternFinder(
                label          = "DxRendererPtrAddress",
                # the 3rd reference from dx renderer, based on 20131001 dump
                patternExpected= "48 89 5C 24 08 48 89 6C 24 10 48 89 74 24 18 57 48 83 EC 30 8B D9 48 8B 0D 83 F4 0D 02 0F 29 74 24 20 0F 28 F3 41 8B F0 8B EA 33 FF",
                patternMask    = "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x19, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x1D
                ),
            patternfinder.PatternFinder(
                label          = "GameRendererPtrAddress",
                # the 5th reference from game renderer, based on 20131031 retail dump
                patternExpected= "0F 29 90 78 FF FF FF 44 0F 29 98 68 FF FF FF 44 0F 29 A0 58 FF FF FF 44 0F 29 A8 48 FF FF FF 49 8B D8 8B FA 4C 8B E9 48 8B 0D 96 2D C8 01",
                patternMask    = "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x2A, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0x2E
                ),
            patternfinder.PatternFinder(
                label          = "BorderInputNodePtrAddress",
                # the 8th reference from border input node, based on 20131001 dump
                patternExpected= "40 53 48 83 EC 30 48 8B 1D 63 B5 C9 01 0F 29 74 24 20 0F 28 F0 48 8B 43 08 C6 00 00 48 8B 4B 40 48 85 C9",
                patternMask    = "FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
                               #  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A
                patternMatch   = "FF",
                valueOffsets   = [ ( 0x9, win32types.c_uint, win32types.sizeof(win32types.c_uint) ) ],
                addressExpected= 0x0,
                offsetStarting = 0xD
                ),
            
            # ---------------------------------------------------------------------------------
            patternfinder.PatternFinderFollower(
                label = "GameContextAddress",
                baseVariableName = "GameContextPtrAddress",
                isPointer = True,
                valueOffsets = [0x0, win32types.c_ulonglong, win32types.sizeof(win32types.c_ulonglong)]
                ),
            patternfinder.PatternFinderFollower(
                label = "PlayerManagerAddress",
                baseVariableName = "GameContextAddress",
                isPointer = True,
                valueOffsets = [0x60, win32types.c_ulonglong, win32types.sizeof(win32types.c_ulonglong)]
                ),
            patternfinder.PatternFinderFollower(
                label = "GameRendererAddress",
                baseVariableName = "GameRendererPtrAddress",
                isPointer = True,
                valueOffsets = [0x0, win32types.c_ulonglong, win32types.sizeof(win32types.c_ulonglong)]
                ),
            patternfinder.PatternFinderFollower(
                label = "RenderViewAddress",
                baseVariableName = "GameRendererAddress",
                isPointer = True,
                valueOffsets = [0x60, win32types.c_ulonglong, win32types.sizeof(win32types.c_ulonglong)]
                ),
            # firstPersonTransform: 0x40 (need to figure out the matrix mem layout!)
            # according to the Mat4.h from bf3 sdk, it seems to be column-major order
            
            # aspect ratio: 0xC4
            # fovY: 0xB4
            # fovX: 0x250???
            patternfinder.PatternFinderFollower(
                label = "LocalPlayerAddress",
                baseVariableName = "PlayerManagerAddress",
                isPointer = True,
                valueOffsets = [0x2A0, win32types.c_ulonglong, win32types.sizeof(win32types.c_ulonglong)]
                ),
            patternfinder.PatternFinderFollower(
                label = "PlayerPtrArrayAddress",
                baseVariableName = "PlayerManagerAddress",
                isPointer = True,
                valueOffsets = [0x2A8, win32types.c_ulonglong, win32types.sizeof(win32types.c_ulonglong)]
                ),
           ]

    def getRepo(self):
        return self.repo  