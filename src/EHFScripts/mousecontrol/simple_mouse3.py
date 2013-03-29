from ctypes import *

import time

InputMapping = \
{
"LMB":0x01,
"RMB":0x02,
"INSERT":0x2D,
}

PRESSED = 0x01
TOGGLE  = 0x80

SLEEP_TIME = 1.0 / 60.0

def simpleInput():
    isPressed = False
    
    keyStateLMB = False
    keyStateInsert = False
    
    toggleState = False
    
    while True:
        keyStateLMB = windll.User32.GetAsyncKeyState(InputMapping["LMB"]) & 0x8000
        keyStateInsert = (windll.User32.GetAsyncKeyState(InputMapping["INSERT"]) & 0x0001) != 0
        
        if keyStateLMB:
            if not isPressed:
                print "LMB pressed!"
                isPressed = True
        else:
            if isPressed:
                print "LMB released!"
                isPressed = False
                
        # to toggle!
        if keyStateInsert:
            toggleState = not toggleState
            print "toggled! state:", toggleState
        
        
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    simpleInput()