import psutil

from ctypes import windll
kernel32 = windll.kernel32
user32 = windll.user32

from EHF.core.win32types import *
from EHF.core import datastruct

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class ProcessHelper(object):
    """
    An utility class holding a collection of win-process related functionalities
    
    * hwnd: window handle
    * pid : window process id
    * tid : window thread id
    * windowRect: a data structure holding the left/right/top/bottom value of the window
                  Note that these values represent the bbox, thus right - left >= resolutionX;
                  bottom - top >= resolutionY
    * clientRect: a data structure associated with the previous rect but holding the "canvas"
                  instead of the bbox values.
                  the top and left of clientRect will always be 0, thus making it safe to 
                  compute the resolutionX and resolutionY by right - left and bottom - top
    """
    def __init__(self):
        self.hwnd = 0
        self.pid = 0
        self.tid = 0
        self.windowRect = datastruct.RECT()
        self.clientRect = datastruct.RECT()
        self.origPoint = datastruct.POINT(0, 0)
        self.process = None
        self.hProcess = None # cached from OpenProcess()
        
    def findProcessByName(self, processName=""):
        """
        Note that this method relies on psutil, which does not provide a way
        to directly access to the window thread
        
        * It's suggested to use findWindowByClass() method for all the window-related
        access.
        
        return process id
        """
        for _process in psutil.process_iter():
            if _process.name == processName:
                self.pid = _process.pid # cache the result
                self.process = _process
                logger.debug(" + Found process %d by name [%s]" % (self.pid, processName))
                return _process.pid
        return 0
    
    def findWindowByClass(self, windowClassName=""):
        """
        To get the window class name of a certain running application, use spy++ 
        (shipped with visual studio retail, can be found in its launch menu)
        
        * It also populates the process id 
        
        return the window handle
        """
        self.hwnd = user32.FindWindowA(windowClassName, None) # cache the result 
        _hwnd = c_int(0)
        self.tid = user32.GetWindowThreadProcessId(self.hwnd, byref(_hwnd))
        self.pid = _hwnd.value
        logger.debug(" + Found hwnd %d process %s by window class [%s]" % (self.hwnd, self.pid, windowClassName))
        return self.hwnd
    
    def openProcess(self):
        self.hProcess = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        return self.hProcess
    
    def populateWindowRect(self):
        """
        populate member structs windowRect and clientRect
        """
        user32.GetWindowRect(self.hwnd, byref(self.windowRect))
        user32.GetClientRect(self.hwnd, byref(self.clientRect))
        user32.ClientToScreen(self.hwnd, byref(self.origPoint))
        logger.debug(
                  " + Populated rects:\n"\
                  "windowRect.left   : %d\n"\
                  "windowRect.right  : %d\n"\
                  "windowRect.top    : %d\n"\
                  "windowRect.bottom : %d\n\n"\
                  "clientRect.left   : %d\n"\
                  "clientRect.right  : %d\n"\
                  "clientRect.top    : %d\n"\
                  "clientRect.bottom : %d\n\n"\
                  "origin.x  : %d\n"\
                  "origin.y  : %d"%(self.windowRect.left,
                                    self.windowRect.right,
                                    self.windowRect.top,
                                    self.windowRect.bottom,
                                    self.clientRect.left,
                                    self.clientRect.right,
                                    self.clientRect.top,
                                    self.clientRect.bottom,
                                    self.origPoint.x,
                                    self.origPoint.y)
                  )