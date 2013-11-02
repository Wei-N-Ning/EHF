import random
import time

import win32gui
import win32con


def _createWindowClass(name="test"):
    """
    @return: the class atom
    @rtype :
    """
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = name
    wc.style = win32con.CS_GLOBALCLASS | win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wc.hbrBackground = win32con.COLOR_WINDOW + 1
    wc.lpfnWndProc = {win32con.WM_PAINT : _onPaint}
    classAtom = win32gui.RegisterClass(wc)
    return classAtom

def _onPaint(hwnd, msg, wp, lp):
    hDc, ps = win32gui.BeginPaint(hwnd)
    win32gui.SetGraphicsMode(hDc, win32con.GM_ADVANCED)
    # -------------------
    
    # -------------------
    win32gui.EndPaint(hwnd, ps)
    return 0

def _drawCrossHair(hDc):
    pass

def _drawPlayerRect(hDc, posX, posY, scale, stance=0):
    pass
    
def run():
    pass


class MockDataFeeder(object):
    
    def __init__(self, application):
        pass
    
    
if __name__ == "__main__":
    pass