"""
graphics related classes, functions
"""

from ctypes.wintypes import DWORD, LONG, ULONG, WORD, string_at, byref, Structure, Union, POINTER, sizeof, windll
from directx.types import D3DXVECTOR2
from directx.d3dx import RECT

from ctypes import cast

from math import radians, cos, sin, ceil

DT_TOP                      = 0x00000000
DT_LEFT                     = 0x00000000
DT_CENTER                   = 0x00000001
DT_RIGHT                    = 0x00000002
DT_VCENTER                  = 0x00000004
DT_BOTTOM                   = 0x00000008
DT_WORDBREAK                = 0x00000010
DT_SINGLELINE               = 0x00000020
DT_EXPANDTABS               = 0x00000040
DT_TABSTOP                  = 0x00000080
DT_NOCLIP                   = 0x00000100
DT_EXTERNALLEADING          = 0x00000200
DT_CALCRECT                 = 0x00000400
DT_NOPREFIX                 = 0x00000800
DT_INTERNAL                 = 0x00001000


LP_D3DXVECTOR2 = POINTER(D3DXVECTOR2)




# ------------- d3d draw utilities -------------
def drawLine(line, x, y, w, h, width, color):
    """
    w, h: pixel offsets from the point (x, y)
    """
    points = (D3DXVECTOR2 * 2) ((x,y), (x+w,y+h))
    line.SetWidth(width)
    line.Draw(points, len(points), color)

def drawLineAbs(line, x, y, x2, y2, width, color):
    points = (D3DXVECTOR2 * 2) ((x,y), (x2,y2))
    line.SetWidth(width)
    line.Draw(points, len(points), color)

    
def drawSpot(line, x, y, color, size=8):
    """
    draw a diamond-shaped 2x2 square 
    """
    draw4(line, x, y - size, x + size, y, x, y + size, x - size, y, size, color)

def drawSpotN(line, x, y, color, size=3, lineWidth=3):
    """
    another variant of drawSpot, offering more fine control on the sizing..
    """
    draw4(line, x, y - size, x + size, y, x, y + size, x - size, y, size, color)

def drawSpot33(line, x, y, color):
    """
    draw a diamond-shaped 2x2 square 
    """
    draw4(line, x, y - 3, x + 3, y, x, y + 3, x - 3, y, 3, color)

def drawSpot55WithDot(line, x, y, color):
    """
    draw a diamond-shaped 5x5 squre with a dot in the middle
    """
    draw4(line, x, y - 5, x + 5, y, x, y + 5, x - 5, y, 1, color)
    draw4(line, x, y - 1, x + 1, y, x, y + 1, x - 1, y, 1, color)


def drawCrosshair(line, x, y, size, width, color):
    """
     + shaped crosshair
    """
    drawLineAbs(line, x-size, y, x+size, y, width, color)
    drawLineAbs(line, x, y-size, x, y+size, width, color)


def drawXCrosshair(line, x, y, size, width, color):
    """
     x shaped crosshair
    """
    drawLineAbs(line, x-size, y+size, x+size, y-size, width, color)
    drawLineAbs(line, x-size, y-size, x+size, y+size, width, color)

    
def draw4(line, x1, y1, x2, y2, x3, y3, x4, y4, width, color):
    line.SetWidth(width)
    points = (D3DXVECTOR2 * 5) ((x1,y1), (x2,y2), (x3,y3), (x4,y4), (x1,y1))
    line.Draw(points, len(points), color)


def drawDirectionalLineYaw(line, x, y, size, yaw, color):
    """
    a more complicated line method that receives the origin point and
    a yaw value which is inside range (0, 360) in deg or (0, 2pi) in rad. 
    """
    pass

def drawDirectionalLineVec(line, x, y, size, lookVector, color):
    """
    a variant of the previous function with the difference that this
    one requires a 2D vector instead of the yaw value 
    """
    pass
    
def drawArrow(line, x, y, yaw, color):
    """
    yaw: control the direction
    """
    points = (D3DXVECTOR2 * 3) ((-3,5), (0,0), (3.5,5.5))
    points2 = (D3DXVECTOR2 * 3) ((0,0), (0,0), (0,0))
    rad_dir = radians(yaw)
    for i in range(len(points)):
        c = cos(rad_dir)
        s = sin(rad_dir)
        points2[i].x = ((points[i].x * c) - (points[i].y * s)) + x
        points2[i].y = ((points[i].y * c) + (points[i].x * s)) + y
    line.SetWidth(2)
    line.Draw(points2, len(points2), color)


def drawBox(line, x, y, w, h, width, color):
    """
    w, h: width and height of the box,
    x, y: top-left corner
    """
    points = (D3DXVECTOR2 * 5) ((x,y), (x+w,y), (x+w,y+h), (x,y+h), (x,y))
    line.SetWidth(width)
    line.Draw(points, len(points), color)


def drawStringLeft(font, x, y, w, h, color, text):
    """
    (x, y) defines the top-left corner of the text
    """
    r = RECT(int(x), int(y), int(x+w), int(y-h))
    font.DrawTextA(None, text, -1, byref(r), DT_LEFT | DT_NOCLIP | DT_SINGLELINE, color)


def drawStringRight(font, x, y, w, h, color, text):
    """
    (x, y) defines the bottom-right corner of the text
    """
    r = RECT(int(x-w), int(y-h), int(x), int(y))
    font.DrawTextA(None, text, -1, byref(r), DT_RIGHT | DT_NOCLIP | DT_SINGLELINE, color)


# ------------- xx -------------