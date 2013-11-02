# The start of a win32gui generic demo.
# Feel free to contribute more demos back ;-)

import win32gui, win32con, win32api
import time, random

tick = 1

def drawCrossHair(hDc, centerX, centerY, size, lineWidth=1, color=win32api.RGB(255, 0, 0)):
    hPen= win32gui.CreatePen(win32con.PS_SOLID, lineWidth, color)
    win32gui.SelectObject(hDc, hPen)
    win32gui.MoveToEx(hDc, centerX-size, centerY)
    win32gui.LineTo(hDc, centerX+size, centerY)
    win32gui.MoveToEx(hDc, centerX, centerY+size)
    win32gui.LineTo(hDc, centerX, centerY-size)

def drawDummyX(hDc, initX, initY, sizeX, sizeY, scale):
    speedPerFrame = 1.0
    offset = speedPerFrame * tick
    movementX = int(offset % scale)
    win32gui.Rectangle(hDc, movementX+initX, initY, movementX+initX+sizeX, initY+sizeY)

def drawDummyY(hDc, initX, initY, sizeX, sizeY, scale):
    speedPerFrame = 1.0
    offset = speedPerFrame * tick
    movementY = int(offset % scale)
    win32gui.Rectangle(hDc, initX, movementY+initY, initX+sizeX, movementY+initY+sizeY)

def onPaint(hwnd, msg, wp, lp):
    dc, ps=win32gui.BeginPaint(hwnd)
    win32gui.SetGraphicsMode(dc, win32con.GM_ADVANCED)
    drawCrossHair(dc, 400, 500, 20)
    sizeX, sizeY = 20, 60
    drawDummyX(dc, 10, 10, sizeX, sizeY, 100)
    drawDummyX(dc, 15, 50, sizeX, sizeY, 200)
    drawDummyX(dc, 20, 100, sizeX, sizeY, 300)
    drawDummyX(dc, 30, 150, sizeX, sizeY, 400)
    drawDummyX(dc, 25, 200, sizeX, sizeY, 500)
    drawDummyX(dc, 45, 300, sizeX, sizeY, 600)
    drawDummyX(dc, 55, 400, sizeX, sizeY, 130)
    drawDummyX(dc, 66, 500, sizeX, sizeY, 230)
    drawDummyX(dc, 77, 600, sizeX, sizeY, 330)
    drawDummyX(dc, 88, 700, sizeX, sizeY, 350)

    drawDummyY(dc, 10, 10, sizeX, sizeY, 100)
    drawDummyY(dc, 15, 50, sizeX, sizeY, 200)
    drawDummyY(dc, 20, 100, sizeX, sizeY, 300)
    drawDummyY(dc, 30, 150, sizeX, sizeY, 400)
    drawDummyY(dc, 25, 200, sizeX, sizeY, 500)
    drawDummyY(dc, 45, 300, sizeX, sizeY, 600)
    drawDummyY(dc, 55, 400, sizeX, sizeY, 130)
    drawDummyY(dc, 66, 500, sizeX, sizeY, 230)
    drawDummyY(dc, 77, 600, sizeX, sizeY, 330)
    drawDummyY(dc, 88, 700, sizeX, sizeY, 350)

    drawDummyX(dc, 200, 10, sizeX, sizeY, 500)
    drawDummyX(dc, 220, 20, sizeX, sizeY, 600)
    drawDummyX(dc, 230, 40, sizeX, sizeY, 300)
    drawDummyX(dc, 240, 50, sizeX, sizeY, 100)
    drawDummyX(dc, 250, 60, sizeX, sizeY, 300)
    drawDummyX(dc, 206, 17, sizeX, sizeY, 500)
    drawDummyX(dc, 270, 80, sizeX, sizeY, 140)
    drawDummyX(dc, 280, 90, sizeX, sizeY, 450)
    drawDummyX(dc, 290, 14, sizeX, sizeY, 342)
    drawDummyX(dc, 300, 66, sizeX, sizeY, 113)

    drawDummyY(dc, 200, 10, sizeX, sizeY, 500)
    drawDummyY(dc, 220, 20, sizeX, sizeY, 600)
    drawDummyY(dc, 230, 40, sizeX, sizeY, 300)
    drawDummyY(dc, 240, 50, sizeX, sizeY, 100)
    drawDummyY(dc, 250, 60, sizeX, sizeY, 300)
    drawDummyY(dc, 206, 17, sizeX, sizeY, 500)
    drawDummyY(dc, 270, 80, sizeX, sizeY, 140)
    drawDummyY(dc, 280, 90, sizeX, sizeY, 450)
    drawDummyY(dc, 290, 14, sizeX, sizeY, 342)
    drawDummyY(dc, 300, 66, sizeX, sizeY, 113)
 
    win32gui.EndPaint(hwnd, ps)
    return 0
wndproc={win32con.WM_PAINT:onPaint}

def run():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = 'test_win32gui_2'
    wc.style = win32con.CS_GLOBALCLASS|win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wc.hbrBackground = win32con.COLOR_WINDOW+1
    wc.lpfnWndProc = wndproc
    class_atom=win32gui.RegisterClass(wc)       
    hwnd = win32gui.CreateWindowEx(
                                   win32con.WS_EX_TOPMOST|win32con.WS_EX_TRANSPARENT|win32con.WS_EX_LAYERED|win32con.WS_EX_COMPOSITED, 
                                   class_atom,
                                   'Kaleidoscope',
                                   win32con.WS_POPUP|win32con.WS_VISIBLE,
                                   100,
                                   100,
                                   900,
                                   900, 
                                   0, 
                                   0, 
                                   0, 
                                   None
                                  )
    s=win32gui.GetWindowLong(hwnd,win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, s|win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 255, 255), 255, win32con.LWA_COLORKEY)
    sleepTime = 1.0/60.0
    global tick
    try:
        while True:
            tick += 1
            win32gui.InvalidateRect(hwnd,None,True)
            win32gui.PumpWaitingMessages()
            time.sleep(sleepTime)
        win32gui.DestroyWindow(hwnd)
        win32gui.UnregisterClass(class_atom,None)
    except KeyboardInterrupt:
        win32gui.DestroyWindow(hwnd)
        win32gui.UnregisterClass(class_atom,None)  

run()
