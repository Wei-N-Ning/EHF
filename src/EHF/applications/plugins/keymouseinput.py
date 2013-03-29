from ctypes.wintypes import DWORD, LONG, ULONG, WORD, string_at, byref, Structure, Union, POINTER, sizeof, windll
from math import ceil

from EHF.plugins import base

import win32con
import win32api

INPUT_MOUSE     = 0
INPUT_KEYBOARD  = 1
INPUT_HARDWARE  = 2

MOUSEEVENTF_MOVE        = 0x0001 #/* mouse move */
MOUSEEVENTF_ABSOLUTE    = 0x8000 #/* absolute move */

class MOUSEINPUT(Structure):
    _fields_ = [ ("dx", LONG),
                 ("dy", LONG),
                 ("mouseData", DWORD),
                 ("dwFlags", DWORD),
                 ("time", DWORD),
                 ("dwExtraInfo", POINTER(ULONG))
                ]

class KEYBDINPUT(Structure):
    _fields_ = [ ("wVk", WORD),
                 ("wScan", WORD),
                 ("dwFlags", DWORD),
                 ("time", DWORD),
                 ("dwExtraInfo", POINTER(ULONG))
                ]
    
class HARDWAREINPUT(Structure):
    _fields_ = [ ("uMsg", DWORD),
                 ("wParamL", WORD),
                 ("wParamH", WORD),
                ]

class _INPUT_UNION(Union):
    _fields_ = [("mi", MOUSEINPUT),
                ("ki", KEYBDINPUT),
                ("hi", HARDWAREINPUT),
                ]

class INPUT(Structure):
    _anonymous_ = ("iu",)
    _fields_ = [ ("type", DWORD),
                 ("iu", _INPUT_UNION)]
    

class KeyMouseInputPlugin(base.BasePerFrameDataPlugin):
    """
    This plugin utilize the windll.User32 function
    GetAsyncKeyState() to get the key press/release
    state 
    
    It updates an AppInfo attribute: keyMouseInputState
    
    keyMouseInputState:
     a dict stores the nice name of the key, the id, the input type
     either "toggle" (0) or "hold" (1) and the state (True or False)
     for hold type, True means pressed, False means released;
     for toggle type, True means it has turned on something, and 
     False otherwise - in another word the downstream logic is only 
     interested in the alternating of the state but not the state
     itself
     override this inputMapping in the subclasses
     all the key-value pairs will be visited during the runtime
    """
    requirements = [ "AppInfo", "EnvInfo" ]
    contributions = []
    
    def _run(self):
        for keyMouseName, keyMouseState in self._appAttr["AppInfo"].keyMouseInputState.items():
            self.updateKeyMouseInputState(keyMouseState)
        
    def updateKeyMouseInputState(self, keyMouseState):
        """
        It updates the keyMouseState object's state attribute...
        """
        # for toggle
        if keyMouseState.type == 0:
            keyMouseState.state = \
            (windll.User32.GetAsyncKeyState(keyMouseState.id) & 0x0001) != 0
        # for hold
        elif keyMouseState.type == 1:
            _state = windll.User32.GetAsyncKeyState(keyMouseState.id) & 0x8000
            if _state:
                if not keyMouseState.state:
                    keyMouseState.state = True
            else:
                if keyMouseState.state:
                    keyMouseState.state = False


class SimpleMouseMovePlugin(base.BasePerFrameDataPlugin):
    """
    external de-recoil...
    not the old implementation using SetCursorPosition, since it no longer works
    with Frost Bite 2 games (BF3, MOHW....); rather it uses:
    windll.User32.SendInput()
    """
    requirements = [ "AppInfo", "EnvInfo" ]
    contributions = []
    
    def initialise(self):
        
        self.isEnabled = True
        self.isFiring = False
        
        self.screenCenterX = self._appAttr["AppInfo"].centerX + self._appAttr["AppInfo"].bboxLeft
        self.screenCenterY = self._appAttr["AppInfo"].centerY + self._appAttr["AppInfo"].bboxTop
        
        #self.input = INPUT()
        #self.input.type = INPUT_MOUSE
        #self.input.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        
        self.mouseMoveFlag = win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE
        
        self.frame = 0
        
    def _run(self):
        # move mouse
        insertState = self._appAttr["AppInfo"].keyMouseInputState["INSERT"].state
        if insertState:
            self.isEnabled = not self.isEnabled
        if not self.isEnabled:
            return
        self.isFiring = self._appAttr["AppInfo"].keyMouseInputState["LMB"].state
        if self.isFiring:
            px, py = self.screenCenterX, self.screenCenterY
            fScreenWidth = windll.user32.GetSystemMetrics(0) - 1.0      # SM_CXSCREEN
            fScreenHeight = windll.user32.GetSystemMetrics(1) - 1.0     # SM_CYSCREEN
            rx = 65535.0 / fScreenWidth
            ry = 65535.0 / fScreenHeight
            
            py += 130
            
            #self.input.mi.dx = int( ceil(px * rx) )
            #self.input.mi.dy = int( ceil(py * ry) )
            
            #windll.User32.SendInput(1, byref(self.input), sizeof(self.input))
            
            c_px = int(ceil(px))
            c_py = int(ceil(py))
            
            
            win32api.mouse_event(self.mouseMoveFlag, c_px, c_py)
            
            self.frame += 1
        
        else:
            self.frame = 0